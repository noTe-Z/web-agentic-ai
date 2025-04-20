from fastapi import APIRouter, HTTPException
from ..models.chat import ChatRequest, ChatResponse, Message, ToolResultRequest, ToolCall, ToolResult
from ..utils.llm_client import claude_client
from ..utils.tools import tool_registry
from ..core.conversation_manager import conversation_manager
import uuid
import sys
from typing import Dict, List, Any, Optional

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat request and return a response from Claude.
    
    Args:
        request: The chat request containing messages and optionally a conversation_id
        
    Returns:
        ChatResponse: The response from Claude
    """
    try:
        # Get or create conversation_id
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Get existing conversation history or create new
        claude_messages = []
        if conversation_id in conversation_manager.conversations:
            claude_messages = conversation_manager.get_conversation(conversation_id)
        else:
            # If this is a new conversation, create the workspace directory
            conversation_manager.create_conversation()
        
        # Add new messages from the request
        for message in request.messages:
            if message.role == "user" and (not claude_messages or claude_messages[-1]["role"] != "user"):
                # Add user message directly
                new_message = {"role": "user", "content": message.content}
                conversation_manager.add_message(conversation_id, new_message)
                claude_messages.append(new_message)
            elif message.role == "assistant" and (not claude_messages or claude_messages[-1]["role"] != "assistant"):
                # Add assistant message directly
                new_message = {"role": "assistant", "content": message.content}
                conversation_manager.add_message(conversation_id, new_message)
                claude_messages.append(new_message)
        
        # Check if we should use a mock response for testing
        use_mock = False
        try:
            # Try to call Claude API
            print(f"Sending {len(claude_messages)} messages to Claude API", file=sys.stderr)
            response = claude_client.create_message(claude_messages)
            
            # Extract text content and tool calls
            assistant_message = ""
            tool_calls = None
            
            # Extract text content from response
            for content_block in response.content:
                if content_block.type == "text":
                    assistant_message += content_block.text
            
            # Extract tool calls from response
            extracted_tool_calls = claude_client.extract_tool_calls(response)
            if extracted_tool_calls:
                tool_calls = []
                for tool_call in extracted_tool_calls:
                    # Add the pending tool call to conversation manager
                    conversation_manager.add_pending_tool_call(
                        conversation_id, 
                        tool_call["id"], 
                        tool_call
                    )
                    
                    # Add to response tool calls list
                    tool_calls.append(ToolCall(**tool_call))
                
                print(f"Found {len(tool_calls)} tool calls in response", file=sys.stderr)
            
        except Exception as e:
            print(f"Error calling Claude API: {e}", file=sys.stderr)
            print("Using mock response for testing", file=sys.stderr)
            use_mock = True
            
        if use_mock:
            # Create a mock response for testing
            last_user_message = next((m["content"] for m in reversed(claude_messages) if m["role"] == "user"), "")
            assistant_message = f"This is a mock response. You said: {last_user_message}"
            tool_calls = None
        
        # Store assistant response in conversation history
        assistant_response = {"role": "assistant", "content": assistant_message}
        conversation_manager.add_message(conversation_id, assistant_response)
        
        # Create response
        return ChatResponse(
            conversation_id=conversation_id,
            message=Message(
                role="assistant",
                content=assistant_message
            ),
            tool_calls=tool_calls
        )
    except Exception as e:
        print(f"Error processing chat request: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tool-results", response_model=ChatResponse)
async def process_tool_results(request: ToolResultRequest):
    """
    Process results from tool calls and continue the conversation.
    
    Args:
        request: The tool results request
        
    Returns:
        ChatResponse: The next response from Claude
    """
    try:
        conversation_id = request.conversation_id
        
        # Verify conversation exists
        if not conversation_manager.get_conversation(conversation_id):
            raise HTTPException(status_code=404, detail=f"Conversation not found: {conversation_id}")
        
        # Verify tool calls exist for this conversation
        pending_tool_calls = conversation_manager.get_pending_tool_calls(conversation_id)
        if not pending_tool_calls:
            raise HTTPException(status_code=400, detail="No pending tool calls for this conversation")
        
        # Process each tool result
        for tool_result in request.tool_results:
            # Check if this tool call exists
            if tool_result.tool_call_id not in pending_tool_calls:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Tool call not found: {tool_result.tool_call_id}"
                )
            
            # Format the tool result for Claude's message format
            tool_result_message = {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_result.tool_call_id,
                        "content": tool_result.result
                    }
                ]
            }
            
            # Add tool result to conversation history
            conversation_manager.add_message(conversation_id, tool_result_message)
            
            # Remove pending tool call
            conversation_manager.remove_pending_tool_call(conversation_id, tool_result.tool_call_id)
        
        # Get the updated conversation history
        claude_messages = conversation_manager.get_conversation(conversation_id)
        
        # Call Claude API with the updated conversation
        try:
            print(f"Sending updated conversation with tool results to Claude API", file=sys.stderr)
            response = claude_client.create_message(claude_messages)
            
            # Extract text content and tool calls
            assistant_message = ""
            tool_calls = None
            
            # Extract text content from response
            for content_block in response.content:
                if content_block.type == "text":
                    assistant_message += content_block.text
            
            # Extract tool calls from response
            extracted_tool_calls = claude_client.extract_tool_calls(response)
            if extracted_tool_calls:
                tool_calls = []
                for tool_call in extracted_tool_calls:
                    # Add the pending tool call to conversation manager
                    conversation_manager.add_pending_tool_call(
                        conversation_id, 
                        tool_call["id"], 
                        tool_call
                    )
                    
                    # Add to response tool calls list
                    tool_calls.append(ToolCall(**tool_call))
                
                print(f"Found {len(tool_calls)} tool calls in response", file=sys.stderr)
            
            # Store assistant response in conversation history
            assistant_response = {"role": "assistant", "content": assistant_message}
            conversation_manager.add_message(conversation_id, assistant_response)
            
            # Create response
            return ChatResponse(
                conversation_id=conversation_id,
                message=Message(
                    role="assistant",
                    content=assistant_message
                ),
                tool_calls=tool_calls
            )
            
        except Exception as e:
            print(f"Error calling Claude API with tool results: {e}", file=sys.stderr)
            raise HTTPException(status_code=500, detail=str(e))
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing tool results: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e)) 
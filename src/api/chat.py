from fastapi import APIRouter, HTTPException
from ..models.chat import ChatRequest, ChatResponse, Message, ToolResultRequest
from ..utils.llm_client import claude_client
import uuid
import sys
from typing import Dict, List, Any

router = APIRouter()

# In-memory store for conversations
conversations: Dict[str, List[Dict[str, Any]]] = {}

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat request and return a response from Claude.
    
    Args:
        request: The chat request containing messages and optionally a conversation_id
        
    Returns:
        ChatResponse: The response from Claude
    """
    # Get or create conversation_id
    conversation_id = request.conversation_id or str(uuid.uuid4())
    
    # Convert Pydantic messages to dict format required by Claude
    claude_messages = []
    
    # Get existing conversation history or create new
    if conversation_id in conversations:
        claude_messages = conversations[conversation_id]
    
    # Add new messages from the request
    for message in request.messages:
        if message.role == "user" and (not claude_messages or claude_messages[-1]["role"] != "user"):
            # Add user message directly
            claude_messages.append({"role": "user", "content": message.content})
        elif message.role == "assistant" and (not claude_messages or claude_messages[-1]["role"] != "assistant"):
            # Add assistant message directly
            claude_messages.append({"role": "assistant", "content": message.content})
    
    try:
        # Check if we should use a mock response for testing
        use_mock = False
        try:
            # Try to call Claude API
            print(f"Sending {len(claude_messages)} messages to Claude API", file=sys.stderr)
            response = claude_client.create_message(claude_messages)
            assistant_message = response.content[0].text
        except Exception as e:
            print(f"Error calling Claude API: {e}", file=sys.stderr)
            print("Using mock response for testing", file=sys.stderr)
            use_mock = True
            
        if use_mock:
            # Create a mock response for testing
            last_user_message = next((m["content"] for m in reversed(claude_messages) if m["role"] == "user"), "")
            assistant_message = f"This is a mock response. You said: {last_user_message}"
        
        # Store updated conversation
        conversations[conversation_id] = claude_messages + [
            {"role": "assistant", "content": assistant_message}
        ]
        
        # Create response
        return ChatResponse(
            conversation_id=conversation_id,
            message=Message(
                role="assistant",
                content=assistant_message
            ),
            tool_calls=None  # Initial version doesn't handle tool calls yet
        )
    except Exception as e:
        print(f"Error processing chat request: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tool-results")
async def process_tool_results(request: ToolResultRequest):
    """
    Process results from tool calls and continue the conversation.
    
    Args:
        request: The tool results request
        
    Returns:
        ChatResponse: The next response from Claude
    """
    # This endpoint will be fully implemented in a future phase
    # For now, it just returns a simple response
    
    if request.conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Placeholder response
    return ChatResponse(
        conversation_id=request.conversation_id,
        message=Message(
            role="assistant",
            content="I've received the tool results. This endpoint will be fully implemented in a future phase."
        ),
        tool_calls=None
    ) 
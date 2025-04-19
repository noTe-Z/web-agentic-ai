from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal, Union


class Message(BaseModel):
    """Base model for chat messages."""
    role: Literal["user", "assistant"] = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    """Model for chat request from client."""
    messages: List[Message] = Field(..., description="List of conversation messages")
    conversation_id: Optional[str] = Field(None, description="ID of the conversation")


class ToolParameter(BaseModel):
    """Model for tool parameter."""
    name: str = Field(..., description="Name of the parameter")
    description: str = Field("", description="Description of the parameter")
    required: bool = Field(False, description="Whether the parameter is required")
    type: str = Field("string", description="Type of the parameter")


class ToolDefinition(BaseModel):
    """Model for tool definition."""
    name: str = Field(..., description="Name of the tool")
    description: str = Field(..., description="Description of the tool")
    parameters: List[ToolParameter] = Field(default_factory=list, description="Parameters of the tool")


class ToolCall(BaseModel):
    """Model for tool call from LLM."""
    id: str = Field(..., description="ID of the tool call")
    type: str = Field("tool_call", description="Type of the content")
    tool: ToolDefinition = Field(..., description="Tool definition")
    input: Dict[str, Any] = Field(..., description="Input parameters for the tool")


class ToolResult(BaseModel):
    """Model for tool call result."""
    tool_call_id: str = Field(..., description="ID of the tool call")
    result: Any = Field(..., description="Result of the tool call")
    error: Optional[str] = Field(None, description="Error message if tool call failed")


class ChatResponse(BaseModel):
    """Model for chat response to client."""
    conversation_id: str = Field(..., description="ID of the conversation")
    message: Message = Field(..., description="Response message")
    tool_calls: Optional[List[ToolCall]] = Field(None, description="Tool calls requested by assistant")


class ToolResultRequest(BaseModel):
    """Model for tool result request from client."""
    conversation_id: str = Field(..., description="ID of the conversation")
    tool_results: List[ToolResult] = Field(..., description="Results of tool calls") 
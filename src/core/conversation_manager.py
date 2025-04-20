import uuid
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from ..config import settings

class ConversationManager:
    """
    Manages conversations and their associated workspaces.
    
    This class handles:
    - In-memory tracking of conversation histories
    - Creating and managing conversation workspaces (directories)
    - Associating tool calls with conversations
    """
    
    def __init__(self):
        """Initialize the conversation manager."""
        # Store conversations in memory
        # {conversation_id: [message1, message2, ...]}
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}
        
        # Store pending tool calls for each conversation
        # {conversation_id: {tool_call_id: tool_call_info}}
        self.pending_tool_calls: Dict[str, Dict[str, Any]] = {}
        
        # Create the base workspace directory if it doesn't exist
        os.makedirs(settings.WORKSPACE_DIR, exist_ok=True)
        print(f"Initialized ConversationManager with workspace at {settings.WORKSPACE_DIR}", file=sys.stderr)
    
    def get_conversation(self, conversation_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get a conversation by ID.
        
        Args:
            conversation_id: The ID of the conversation
            
        Returns:
            The conversation messages or None if not found
        """
        return self.conversations.get(conversation_id)
    
    def create_conversation(self) -> str:
        """
        Create a new conversation with a unique ID.
        
        Returns:
            The ID of the new conversation
        """
        conversation_id = str(uuid.uuid4())
        self.conversations[conversation_id] = []
        self._create_workspace(conversation_id)
        return conversation_id
    
    def add_message(self, conversation_id: str, message: Dict[str, Any]) -> None:
        """
        Add a message to a conversation.
        
        Args:
            conversation_id: The ID of the conversation
            message: The message to add
        """
        if conversation_id not in self.conversations:
            self.create_conversation()
        
        self.conversations[conversation_id].append(message)
    
    def add_pending_tool_call(self, conversation_id: str, tool_call_id: str, tool_call: Dict[str, Any]) -> None:
        """
        Add a pending tool call to a conversation.
        
        Args:
            conversation_id: The ID of the conversation
            tool_call_id: The ID of the tool call
            tool_call: The tool call information
        """
        if conversation_id not in self.pending_tool_calls:
            self.pending_tool_calls[conversation_id] = {}
        
        self.pending_tool_calls[conversation_id][tool_call_id] = tool_call
    
    def get_pending_tool_calls(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get all pending tool calls for a conversation.
        
        Args:
            conversation_id: The ID of the conversation
            
        Returns:
            Dictionary of pending tool calls {tool_call_id: tool_call_info}
        """
        return self.pending_tool_calls.get(conversation_id, {})
    
    def remove_pending_tool_call(self, conversation_id: str, tool_call_id: str) -> None:
        """
        Remove a pending tool call from a conversation.
        
        Args:
            conversation_id: The ID of the conversation
            tool_call_id: The ID of the tool call
        """
        if conversation_id in self.pending_tool_calls:
            if tool_call_id in self.pending_tool_calls[conversation_id]:
                del self.pending_tool_calls[conversation_id][tool_call_id]
    
    def get_workspace_path(self, conversation_id: str) -> Path:
        """
        Get the path to a conversation's workspace.
        
        Args:
            conversation_id: The ID of the conversation
            
        Returns:
            Path to the workspace directory
        """
        return settings.WORKSPACE_DIR / conversation_id
    
    def _create_workspace(self, conversation_id: str) -> Path:
        """
        Create a workspace directory for a conversation.
        
        Args:
            conversation_id: The ID of the conversation
            
        Returns:
            Path to the workspace directory
        """
        workspace_path = self.get_workspace_path(conversation_id)
        os.makedirs(workspace_path, exist_ok=True)
        return workspace_path

# Create a singleton instance
conversation_manager = ConversationManager() 
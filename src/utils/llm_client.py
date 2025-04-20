from anthropic import Anthropic
from typing import List, Dict, Any, Optional
import os
import sys
from ..config import settings
from .tools import tool_registry

class ClaudeClient:
    """Client for Anthropic's Claude API."""
    
    def __init__(self):
        """Initialize Claude client with API key from settings."""
        if not settings.ANTHROPIC_API_KEY:
            print("ANTHROPIC_API_KEY not found in environment variables. Please add it to your .env file.", file=sys.stderr)
        
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL
        print(f"Initialized Claude client with model: {self.model}", file=sys.stderr)
    
    def create_message(self, messages: List[Dict[str, Any]], enable_tools: bool = True) -> Dict[str, Any]:
        """
        Create a message with Claude API.
        
        Args:
            messages: List of messages in the conversation
            enable_tools: Whether to enable tool usage
            
        Returns:
            The response from Claude API
        """
        try:
            # Prepare tools if enabled
            tools = None
            if enable_tools:
                tools = tool_registry.get_tool_definitions()
                if tools:
                    print(f"Enabling {len(tools)} tools for Claude", file=sys.stderr)
            
            # Create the message with tools if enabled
            response = self.client.messages.create(
                model=self.model,
                messages=messages,
                max_tokens=4000,
                temperature=0.7,
                tools=tools if tools else None
            )
            
            return response
        except Exception as e:
            print(f"Error creating message with Claude API: {e}", file=sys.stderr)
            raise
    
    def extract_tool_calls(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract tool calls from a Claude API response.
        
        Args:
            response: The response from Claude API
            
        Returns:
            List of tool calls extracted from the response
        """
        tool_calls = []
        
        # Check if response has content blocks
        if hasattr(response, 'content') and response.content:
            for block in response.content:
                # Check for tool calls in the content blocks
                if block.type == 'tool_use':
                    tool_call = {
                        'id': block.id,
                        'type': 'tool_call',
                        'tool': {
                            'name': block.name,
                            'description': tool_registry.get_tool(block.name).description,
                            'parameters': tool_registry.get_tool(block.name).parameters
                        },
                        'input': block.input
                    }
                    tool_calls.append(tool_call)
        
        return tool_calls

# Create a singleton instance
claude_client = ClaudeClient() 
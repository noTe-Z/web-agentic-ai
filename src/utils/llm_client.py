from anthropic import Anthropic
from typing import List, Dict, Any, Optional
import os
import sys
from ..config import settings

class ClaudeClient:
    """Client for Anthropic's Claude API."""
    
    def __init__(self):
        """Initialize Claude client with API key from settings."""
        if not settings.ANTHROPIC_API_KEY:
            print("ANTHROPIC_API_KEY not found in environment variables. Please add it to your .env file.", file=sys.stderr)
        
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL
        print(f"Initialized Claude client with model: {self.model}", file=sys.stderr)
    
    def create_message(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a message with Claude API.
        
        Args:
            messages: List of messages in the conversation
            
        Returns:
            The response from Claude API
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                messages=messages,
                max_tokens=4000,
                temperature=0.7
            )
            return response
        except Exception as e:
            print(f"Error creating message with Claude API: {e}", file=sys.stderr)
            raise

# Create a singleton instance
claude_client = ClaudeClient() 
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
from .base import BaseTool
from ...models.chat import ToolParameter
from ...core.conversation_manager import conversation_manager


class ReadFileTool(BaseTool):
    """Tool for reading files within the conversation workspace."""
    
    name = "read_file"
    description = "Read the contents of a file in the conversation workspace."
    
    @property
    def _get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="path",
                description="Path to the file to read, relative to the conversation workspace",
                required=True,
                type="string"
            )
        ]
    
    async def execute(self, conversation_id: str, input_data: Dict[str, Any]) -> Any:
        """
        Read a file from the conversation workspace.
        
        Args:
            conversation_id: The ID of the conversation
            input_data: Input parameters containing the file path
            
        Returns:
            The contents of the file as a string
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the path tries to access files outside the workspace
        """
        # Validate the input
        validation_error = self.validate_input(input_data)
        if validation_error:
            raise ValueError(validation_error)
        
        # Get the file path
        file_path = input_data["path"]
        
        # Get the workspace path
        workspace_path = conversation_manager.get_workspace_path(conversation_id)
        
        # Create the full path to the file
        full_path = workspace_path / file_path
        
        # Security check: Make sure the resolved path is within the workspace
        try:
            resolved_path = full_path.resolve()
            workspace_resolved = workspace_path.resolve()
            
            if not str(resolved_path).startswith(str(workspace_resolved)):
                raise ValueError(f"Access denied: Cannot access files outside the workspace")
        except Exception as e:
            raise ValueError(f"Invalid path: {str(e)}")
        
        # Check if the file exists
        if not resolved_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check if it's a file (not a directory)
        if not resolved_path.is_file():
            raise ValueError(f"Not a file: {file_path}")
        
        try:
            # Read the file
            with open(resolved_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            return content
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}", file=sys.stderr)
            raise


class SaveFileTool(BaseTool):
    """Tool for saving files within the conversation workspace."""
    
    name = "save_file"
    description = "Save a file to the conversation workspace."
    
    @property
    def _get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="path",
                description="Path to save the file to, relative to the conversation workspace",
                required=True,
                type="string"
            ),
            ToolParameter(
                name="content",
                description="Content to write to the file",
                required=True,
                type="string"
            )
        ]
    
    async def execute(self, conversation_id: str, input_data: Dict[str, Any]) -> Any:
        """
        Save a file to the conversation workspace.
        
        Args:
            conversation_id: The ID of the conversation
            input_data: Input parameters containing the file path and content
            
        Returns:
            Success message
            
        Raises:
            ValueError: If the path tries to access files outside the workspace
        """
        # Validate the input
        validation_error = self.validate_input(input_data)
        if validation_error:
            raise ValueError(validation_error)
        
        # Get the file path and content
        file_path = input_data["path"]
        content = input_data["content"]
        
        # Get the workspace path
        workspace_path = conversation_manager.get_workspace_path(conversation_id)
        
        # Create the full path to the file
        full_path = workspace_path / file_path
        
        # Security check: Make sure the resolved path is within the workspace
        try:
            # Create parent directories if they don't exist
            os.makedirs(full_path.parent, exist_ok=True)
            
            resolved_path = full_path.resolve()
            workspace_resolved = workspace_path.resolve()
            
            if not str(resolved_path).startswith(str(workspace_resolved)):
                raise ValueError(f"Access denied: Cannot access files outside the workspace")
        except Exception as e:
            raise ValueError(f"Invalid path: {str(e)}")
        
        try:
            # Write the file
            with open(resolved_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            return f"File saved successfully: {file_path}"
        except Exception as e:
            print(f"Error saving file {file_path}: {str(e)}", file=sys.stderr)
            raise 
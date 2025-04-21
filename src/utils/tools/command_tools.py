import os
import sys
import subprocess
import shlex
from typing import Dict, Any, List, Optional
from .base import BaseTool
from ...models.chat import ToolParameter
from ...core.conversation_manager import conversation_manager


class RunCommandTool(BaseTool):
    """Tool for running terminal commands within the conversation workspace."""
    
    name = "run_command"
    description = "Run a terminal command in the conversation workspace."
    
    # List of forbidden commands for security
    FORBIDDEN_COMMANDS = [
        "rm -rf",
        "sudo",
        "> /",
        "shutdown",
        "reboot",
        "format",
        "mkfs",
        "dd",
        "mv /*",
    ]
    
    # Max command execution time in seconds
    MAX_EXECUTION_TIME = 30
    
    def _get_parameters(self) -> List[ToolParameter]:
        """Define the parameters for this tool."""
        return [
            ToolParameter(
                name="command",
                description="Command to run",
                required=True,
                type="string"
            ),
            ToolParameter(
                name="timeout",
                description="Maximum execution time in seconds (default: 30)",
                required=False,
                type="integer"
            )
        ]
    
    def _validate_command(self, command: str) -> Optional[str]:
        """
        Validate a command for security issues.
        
        Args:
            command: The command to validate
            
        Returns:
            Error message if validation fails, None otherwise
        """
        # Check for forbidden commands
        for forbidden in self.FORBIDDEN_COMMANDS:
            if forbidden in command:
                return f"Forbidden command: {forbidden}"
        
        # Additional security checks can be added here
        
        return None
    
    async def execute(self, conversation_id: str, input_data: Dict[str, Any]) -> Any:
        """
        Run a command in the conversation workspace.
        
        Args:
            conversation_id: The ID of the conversation
            input_data: Input parameters containing the command
            
        Returns:
            Output of the command
            
        Raises:
            ValueError: If the command fails validation
            subprocess.SubprocessError: If the command execution fails
            TimeoutExpired: If the command times out
        """
        # Validate the input
        validation_error = self.validate_input(input_data)
        if validation_error:
            raise ValueError(validation_error)
        
        # Get the command
        command = input_data["command"]
        
        # Validate the command for security
        security_error = self._validate_command(command)
        if security_error:
            raise ValueError(security_error)
        
        # Get timeout value or use default
        timeout = input_data.get("timeout", self.MAX_EXECUTION_TIME)
        
        # Get the workspace path
        workspace_path = conversation_manager.get_workspace_path(conversation_id)
        
        print(f"Running command in workspace {workspace_path}: {command}", file=sys.stderr)
        
        try:
            # Run the command in the workspace directory
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=str(workspace_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for the command to complete with timeout
            stdout, stderr = process.communicate(timeout=timeout)
            
            # Create result dictionary
            result = {
                "exit_code": process.returncode,
                "stdout": stdout,
                "stderr": stderr
            }
            
            # Log the execution result
            print(f"Command execution completed (exit code: {process.returncode})", file=sys.stderr)
            
            # Save the command output as a file in the workspace for reference
            output_file = workspace_path / f"command_output_{conversation_id[:8]}.txt"
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"\n--- Command: {command} ---\n")
                f.write(f"Exit Code: {process.returncode}\n")
                f.write(f"--- STDOUT ---\n{stdout}\n")
                f.write(f"--- STDERR ---\n{stderr}\n")
            
            return result
            
        except subprocess.TimeoutExpired:
            print(f"Command timed out after {timeout} seconds: {command}", file=sys.stderr)
            return {
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds"
            }
        except Exception as e:
            print(f"Error running command: {str(e)}", file=sys.stderr)
            return {
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Error: {str(e)}"
            } 
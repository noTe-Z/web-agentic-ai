from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from ...models.chat import ToolParameter


class BaseTool(ABC):
    """Base class for all tools."""
    
    name: str
    description: str
    parameters: List[ToolParameter]
    
    def __init__(self):
        """Initialize the tool with parameters."""
        self.parameters = self._get_parameters()
    
    @abstractmethod
    def _get_parameters(self) -> List[ToolParameter]:
        """
        Define the parameters for this tool.
        
        Returns:
            List of ToolParameter objects
        """
        pass
    
    @abstractmethod
    async def execute(self, conversation_id: str, input_data: Dict[str, Any]) -> Any:
        """
        Execute the tool with the provided input.
        
        Args:
            conversation_id: The ID of the conversation
            input_data: Input parameters for the tool
            
        Returns:
            Result of the tool execution
        """
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the tool to a dictionary format for the API.
        
        Returns:
            Tool definition as a dictionary
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": [param.dict() for param in self.parameters]
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> Optional[str]:
        """
        Validate the input data against the tool's parameters.
        
        Args:
            input_data: Input parameters for the tool
            
        Returns:
            Error message if validation fails, None otherwise
        """
        # Check for required parameters
        for param in self.parameters:
            if param.required and param.name not in input_data:
                return f"Missing required parameter: {param.name}"
        
        # Additional validation can be added here
        
        return None 
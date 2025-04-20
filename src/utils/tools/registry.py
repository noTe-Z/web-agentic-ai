from typing import Dict, Type, List, Any
import sys
from .base import BaseTool


class ToolRegistry:
    """Registry for all available tools."""
    
    def __init__(self):
        """Initialize the tool registry."""
        self.tools: Dict[str, BaseTool] = {}
    
    def register_tool(self, tool_instance: BaseTool) -> None:
        """
        Register a tool in the registry.
        
        Args:
            tool_instance: Instance of the tool to register
        """
        self.tools[tool_instance.name] = tool_instance
        print(f"Registered tool: {tool_instance.name}", file=sys.stderr)
    
    def get_tool(self, tool_name: str) -> BaseTool:
        """
        Get a tool by name.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool instance
            
        Raises:
            ValueError: If tool is not found
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool not found: {tool_name}")
        
        return self.tools[tool_name]
    
    def get_all_tools(self) -> List[BaseTool]:
        """
        Get all registered tools.
        
        Returns:
            List of all registered tool instances
        """
        return list(self.tools.values())
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Get definitions for all tools in a format suitable for API responses.
        
        Returns:
            List of tool definitions
        """
        return [tool.to_dict() for tool in self.tools.values()]


# Create a singleton instance
tool_registry = ToolRegistry() 
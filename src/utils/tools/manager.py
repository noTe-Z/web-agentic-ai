import sys
from .registry import tool_registry
from .file_tools import ReadFileTool, SaveFileTool
from .command_tools import RunCommandTool


def initialize_tools():
    """Initialize and register all available tools."""
    print("Initializing tools...", file=sys.stderr)
    
    # Initialize and register file tools
    tool_registry.register_tool(ReadFileTool())
    tool_registry.register_tool(SaveFileTool())
    
    # Initialize and register command tools
    tool_registry.register_tool(RunCommandTool())
    
    print(f"Registered {len(tool_registry.get_all_tools())} tools", file=sys.stderr)


# Initialize tools at module import
initialize_tools() 
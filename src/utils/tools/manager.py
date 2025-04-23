import sys
from .registry import tool_registry
from .file_tools import ReadFileTool, SaveFileTool
from .command_tools import RunCommandTool
from .web_tools import WebSearchTool, ExtractContentTool


def initialize_tools():
    """Initialize and register all available tools."""
    print("Initializing tools...", file=sys.stderr)
    
    try:
        # Initialize and register file tools
        tool_registry.register_tool(ReadFileTool())
        tool_registry.register_tool(SaveFileTool())
        
        # Initialize and register command tools
        tool_registry.register_tool(RunCommandTool())
        
        # Initialize and register web tools
        tool_registry.register_tool(WebSearchTool())
        tool_registry.register_tool(ExtractContentTool())
        
        print(f"Registered {len(tool_registry.get_all_tools())} tools", file=sys.stderr)
    except Exception as e:
        print(f"ERROR initializing tools: {e}", file=sys.stderr)
        # Don't raise the exception to allow the application to continue
        # but log it for debugging


# Initialize tools at module import
try:
    initialize_tools()
except Exception as e:
    print(f"ERROR during tool initialization: {e}", file=sys.stderr) 
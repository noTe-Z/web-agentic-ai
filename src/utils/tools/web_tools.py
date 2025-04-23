import sys
import os
import asyncio
import subprocess
from typing import Dict, Any, List
from pathlib import Path
from .base import BaseTool
from ...models.chat import ToolParameter
from ...core.conversation_manager import conversation_manager


class WebSearchTool(BaseTool):
    """Tool for searching the web using DuckDuckGo."""
    
    name = "web_search"
    description = "Search the web for information using DuckDuckGo."
    
    def _get_parameters(self) -> List[ToolParameter]:
        """Define the parameters for this tool."""
        return [
            ToolParameter(
                name="query",
                description="The search query to look up on the web",
                required=True,
                type="string"
            ),
            ToolParameter(
                name="max_results",
                description="Maximum number of results to return (default: 10)",
                required=False,
                type="integer"
            )
        ]
    
    async def execute(self, conversation_id: str, input_data: Dict[str, Any]) -> Any:
        """
        Search the web using DuckDuckGo.
        
        Args:
            conversation_id: The ID of the conversation
            input_data: Input parameters containing the search query
            
        Returns:
            Search results as a formatted string
            
        Raises:
            ValueError: If the query is invalid
            Exception: If the search fails
        """
        # Validate the input
        validation_error = self.validate_input(input_data)
        if validation_error:
            raise ValueError(validation_error)
        
        # Get the search query
        query = input_data["query"]
        max_results = input_data.get("max_results", 10)
        
        # Validate max_results
        if not isinstance(max_results, int) or max_results <= 0:
            max_results = 10
        
        try:
            # Get the path to the search_engine.py script
            script_path = Path(os.path.abspath(__file__)).parent.parent.parent.parent / "tools" / "search_engine.py"
            
            if not script_path.exists():
                raise FileNotFoundError(f"Search engine script not found: {script_path}")
            
            # Prepare the command
            cmd = [
                sys.executable, 
                str(script_path), 
                query,
                "--max-results", str(max_results)
            ]
            
            # Execute the search script
            print(f"Executing search command: {' '.join(cmd)}", file=sys.stderr)
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Get output and error
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"Search command failed with error: {stderr}", file=sys.stderr)
                raise Exception(f"Search failed: {stderr}")
            
            # Parse the results
            results = stdout.strip()
            
            # Save the search results to a file in the conversation workspace
            workspace_path = conversation_manager.get_workspace_path(conversation_id)
            results_path = workspace_path / f"search_results_{query[:30].replace(' ', '_')}.txt"
            
            with open(results_path, "w", encoding="utf-8") as f:
                f.write(f"Search Query: {query}\n\n")
                f.write(results)
            
            return results
            
        except Exception as e:
            print(f"Error executing web search: {str(e)}", file=sys.stderr)
            raise


class ExtractContentTool(BaseTool):
    """Tool for extracting content from web pages."""
    
    name = "extract_content"
    description = "Extract and parse content from a website URL."
    
    def _get_parameters(self) -> List[ToolParameter]:
        """Define the parameters for this tool."""
        return [
            ToolParameter(
                name="url",
                description="URL of the web page to extract content from",
                required=True,
                type="string"
            )
        ]
    
    async def execute(self, conversation_id: str, input_data: Dict[str, Any]) -> Any:
        """
        Extract content from a web page.
        
        Args:
            conversation_id: The ID of the conversation
            input_data: Input parameters containing the URL
            
        Returns:
            Extracted content as a string
            
        Raises:
            ValueError: If the URL is invalid
            Exception: If the extraction fails
        """
        # Validate the input
        validation_error = self.validate_input(input_data)
        if validation_error:
            raise ValueError(validation_error)
        
        # Get the URL
        url = input_data["url"]
        
        try:
            # Get the path to the web_scraper.py script
            script_path = Path(os.path.abspath(__file__)).parent.parent.parent.parent / "tools" / "web_scraper.py"
            
            if not script_path.exists():
                raise FileNotFoundError(f"Web scraper script not found: {script_path}")
            
            # Prepare the command
            cmd = [
                sys.executable, 
                str(script_path),
                url
            ]
            
            # Execute the scraper script
            print(f"Executing scraper command: {' '.join(cmd)}", file=sys.stderr)
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Get output and error
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"Scraper command failed with error: {stderr}", file=sys.stderr)
                raise Exception(f"Content extraction failed: {stderr}")
            
            # Get the extracted content
            content = stdout.strip()
            
            # Save the extracted content to a file in the conversation workspace
            workspace_path = conversation_manager.get_workspace_path(conversation_id)
            
            # Extract domain for filename
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            safe_domain = ''.join(c if c.isalnum() else '_' for c in domain)
            
            content_path = workspace_path / f"extracted_content_{safe_domain}.txt"
            
            with open(content_path, "w", encoding="utf-8") as f:
                f.write(f"Extracted from URL: {url}\n\n")
                f.write(content)
            
            return content
            
        except Exception as e:
            print(f"Error extracting content: {str(e)}", file=sys.stderr)
            raise 
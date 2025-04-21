from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import sys
import os

from .api import chat
from .config import settings
from .utils import tool_registry  # Import tool registry to ensure tools are initialized
from .core import conversation_manager  # Import conversation manager to ensure it's initialized

# Create FastAPI app
app = FastAPI(
    title="Agentic AI Chat API",
    description="Backend API for Agentic AI Chat application",
    version="0.3.0",  # Updated version for Phase 3
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api", tags=["chat"])

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    print(f"Mounted static files from {static_dir}", file=sys.stderr)
else:
    print(f"Warning: Static directory not found at {static_dir}", file=sys.stderr)

# Serve the main HTML page
@app.get("/", tags=["frontend"])
async def get_index():
    """Serve the main HTML page."""
    from fastapi.responses import FileResponse
    index_path = os.path.join(static_dir, "templates", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        return {"error": "Index file not found. Make sure to create the frontend files."}

# Add health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "registered_tools": [tool.name for tool in tool_registry.get_all_tools()]
    }


def start():
    """Start the FastAPI application using uvicorn server."""
    print(f"Starting Agentic AI Chat API on {settings.API_HOST}:{settings.API_PORT}", file=sys.stderr)
    print(f"Available tools: {[tool.name for tool in tool_registry.get_all_tools()]}", file=sys.stderr)
    print(f"Frontend available at http://{settings.API_HOST}:{settings.API_PORT}/", file=sys.stderr)
    uvicorn.run(
        "src.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    start() 
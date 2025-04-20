from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys

from .api import chat
from .config import settings
from .utils import tool_registry  # Import tool registry to ensure tools are initialized
from .core import conversation_manager  # Import conversation manager to ensure it's initialized

# Create FastAPI app
app = FastAPI(
    title="Agentic AI Chat API",
    description="Backend API for Agentic AI Chat application",
    version="0.2.0",  # Updated version for Phase 2
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
    uvicorn.run(
        "src.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    start() 
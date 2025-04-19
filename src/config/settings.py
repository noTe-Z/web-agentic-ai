import os
from pathlib import Path
from dotenv import load_dotenv
import sys

def load_environment():
    """
    Load environment variables from .env files in order of precedence:
    1. System environment variables (already loaded)
    2. .env.local (user-specific overrides)
    3. .env (project defaults)
    4. .env.example (example configuration)
    """
    env_files = ['.env.local', '.env', '.env.example']
    env_loaded = False
    
    # Get the base project directory
    base_dir = Path(__file__).resolve().parent.parent
    
    print(f"Current working directory: {base_dir}", file=sys.stderr)
    print(f"Looking for environment files: {env_files}", file=sys.stderr)
    
    for env_file in env_files:
        env_path = base_dir / env_file
        print(f"Checking {env_path}", file=sys.stderr)
        if env_path.exists():
            print(f"Found {env_file}, loading variables...", file=sys.stderr)
            load_dotenv(dotenv_path=env_path)
            env_loaded = True
            print(f"Loaded environment variables from {env_file}", file=sys.stderr)
            # Print loaded keys (but not values for security)
            with open(env_path) as f:
                keys = [line.split('=')[0].strip() for line in f if '=' in line and not line.startswith('#')]
                print(f"Keys loaded from {env_file}: {keys}", file=sys.stderr)
    
    if not env_loaded:
        print("Warning: No .env files found. Using system environment variables only.", file=sys.stderr)

# Load environment variables at module import
load_environment()

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Claude API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-7-sonnet-20250219")

# Workspace Configuration
WORKSPACE_DIR = Path(os.getenv("WORKSPACE_DIR", "runs")).resolve()

# Ensure workspace directory exists
os.makedirs(WORKSPACE_DIR, exist_ok=True) 
# Agentic AI Chat

A web-based chat application where an AI assistant (Claude 3.7) can effectively utilize external tools to fulfill complex user requests.

## Project Structure

```
src/
├── api/               # API endpoints
├── config/            # Configuration
├── core/              # Core application components
├── models/            # Pydantic models
├── runs/              # Conversation workspaces
└── utils/
    └── tools/         # Tool implementations
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements_agentic.txt
```

4. Set up environment variables:
```bash
cp src/.env.example src/.env
```

5. Edit `src/.env` to add your Anthropic API key.

## Running the Application

```bash
python run.py
```

The API will be available at `http://localhost:8000`.

## API Endpoints

- `GET /health`: Health check endpoint
- `POST /api/chat`: Send a message to the AI assistant
- `POST /api/tool-results`: Provide results for tool calls

## Implemented Tools

The following tools are available for the AI assistant to use:

- **read_file**: Read the contents of a file in the workspace
- **save_file**: Save content to a file in the workspace
- **run_command**: Execute a shell command in the workspace

## Conversation Workspaces

Each conversation has its own workspace directory under `src/runs/` where files can be stored and commands can be executed. This provides isolation between different conversations.

## Tool Execution Flow

The application currently supports **manual tool execution**:

1. The user sends a message to the AI
2. The AI responds and may request tool executions
3. The frontend displays the tool requests to the user
4. The user provides the results of the tool executions
5. The results are sent to the AI, which continues the conversation

## Development

This project follows a phased approach:

- Phase 1: Project setup and backend foundation (completed)
- Phase 2: Core backend logic (current)
- Phase 3: Frontend implementation 
# Agentic AI Chat

A web-based chat application where an AI assistant (Claude 3.7) can effectively utilize external tools to fulfill complex user requests.

## Project Structure

```
src/
├── api/               # API endpoints
├── config/            # Configuration
├── models/            # Pydantic models
├── runs/              # Conversation workspaces
└── utils/             # Utility functions
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
- `POST /api/tool-results`: Provide results for tool calls (placeholder for future implementation)

## Development

This project follows a phased approach:

- Phase 1: Project setup and backend foundation (current)
- Phase 2: Core backend logic
- Phase 3: Frontend implementation 
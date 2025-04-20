## Product Requirements Document: Agentic AI Chat

**Version:** 1.1
**Date:** 2025-04-18

**1. Introduction & Goal**

* **Purpose:** This document outlines the requirements for building the "Agentic AI Chat" project.
* **Goal:** The primary goal is to **build an interactive web application** where an AI assistant (Claude 3.7) can effectively utilize external tools (like file system access, command execution, web search) to fulfill complex user requests within a chat interface. This involves developing both the frontend UI and the backend API infrastructure.

**2. Key Features**

The project will implement the following core features:

* **F1: Web-Based Chat Interface:** A frontend UI allowing users to interact with the AI assistant in a conversational manner.
* **F2: Backend API:** A FastAPI backend to manage conversations, interact with the AI model, and handle tool execution.
* **F3: Tool Integration Framework:** A system allowing the AI assistant to define and request the execution of predefined tools.
* **F4: Implemented Tools:**
    * **File Management:** Tools to read and write files within a designated workspace (`save_file`, `read_file`).
    * **Command Execution:** A tool to run terminal commands (`run_terminal_command`, `install_python_package`).
    * **Web Interaction:** Tools for web searching and content extraction (`web_search`, `extract_content`).
* **F5: Conversation Context:** Maintain conversation history and associate generated files/outputs with specific conversations.
* **F6: Tool Execution Flow:** Support both:
    * **Manual Execution:** Prompting the user (via frontend) to provide results for tool calls when needed or configured.
    * **Automatic Execution:** Backend automatically executes requested tools and continues the conversation, including handling sequences of tool calls.
* **F7: Conversation Workspace:** Each conversation will have an associated directory (e.g., within `runs/`) where generated files and command outputs are stored.
* **F8: File Serving & Preview:** Ability to serve files generated within a conversation workspace and provide basic previews (image, markdown, HTML) in the frontend.
* **F9: Auto-Execution Control:** Allow users to toggle auto-execution, cancel ongoing execution, and resume execution if paused (e.g., due to limits).

**3. Scope & Phasing (Initial Focus)**

To manage development, we will initially focus on building a Minimum Viable Product (MVP) encompassing the foundational elements:

* **Phase 1: Project Setup and Backend Foundation**
    * Environment setup (Python venv, core dependencies).
    * Basic FastAPI app structure.
    * Configuration management (.env).
    * Basic Pydantic models.
    * Anthropic client setup.
    * Basic `/api/chat` route forwarding messages to Claude.
* **Phase 2: Core Backend Logic**
    * In-memory conversation management (history, IDs).
    * Basic tool definition structure.
    * Implementation of `save_file`, `read_file`, `run_command`.
    * Integration of tool calls into the chat API response.
    * Implementation of the `/api/tool-results` endpoint for *manual* execution flow first.
    * *Defer* full auto-execution logic (background tasks, polling, cancel/resume) to a later stage.
* **Phase 3: Frontend Implementation**
    * Basic HTML structure and CSS.
    * Modular JS setup.
    * Displaying chat messages (user/assistant).
    * Sending user messages via the API.
    * Basic display of tool calls (name/input).
    * Basic display of tool results.

**4. Out of Initial Scope (Potential Future Phases)**

* Advanced frontend features (complex file previews, file browser).
* Full implementation and dependency setup for web tools (`search`, `extract_content`).
* Robust error handling and UI feedback across the application.
* Comprehensive testing suite (unit, integration).
* Deployment optimizations (Gunicorn, multi-worker stability).
* User authentication or multi-user support.
* Persistent conversation storage (e.g., database).

**5. Success Criteria (for MVP)**

* Successfully set up the project environment.
* Implement a functional chat interface connected to the Claude API via the FastAPI backend.
* Demonstrate the AI requesting at least one file tool and one command tool.
* Successfully provide results for tool calls manually via the frontend/API.
* Store conversation history correctly for the duration of a session.
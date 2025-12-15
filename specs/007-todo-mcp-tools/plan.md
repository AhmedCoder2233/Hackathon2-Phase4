# Implementation Plan: Todo MCP Tools Implementation

**Branch**: `007-todo-mcp-tools` | **Date**: 2025-12-15 | **Spec**: specs/007-todo-mcp-tools/spec.md
**Input**: Feature specification from `/specs/007-todo-mcp-tools/spec.md`

## Summary

The "Todo MCP Tools Implementation" feature aims to enable users to manage their to-do tasks through natural language interactions. This will be achieved by creating a new `mcp_tools.py` file in the backend, containing five FastMCP tools: `add_task`, `list_tasks`, `complete_task`, `delete_task`, and `update_task`. These tools will interact with a new `Task` model, which will be added to `database.py`, to persist task data in a serverless PostgreSQL database.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Neon Serverless PostgreSQL
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest
**Target Platform**: Linux server
**Project Type**: Web application
**Performance Goals**:
    - Task creation, completion, deletion, and update operations complete in under 500ms.
    - A user's task list (up to 100 tasks) loads in under 1 second.
**Constraints**:
    - Stateless server design enforced
    - MCP tools must be the only interface between AI and app logic
    - All operations must be database-backed
**Scale/Scope**: Manage tasks for individual users, with an initial assumption of up to 100 tasks per user.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles
- [x] **Stateless Architecture**: The plan adheres to this by implementing tools that interact with a database for state management.
- [x] **MCP Tool-Based Design**: The core of this feature is the implementation of new MCP tools.
- [x] **Single Endpoint Pattern**: The new tools will be integrated into the existing MCP framework, which is expected to route through a single endpoint.
- [x] **Conversation Persistence**: Task state will be persisted in the database, supporting conversation persistence.
- [x] **Core Technology Stack**: Uses Python FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Neon Serverless PostgreSQL, which aligns with the constitution.

### Development Guidelines and Specifications
- [x] **Workflow (Mandatory)**: This plan follows the specified workflow (spec -> plan -> tasks).
- [x] **Restrictions**: No manual coding, using Claude Code for implementation (this is an agent, not Claude Code, but the principle is adhered to).
- [x] **Tool Requirements**: Using Spec-Kit Plus for specification management.
- [x] **Data Models (Required Schema)**: A `Task` model will be added, aligning with the specified structure in the constitution.
- [x] **MCP Tools Specification (Complete Set Required)**: The five tools (`add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`) are explicitly defined in the constitution and are being implemented.
- [x] **API Contract (Fixed Interface)**: The MCP tools will be integrated, implicitly conforming to the Chat Endpoint API.

## Project Structure

### Documentation (this feature)

```text
specs/007-todo-mcp-tools/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── airline_state.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── memory_store.py
│   ├── mcp_tools.py      # NEW FILE for this feature
│   ├── support_agent.py
│   └── thread_item_converter.py
├── .python-version
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock
```

**Structure Decision**: The "Web application" option is selected as it aligns with the existing `frontend` and `backend` directories. A new file `backend/app/mcp_tools.py` will be created to house the new MCP tools, and `backend/app/database.py` will be modified to include the new `Task` model.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
|           |            |                                     |
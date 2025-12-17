# Implementation Plan: Integrate MCP Server with OpenAI Agent

**Branch**: `008-mcp-client` | **Date**: 2025-12-15 | **Spec**: specs/008-mcp-client/spec.md
**Input**: Feature specification from `/specs/008-mcp-client/spec.md`

## Summary

This feature integrates the existing MCP (Micro-Agent Control Plane) server, which provides todo management tools, with the OpenAI Agents SDK within the application's support agent. The integration will allow users to manage their todo tasks through natural language conversations with an AI assistant, leveraging user authentication for task ownership.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, FastMCP
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest
**Target Platform**: Linux server
**Project Type**: Web application
**Performance Goals**:
    - MCP tool calls (including tool execution time) under 3 seconds for 90% of requests
**Constraints**:
    - MCP server running at `http://localhost:8001/mcp/`
    - `user_id` from Better Auth MUST be passed to all MCP tools
    - Users can only interact with tasks associated with their `user_id`
**Scale/Scope**: Manage tasks for individual users, allowing natural language interaction with todo tools.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles
- [x] **Stateless Architecture**: The plan adheres to this by integrating MCP tools that interact with a backend server, which in turn manages state in a database. The agent itself will be stateless, relying on the `user_id` from the context for all operations.
- [x] **MCP Tool-Based Design**: The core of this feature is the integration and utilization of MCP tools.
- [x] **Single Endpoint Pattern**: This feature leverages the existing chat endpoint in `main.py` where the agent will be integrated.
- [x] **Conversation Persistence**: The agent relies on the `chat_history` passed in the context from `main.py`, which is fetched from the database, ensuring persistence.
- [x] **Core Technology Stack**: Uses Python FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Neon Serverless PostgreSQL, which aligns with the constitution.

### Development Guidelines and Specifications
- [x] **Workflow (Mandatory)**: This plan follows the specified workflow (spec -> plan -> tasks).
- [x] **Restrictions**: No manual coding, using Claude Code for implementation (this is an agent, not Claude Code, but the principle is adhered to).
- [x] **Tool Requirements**: Using Spec-Kit Plus for specification management.
- [x] **Data Models (Required Schema)**: The MCP tools interact with the `Task` model, which aligns with the data models defined in the constitution.
- [x] **MCP Tools Specification (Complete Set Required)**: The five todo tools (`add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`) are explicitly defined in the constitution and are being integrated.
- [x] **API Contract (Fixed Interface)**: The MCP tools will be integrated through the agent, implicitly conforming to the Chat Endpoint API.

## Project Structure

### Documentation (this feature)

```text
specs/008-mcp-client/
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
│   ├── support_agent.py      # MODIFIED for this feature
│   ├── main.py               # MODIFIED for this feature
│   └── ...
└── ...

frontend/
└── ...
```

**Structure Decision**: The "Web application" option is selected as it aligns with the existing `frontend` and `backend` directories. `backend/app/support_agent.py` and `backend/app/main.py` will be modified.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

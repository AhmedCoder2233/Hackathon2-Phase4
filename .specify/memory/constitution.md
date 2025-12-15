<!--
Sync Impact Report:
- Version change: 0.0.0 (initial template) -> 1.0.0
- List of modified principles:
    - [PRINCIPLE_1_NAME] -> Stateless Architecture
    - [PRINCIPLE_2_NAME] -> MCP Tool-Based Design
    - [PRINCIPLE_3_NAME] -> Single Endpoint Pattern
    - [PRINCIPLE_4_NAME] -> Conversation Persistence
    - [PRINCIPLE_5_NAME] -> Core Technology Stack
- Added sections: Development Guidelines and Specifications, Operational and Quality Requirements
- Removed sections: N/A (template placeholders were filled/removed)
- Templates requiring updates:
    - .specify/templates/plan-template.md: ⚠ pending
    - .specify/templates/spec-template.md: ⚠ pending
    - .specify/templates/tasks-template.md: ⚠ pending
    - .specify/templates/commands/*.md: ⚠ pending
- Follow-up TODOs: N/A
-->
# Todo AI Chatbot Constitution

## Core Principles

### Stateless Architecture
- Server maintains NO in-memory state
- All state persists in database
- Each request is independent and reproducible
- Horizontally scalable by design

### MCP Tool-Based Design
- AI agent interacts with app exclusively through MCP tools
- Standardized tool interface required
- Tools must be stateless and database-backed

### Single Endpoint Pattern
- One chat endpoint: `POST /api/{user_id}/chat`
- All AI routing handled internally
- Simpler API surface

### Conversation Persistence
- All messages stored in database
- Conversation history fetched per request
- No session state on server
- Resume conversations after server restart

### Core Technology Stack
### Frontend
- Framework: OpenAI ChatKit
- Deployment: Vercel/GitHub Pages with domain allowlist configuration

### Backend
- Framework: Python FastAPI
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth

## Development Guidelines and Specifications

### Development Constraints

### Workflow (Mandatory)
1. Write specification
2. Generate plan
3. Break into tasks
4. Implement via Claude Code

### Restrictions
- **NO manual coding allowed**
- Must use Claude Code for all implementation
- Process, prompts, and iterations will be reviewed

### Tool Requirements
- Claude Code (primary development tool)
- Spec-Kit Plus (specification management)

### Data Models (Required Schema)

### Task Model
```
- user_id: string (required)
- id: integer (primary key)
- title: string (required)
- description: string (optional)
- completed: boolean (default: false)
- created_at: timestamp
- updated_at: timestamp
```

### Conversation Model
```
- user_id: string (required)
- id: integer (primary key)
- created_at: timestamp
- updated_at: timestamp
```

### Message Model
```
- user_id: string (required)
- id: integer (primary key)
- conversation_id: integer (foreign key)
- role: enum (user/assistant)
- content: string
- created_at: timestamp
```

### MCP Tools Specification (Complete Set Required)

### 1. add_task
- **Purpose**: Create a new task
- **Parameters**: user_id (string, required), title (string, required), description (string, optional)
- **Returns**: task_id, status, title

### 2. list_tasks
- **Purpose**: Retrieve tasks from the list
- **Parameters**: user_id (string, required), status (string, optional: "all", "pending", "completed")
- **Returns**: Array of task objects

### 3. complete_task
- **Purpose**: Mark a task as complete
- **Parameters**: user_id (string, required), task_id (integer, required)
- **Returns**: task_id, status, title

### 4. delete_task
- **Purpose**: Remove a task from the list
- **Parameters**: user_id (string, required), task_id (integer, required)
- **Returns**: task_id, status, title

### 5. update_task
- **Purpose**: Modify task title or description
- **Parameters**: user_id (string, required), task_id (integer, required), title (string, optional), description (string, optional)
- **Returns**: task_id, status, title

## API Contract (Fixed Interface)

### Chat Endpoint
- **Method**: POST
- **Path**: `/api/{user_id}/chat`
- **Request Body**:
  - `conversation_id` (integer, optional) - Creates new if not provided
  - `message` (string, required) - User's natural language message
- **Response Body**:
  - `conversation_id` (integer) - The conversation ID
  - `response` (string) - AI assistant's response
  - `tool_calls` (array) - List of MCP tools invoked

## Agent Behavior Requirements

### Natural Language Understanding
Must recognize and respond to:
- Task creation phrases: "add", "create", "remember"
- Task listing phrases: "show", "list", "what's pending"
- Task completion phrases: "done", "complete", "finished"
- Task deletion phrases: "delete", "remove", "cancel"
- Task update phrases: "change", "update", "rename"

### Response Patterns
- Always confirm actions with friendly response
- Gracefully handle errors (task not found, etc.)
- Provide context-aware suggestions

## Operational and Quality Requirements

### Request Cycle (Stateless Flow)

1. Receive user message
2. Fetch conversation history from database
3. Build message array for agent (history + new message)
4. Store user message in database
5. Run agent with MCP tools
6. Agent invokes appropriate MCP tool(s)
7. Store assistant response in database
8. Return response to client
9. Server ready for next request (no retained state)

### Deployment Requirements

### Frontend Configuration
- OpenAI domain allowlist configuration required
- Domain key must be obtained and configured
- Environment variable: `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`

### Database Setup
- Migration scripts required
- Must support Neon Serverless PostgreSQL
- Connection pooling configuration

### Quality Gates (Deliverables Checklist)

### Repository Structure
```
/frontend - ChatKit-based UI
/backend - FastAPI + Agents SDK + MCP
/specs - Specification files for agent and MCP tools
/migrations - Database migration scripts
README.md - Setup instructions
```

### Functional Requirements
- ✓ Manage tasks through natural language via MCP tools
- ✓ Maintain conversation context via database (stateless server)
- ✓ Provide helpful responses with action confirmations
- ✓ Handle errors gracefully
- ✓ Resume conversations after server restart

### Documentation Requirements
- Setup instructions in README
- API documentation
- MCP tool specifications
- Deployment guide with domain allowlist steps

## Scalability Benefits (Architecture Goals)

- **Horizontal Scaling**: Load balancer can route to any backend instance
- **Resilience**: Server restarts don't lose conversation state
- **Testability**: Each request is independent and reproducible
- **Tool Composition**: Agent can chain multiple tools in one turn

## Non-Functional Requirements

- All operations must be database-backed
- No localStorage or sessionStorage usage
- Stateless server design enforced
- MCP tools must be the only interface between AI and app logic
- Error handling must be comprehensive

## Governance
This constitution defines the immutable boundaries of the project. Any deviation from these rules requires explicit justification and documentation.

**Version**: 1.0.0 | **Ratified**: 2025-12-13 | **Last Amended**: 2025-12-13
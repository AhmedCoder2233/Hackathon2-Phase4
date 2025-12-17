# Tasks for Integrate MCP Server with OpenAI Agent

## Feature Branch: `008-mcp-client`

## Implementation Strategy:

This implementation will follow an MVP-first approach, prioritizing the core integration with the MCP server and ensuring secure user context passing.

## Dependencies

- User Story 1: Integrate Agent into Main Application (P1) depends on Foundational - MCP Client Setup in Support Agent (P0)

## Parallel Execution Opportunities:

Not explicitly noted for these integration tasks, as they primarily involve sequential modifications to specific files.

---

## Phase 1: Setup

### Goal: Prepare the environment for the MCP Client integration.

-   [X] T001 Ensure `backend/app/support_agent.py` and `backend/app/main.py` are accessible and modifiable.

---

## Phase 2: Foundational - MCP Client Setup in Support Agent

### Goal: Implement the `create_todo_agent` function to connect to the MCP server.

### Independent Test Criteria:
The `create_todo_agent` function can be successfully imported and executed, returning an agent configured with the MCP client.

### Implementation Tasks:
-   [X] T002 Add imports `from agents import Agent`, `from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams` to `backend/app/support_agent.py`.
-   [X] T003 Define `MCP_SERVER_URL = "http://localhost:8001/mcp/"` in `backend/app/support_agent.py`.
-   [X] T004 Implement `async def create_todo_agent(user_id: str)` function in `backend/app/support_agent.py` as described in the spec.
-   [X] T005 Ensure the `Agent` created in `create_todo_agent` includes the `user_id` in its instructions for all tool calls.

---

## Phase 3: User Story 1 - Integrate Agent into Main Application

### Goal: Modify `backend/app/main.py` to use the new `todo_agent` for processing user messages.

### Independent Test Criteria:
The FastAPI application successfully uses the new `todo_agent` for user messages, correctly extracting the `user_id` and making MCP tool calls.

### Implementation Tasks:
-   [X] T006 Add import `from app.support_agent import create_todo_agent` to `backend/app/main.py`.
-   [X] T007 In `CustomerSupportServer.respond`, extract `user_id` from `context`.
-   [X] T008 In `CustomerSupportServer.respond`, call `create_todo_agent(user_id)` to get `todo_agent` and `mcp_client`.
-   [X] T009 In `CustomerSupportServer.respond`, replace `self.agent` with `todo_agent` in `Runner.run_streamed` call.
-   [X] T010 In `CustomerSupportServer.respond`, add cleanup for `mcp_client` using `await mcp_client.__aexit__(None, None, None)` after streaming the response.

---

## Final Phase: Polish & Cross-Cutting Concerns

### Goal: Ensure overall system quality and readiness.

### Implementation Tasks:
-   [X] T011 Update `GEMINI.md` to include instructions for starting the MCP server and FastAPI application for testing.
-   [X] T012 Verify secure passing of `user_id` to all MCP tool calls.
-   [X] T013 Verify error handling for MCP server unreachability or tool failures.

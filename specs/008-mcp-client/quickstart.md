# Quickstart Guide: Integrate MCP Server with OpenAI Agent

This guide provides a quick overview to get started with the MCP Server integration with the OpenAI Agent.

## Overview

This feature integrates the existing MCP (Micro-Agent Control Plane) server, which provides todo management tools, with the OpenAI Agents SDK within the application's support agent. This allows users to manage their todo tasks through natural language commands via the AI agent.

## Integration Details

-   **MCP Server URL**: `http://localhost:8001/mcp/`
-   **Files Modified**:
    -   `backend/app/support_agent.py`: Will include a new `create_todo_agent` function responsible for setting up the OpenAI Agent with the MCP client.
    -   `backend/app/main.py`: The `respond` function within the `CustomerSupportServer` class will be modified to extract the `user_id` from the context, create a user-specific `todo_agent` using `create_todo_agent`, and use this agent for processing user messages.
-   **Security**: All MCP tool calls will include the authenticated `user_id` to ensure tasks are managed securely and are scoped to the correct user.

## Usage

Once integrated, the AI agent will automatically detect and utilize the MCP todo tools when appropriate natural language commands are issued.

**Example Natural Language Commands**:

-   "Add 'finish report' to my todo list."
-   "Show me my pending tasks."
-   "I completed task 123."
-   "Delete task 456."
-   "Update task 789 to 'buy groceries and milk'."

## Next Steps

-   **Implement `create_todo_agent`**: Add the `create_todo_agent` function in `backend/app/support_agent.py`.
-   **Modify `respond` function**: Update the `respond` function in `backend/app/main.py` to use the `todo_agent`.
-   **Test**: Verify the integration by interacting with the AI agent using natural language commands for todo management.
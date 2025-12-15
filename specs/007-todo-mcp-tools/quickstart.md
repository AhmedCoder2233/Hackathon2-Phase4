# Quickstart Guide: Todo MCP Tools Implementation

This guide provides a quick overview to get started with the new Todo MCP Tools.

## Overview
This feature introduces a set of FastMCP tools that allow users to manage their to-do lists through natural language commands via the AI agent.

## Tools Provided

The following Micro-Agent tools are now available:

1.  **`add_task(user_id: str, title: str, description: str = "") -> dict`**
    *   **Purpose**: Creates a new task for a specified user.
    *   **Example Natural Language**: "Add 'buy groceries' to my tasks.", "Remind me to call mom, it's important."

2.  **`list_tasks(user_id: str, status: str = "all") -> dict`**
    *   **Purpose**: Retrieves a list of tasks for a specified user, with optional filtering by status.
    *   **Example Natural Language**: "List all my tasks.", "Show me my pending tasks.", "What have I completed?"

3.  **`complete_task(user_id: str, task_id: int) -> dict`**
    *   **Purpose**: Marks an existing task as completed.
    *   **Example Natural Language**: "I've completed task 123.", "Mark 'finish report' as done."

4.  **`delete_task(user_id: str, task_id: int) -> dict`**
    *   **Purpose**: Deletes a task from the user's list.
    *   **Example Natural Language**: "Delete task 456.", "Remove 'old reminder'."

5.  **`update_task(user_id: str, task_id: int, title: str = None, description: str = None) -> dict`**
    *   **Purpose**: Modifies the title or description of an existing task.
    *   **Example Natural Language**: "Update task 789 to 'buy milk and bread'.", "Change the description of task 101 to 'weekly team sync'."

## Database Setup

A new `Task` model has been introduced to the database. Ensure your database schema is up-to-date by running the necessary migrations.

## Integration with AI Agent

The AI agent will automatically detect and utilize these tools when appropriate natural language commands are issued. Ensure the MCP server is correctly configured to expose these tools.

## Next Steps

-   **Implement the `Task` model**: Add the `Task` class to `backend/app/database.py`.
-   **Develop `mcp_tools.py`**: Create `backend/app/mcp_tools.py` and implement the five FastMCP tools.
-   **Integrate**: Ensure the FastMCP instance is registered and accessible by the AI agent.
-   **Test**: Verify each tool's functionality and natural language interaction.

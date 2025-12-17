from __future__ import annotations

from datetime import datetime
from typing import Dict

from agents import Agent, RunContextWrapper, StopAtTools, function_tool, tool
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams
from chatkit.agents import AgentContext
from chatkit.types import AssistantMessageContent, AssistantMessageItem, ThreadItemDoneEvent

from .airline_state import AirlineStateManager
from dotenv import load_dotenv
import os

load_dotenv()

print("🔑 OpenAI API Key:", os.getenv("OPENAI_API_KEY")[:20] + "..." if os.getenv("OPENAI_API_KEY") else "NOT FOUND")

MCP_SERVER_URL = "http://localhost:8080/mcp/"

SUPPORT_AGENT_INSTRUCTIONS = """
You are a helpful Todo Management Assistant. You help users manage their tasks efficiently and provide clear, friendly responses.
""".strip()

async def create_todo_agent(user_id: str):
    """
    Create an agent connected to the MCP todo server for a specific user.
    Args:
        user_id: The Better Auth user ID (from current_user.id)
    Returns:
        tuple: (agent, mcp_client) - Keep both to maintain connection
    """
    # Configure MCP server parameters - NO TIMEOUT for stateless servers
    # Stateless servers don't maintain sessions, so each request is independent
    mcp_params = MCPServerStreamableHttpParams(
    url=MCP_SERVER_URL,
    timeout=30.0,
    sse_read_timeout=300.0,
)
    
    # Create MCP client connection
    server = MCPServerStreamableHttp(params=mcp_params, name="TodoMCPServer", max_retry_attempts=3,client_session_timeout_seconds=50,  # Retry up to 3 times
    retry_backoff_seconds_base=1.0,)
    
    # Connect manually
    try:
        await server.connect()
        print(f"✅ MCP client connected for user: {user_id}")
    except Exception as e:
        print(f"❌ Failed to connect MCP client: {e}")
        raise


    # Create agent with MCP tools
    agent = Agent(
        name="Todo Assistant",
        model="gpt-4o-mini",
        mcp_servers=[server],
        instructions=f"""
You are a helpful Todo Management Assistant. You help users manage their tasks.

**CRITICAL SECURITY RULE: For ALL tool calls, you MUST pass user_id as: "{user_id}"**

## Available Tools:
1. **add_task**(user_id, title, description) - Create new task
2. **list_tasks**(user_id, status) - List tasks (status: "all", "pending", "completed")
3. **complete_task**(user_id, task_id) - Mark task complete
4. **delete_task**(user_id, task_id) - Delete task
5. **update_task**(user_id, task_id, title, description) - Update task

## Response Guidelines:

### When Creating Tasks:
- Always confirm what was created
- Example: "✅ I've added 'Buy groceries' to your todo list with the description 'milk, bread, eggs'"

### When Listing Tasks:
- Format clearly with task IDs
- Show completion status
- Example:
  ```
  Here are your tasks:
  
  📋 Pending:
  1. [ID: 5] Buy groceries - milk, bread, eggs
  2. [ID: 6] AI Humanoid & Robotics Book - hackathon project
  
  ✅ Completed:
  3. [ID: 3] Study Python - completed
  ```

### When Completing Tasks:
- Celebrate the accomplishment
- Example: "🎉 Great job! Marked 'Buy groceries' as completed."

### When Deleting Tasks:
- Confirm what was deleted
- Example: "🗑️ Removed 'Old task' from your list."

### When Updating Tasks:
- Show what changed
- Example: "✏️ Updated task title from 'Old' to 'New Title'"

### Error Handling:
- If task not found: "I couldn't find that task. Would you like to see all your tasks?"
- If operation fails: "Something went wrong. Let me try again or you can rephrase your request."

## Natural Language Understanding:
- "add", "create", "new", "remember", "I need to" → add_task
- "show", "list", "what", "view", "my tasks" → list_tasks
- "done", "complete", "finished", "mark" → complete_task
- "delete", "remove", "cancel" → delete_task
- "change", "update", "edit", "rename" → update_task

## Important Rules:
1. Always use user_id="{user_id}" in EVERY tool call
2. Extract task details from natural language
3. Provide helpful, friendly responses
4. Format lists clearly
5. Handle errors gracefully
6. Confirm actions taken

**SECURITY: Never use a different user_id than "{user_id}"**
"""
    )
    return agent, server


def build_support_agent(state_manager: AirlineStateManager) -> Agent[AgentContext]:
    """Create the airline customer support agent with task-specific tools."""

    def _thread_id(ctx: RunContextWrapper[AgentContext]) -> str:
        return ctx.context.thread.id

    return Agent[AgentContext](
        model="gpt-4o-mini",
        name="OpenSkies Concierge",
        instructions=SUPPORT_AGENT_INSTRUCTIONS,
    )


state_manager = AirlineStateManager()
support_agent = build_support_agent(state_manager)
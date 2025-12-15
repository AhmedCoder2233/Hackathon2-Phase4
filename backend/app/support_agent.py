from __future__ import annotations

from datetime import datetime
from typing import Dict

from agents import Agent, RunContextWrapper, StopAtTools, function_tool
from chatkit.agents import AgentContext
from chatkit.types import AssistantMessageContent, AssistantMessageItem, ThreadItemDoneEvent

from .airline_state import AirlineStateManager
from dotenv import load_dotenv

load_dotenv()

SUPPORT_AGENT_INSTRUCTIONS = """
You are a helpful assistant
""".strip()


def build_support_agent(state_manager: AirlineStateManager) -> Agent[AgentContext]:
    """Create the airline customer support agent with task-specific tools."""

    def _thread_id(ctx: RunContextWrapper[AgentContext]) -> str:
        return ctx.context.thread.id

    return Agent[AgentContext](
        model="gpt-4.1-mini",
        name="OpenSkies Concierge",
        instructions=SUPPORT_AGENT_INSTRUCTIONS,
    )


state_manager = AirlineStateManager()
support_agent = build_support_agent(state_manager)

"""
==============================================================
Day 15 - Production Multi-Agent
Step 8: Production Callbacks

Features:
- Agent start/end logging
- Tool start/end logging
- Tool execution timing
- Cache visibility
- Error logging

Benefits:
- Centralized observability
- Clean agent code
- Production monitoring
==============================================================
"""

import time
from google.adk.agents.context import Context

from .logger import get_logger

logger = get_logger("callbacks")

# ---------------------------------------------------------
# Agent callbacks
# ---------------------------------------------------------

async def before_agent(callback_context: Context):
    """
    Called before an agent starts execution.
    """

    callback_context.state["agent_start_time"] = time.perf_counter()

    logger.info("Agent started")

    return None


async def after_agent(callback_context: Context):
    """
    Called after an agent finishes execution.
    """

    start = callback_context.state.get("agent_start_time")

    duration = 0.0

    if start is not None:
        duration = round(
            time.perf_counter() - start,
            2,
        )

    logger.info(
        f"Agent completed in {duration} sec"
    )

    return None


# ---------------------------------------------------------
# Tool callbacks
# ---------------------------------------------------------

async def before_tool(
    tool,
    args,
    tool_context,
):
    """
    Called before a tool is executed.
    """

    tool_context.state["tool_start_time"] = time.perf_counter()

    logger.info(
        f"Tool started: {tool.name} | args={args}"
    )

    return None


async def after_tool(
    tool,
    args,
    tool_context,
    tool_response,
):
    """
    Called after a tool finishes execution.
    """

    start = tool_context.state.get("tool_start_time")

    duration = 0.0

    if start is not None:
        duration = round(
            time.perf_counter() - start,
            2,
        )

    logger.info(
        f"Tool completed: {tool.name} in {duration} sec"
    )

    # Detect cache hit from tool response
    if isinstance(tool_response, dict):

        if tool_response.get("cache_hit"):
            logger.info(f"Cache HIT: {tool.name}")
        else:
            logger.info(f"Cache MISS: {tool.name}")

    return None


# ---------------------------------------------------------
# Tool error callback
# ---------------------------------------------------------

async def on_tool_error(
    tool,
    args,
    tool_context,
    error,
):
    """
    Called when a tool raises an exception.
    """

    logger.error(
        f"Tool failed: {tool.name} | error={error}"
    )

    return None
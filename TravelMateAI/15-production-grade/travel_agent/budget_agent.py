from google.adk.agents import Agent
from google.adk.models import LiteLlm
from .config import Settings
from .tools import estimate_budget

from .callbacks import (
    before_agent,
    after_agent,
    before_tool,
    after_tool,
    on_tool_error,
)

budget_agent = Agent(
    name="BudgetAgent",
    model=LiteLlm(model=Settings.MODEL_NAME),
    instruction="""
    You are a travel budget specialist.

    Always use the estimate_budget tool.

    Return only the estimated budget.
    """,
    tools=[estimate_budget],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
    before_tool_callback=before_tool,
    after_tool_callback=after_tool,
    on_tool_error_callback=on_tool_error,
)
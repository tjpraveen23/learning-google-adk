from google.adk.agents import Agent
from google.adk.models import LiteLlm

from .config import Settings
from .tools import get_hotel_price_range

from .callbacks import (
    before_agent,
    after_agent,
    before_tool,
    after_tool,
    on_tool_error,
)

hotel_agent = Agent(
    name="HotelAgent",
    model=LiteLlm(model=Settings.MODEL_NAME),
    instruction="""
    You are a hotel specialist.

    Always use the get_hotel_price_range tool.

    Return only the hotel recommendation.
    """,
    tools=[get_hotel_price_range],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,

    before_tool_callback=before_tool,
    after_tool_callback=after_tool,
    on_tool_error_callback=on_tool_error,
)
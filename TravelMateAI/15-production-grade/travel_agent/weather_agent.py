from google.adk.agents import Agent
from google.adk.models import LiteLlm

from .config import Settings
from .tools import get_weather

from .callbacks import (
    before_agent,
    after_agent,
    before_tool,
    after_tool,
    on_tool_error,
)

weather_agent = Agent(
    name="WeatherAgent",
    model=LiteLlm(model=Settings.MODEL_NAME),
    instruction="""
    You are a weather specialist.

    Always use the get_weather tool.

    Return only the weather result.
    """,
    tools=[get_weather],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,

    before_tool_callback=before_tool,
    after_tool_callback=after_tool,
    on_tool_error_callback=on_tool_error,
)
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
    Rules:
    1. Always use the get_weather tool.
    2. Call the tool exactly once.
    3. Pass only one argument: city.
    4. The city must be a plain city name (for example: Goa, Chennai, Bangalore, Mumbai).
    5. Do not write XML tags, JSON, markdown, or any function syntax yourself.
    6. After the tool returns, respond with only the weather result.
    7. If city is not available then send polite message as not available
    """,
    tools=[get_weather],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,

    before_tool_callback=before_tool,
    after_tool_callback=after_tool,
    on_tool_error_callback=on_tool_error,
)
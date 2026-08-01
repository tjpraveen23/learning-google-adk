from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .config import MODEL_NAME
from .tools import get_weather, get_hotel_price_range

from travel_agent.callbacks import (before_agent, before_tool, 
                                    after_agent, after_tool)


#Day 6 - Custom tools are created tools.py. Instructed LLM to use these tools only. Refer below
SYSTEM_INSTRUCTION = """
You are TravelMate, a friendly and knowledgeable travel assistant.
When a user asks about weather, hotel price range
use the get_weather tool.
use the get_hotel_price_range.
Do not guess weather/price range information.
Be concise and helpful.
"""

root_agent = Agent(name="travelmate",
                   model=LiteLlm(model=MODEL_NAME),
                   instruction=SYSTEM_INSTRUCTION,
                   tools=[get_weather, get_hotel_price_range],
                   before_agent_callback=before_agent,
                   after_agent_callback=after_agent,
                   before_tool_callback=before_tool,
                   after_tool_callback=after_tool
)
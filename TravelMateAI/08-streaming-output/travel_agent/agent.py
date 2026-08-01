from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .config import MODEL_NAME
from .tools import get_weather, get_hotel_price_range

#Day 8 - Streaming the output
SYSTEM_INSTRUCTION = """
You are TravelMate, a friendly and knowledgeable travel assistant.
When a user asks about weather, hotel price range
use the get_weather tool.
use the get_hotel_price_range.
Do not guess weather/price range information.
Be concise and helpful.
"""

root_agent = Agent(
    name="travelmate",
    model=LiteLlm(model=MODEL_NAME),
    instruction=SYSTEM_INSTRUCTION,
    tools=[get_weather,get_hotel_price_range]
)
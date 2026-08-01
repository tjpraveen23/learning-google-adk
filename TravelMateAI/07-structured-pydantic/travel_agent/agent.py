from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .config import MODEL_NAME
from .tools import get_weather, get_hotel_price_range
from .models import TravelPlan

#Day 7 - Always provide structured ouput using pydantic. Refer models.py
SYSTEM_INSTRUCTION = """
You are TravelMate, a friendly and knowledgeable travel assistant.
Always return a valid structured TravelPlan.
"""

root_agent = Agent(name="travelmate",
                   model=LiteLlm(model=MODEL_NAME),
                   instruction=SYSTEM_INSTRUCTION,
                   output_schema=TravelPlan   #Define the output schema format with custom python class
)
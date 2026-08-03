from google.adk.agents import Agent
from google.adk.models import LiteLlm
from .config import Settings

from .callbacks import (
    before_agent,
    after_agent,
)


coordinator_agent = Agent(
    name="TravelCoordinator",
    model=LiteLlm(model=Settings.MODEL_NAME),
    instruction="""
    You are the travel coordinator.

    Combine the weather, hotel, and budget responses into a complete travel recommendation.

    Produce a concise and practical itinerary.
    """,
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
)

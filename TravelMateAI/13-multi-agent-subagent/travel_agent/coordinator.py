from google.adk.agents import Agent
from google.adk.models import LiteLlm
from .config import MODEL_NAME
from .weather_agent import weather_agent
from .hotel_agent import hotel_agent
from .budget_agent import budget_agent


root_agent = Agent(
    name="TravelCoordinator",
    model=LiteLlm(model=MODEL_NAME),
    instruction="""You are the Travel Coordinator.
                    You are responsible for helping users plan trips.
                    Delegate work to the appropriate specialist agent whenever necessary.
                """,
    sub_agents= [
        weather_agent,
        hotel_agent,
        budget_agent
    ]
)

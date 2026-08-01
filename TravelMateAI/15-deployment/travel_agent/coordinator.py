from google.adk.agents import Agent
from google.adk.models import LiteLlm
from .config import MODEL_NAME


coordinator_agent = Agent(
    name="TravelCoordinator",
    model=LiteLlm(model=MODEL_NAME),
    instruction="""You are the Travel Coordinator.
                    You are responsible for helping users plan trips.
                    Delegate work to the appropriate specialist agent whenever necessary.
                """
)

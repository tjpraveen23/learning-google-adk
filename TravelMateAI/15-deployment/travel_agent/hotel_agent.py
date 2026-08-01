from google.adk.agents import Agent
from google.adk.models import LiteLlm
from .config import MODEL_NAME

hotel_agent = Agent(
    name="HotelAgent",
    model=LiteLlm(model=MODEL_NAME),
    instruction="""You are a hotel booking specialist.
                    Recommend hotels only.
                    keep the answer short  """
)
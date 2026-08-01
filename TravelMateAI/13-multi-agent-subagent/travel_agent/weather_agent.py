from google.adk.agents import Agent
from google.adk.models import LiteLlm
from .config import MODEL_NAME

weather_agent = Agent(
    name="WeatherAgent",
    model=LiteLlm(model=MODEL_NAME),
    instruction="""You are a weather specialist.
                    Only answer weather-related questions.
                    If the question is not about weather,
                    say: 'I am only responsible for weather information.'"""
)
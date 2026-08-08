import time

from google.adk.runners import Runner
from google.genai import types

from .weather_agent import weather_agent
from .hotel_agent import hotel_agent
from .budget_agent import budget_agent
from .coordinator import coordinator_agent


async def create_runners(session_service):
    return {
        "WeatherAgent": Runner(
            app_name="travelmate",
            agent=weather_agent,
            session_service=session_service,
        ),
        "HotelAgent": Runner(
            app_name="travelmate",
            agent=hotel_agent,
            session_service=session_service,
        ),
        "BudgetAgent": Runner(
            app_name="travelmate",
            agent=budget_agent,
            session_service=session_service,
        ),
        "TravelCoordinator": Runner(
            app_name="travelmate",
            agent=coordinator_agent,
            session_service=session_service,
        ),
    }


async def invoke_agent(
    runner,
    agent_name,
    prompt,
    user_id,
    session_id,
):
    start = time.perf_counter()

    content = None

    message = types.Content(
        role="user",
        parts=[types.Part(text=prompt)],
    )

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                content = event.content.parts[0].text

    duration = round(
        time.perf_counter() - start,
        2,
    )

    return content, duration
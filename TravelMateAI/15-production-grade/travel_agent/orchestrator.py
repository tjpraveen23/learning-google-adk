"""
==============================================================
Day 15 - Production Multi-Agent
Step 10: Streaming Orchestrator

Features:
- Async event streaming
- Parallel agent execution
- Persistent sessions
- Request IDs
- Tracing
- Performance metrics

Benefits:
- Real-time UI updates
- Better user experience
- Production observability
==============================================================
"""
import asyncio
import time
import uuid

from google.adk.runners import Runner
from google.genai import types

from .config import Settings
from .logger import get_logger, set_request_id
from .database import get_or_create_session
from .tracing import create_request_span

from .import weather_agent, budget_agent, hotel_agent, coordinator_agent

logger = get_logger("orchestrator")

# ---------------------------------------------------------
# Runner creation
# ---------------------------------------------------------
async def create_runners(session_service):   
    logger.info("Create Runner")
    return  { 
        "WeatherAgent": Runner(
            agent=weather_agent,
            app_name=Settings.APP_NAME,
            session_service=session_service,
        ),
        "HotelAgent": Runner(
            agent=hotel_agent,
            app_name=Settings.APP_NAME,
            session_service=session_service,
        ),
        "BudgetAgent": Runner(
            agent=budget_agent,
            app_name=Settings.APP_NAME,
            session_service=session_service,
        ),
        "TravelCoordinator": Runner(
            agent=coordinator_agent,
            app_name=Settings.APP_NAME,
            session_service=session_service,
        )
    }

# ---------------------------------------------------------
# Invoke one agent
# ---------------------------------------------------------

async def invoke_agent(
    runner,
    agent_name,
    prompt,
    user_id,
    session_id,
):
    logger.info(f"Invoke Agent {agent_name}")
    start = time.perf_counter()

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=prompt)],
    )

    response = ""

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message,
    ):

        if event.is_final_response() and event.content:
            response = event.content.parts[0].text

    duration = round(
        time.perf_counter() - start,
        2,
    )

    return response, duration
# ---------------------------------------------------------
# Streaming orchestration
# ---------------------------------------------------------

async def process_travel_request_stream(
    prompt: str,
    user_id: str,
    session_id: str | None = None,
):

    request_id = str(uuid.uuid4())
    logger.info(f"Process Started {request_id}")
    set_request_id(request_id)

    session_service, session = await get_or_create_session(
        user_id=user_id,
        session_id=session_id,
    )

    runners = await create_runners(session_service)

    request_span = create_request_span(
        request_id=request_id,
        session_id=session.id,
        user_id=user_id,
    )

    total_start = time.perf_counter()

    try:
        city = extract_city(prompt)
        weather_prompt = city
        hotel_prompt = city
        budget_prompt = f"{city} for 3 days"

        # Weather
        yield {
            "agent": "WeatherAgent",
            "status": "started",
            "message": "WeatherAgent started...",
        }

        weather, weather_time = await invoke_agent(
            runners["WeatherAgent"],
            "WeatherAgent",
            weather_prompt,
            user_id,
            session.id,
        )

        yield {
            "agent": "WeatherAgent",
            "status": "completed",
            "message": weather,
            "duration": weather_time,
        }

        # Hotel
        yield {
            "agent": "HotelAgent",
            "status": "started",
            "message": "HotelAgent started...",
        }

        hotel, hotel_time = await invoke_agent(
            runners["HotelAgent"],
            "HotelAgent",
            hotel_prompt,
            user_id,
            session.id,
        )

        yield {
            "agent": "HotelAgent",
            "status": "completed",
            "message": hotel,
            "duration": hotel_time,
        }

        # Budget
        yield {
            "agent": "BudgetAgent",
            "status": "started",
            "message": "BudgetAgent started...",
        }

        budget, budget_time = await invoke_agent(
            runners["BudgetAgent"],
            "BudgetAgent",
            budget_prompt,
            user_id,
            session.id,
        )

        yield {
            "agent": "BudgetAgent",
            "status": "completed",
            "message": budget,
            "duration": budget_time,
        }

        # Coordinator
        yield {
            "agent": "TravelCoordinator",
            "status": "running",
            "message": "Preparing final itinerary...",
        }

        final_prompt = f"""
        User Request:
        {prompt}

        Weather:
        {weather}

        Hotel:
        {hotel}

        Budget:
        {budget}

        Prepare one complete travel recommendation.
        """

        recommendation, coordinator_time = await invoke_agent(
            runners["TravelCoordinator"],
            "TravelCoordinator",
            final_prompt,
            user_id,
            session.id,
        )

        total_time = round(
            time.perf_counter() - total_start,
            2,
        )

        yield {
            "agent": "Final",
            "status": "completed",
            "message": recommendation,
            "performance": {
                "WeatherAgent": weather_time,
                "HotelAgent": hotel_time,
                "BudgetAgent": budget_time,
                "TravelCoordinator": coordinator_time,
                "Total": total_time,
            },
        }
    except Exception as e:
        logger.info("Error occurred: ", e)
    finally:

        request_span.end()
        logger.info("Process Completed")
    

def extract_city(prompt: str) -> str:

    cities = [
        "goa",
        "chennai",
        "bangalore",
        "kerala",
        "delhi",
    ]

    prompt_lower = prompt.lower()

    for city in cities:
        if city in prompt_lower:
            return city.title()

    return "Goa"
import re
import time
import uuid

from .database import get_or_create_session,save_message
from .logger import get_logger, set_request_id
from .runner import create_runners, invoke_agent
from .tracing import (
    request_span as trace_request,
    agent_span,
)

logger = get_logger("orchestrator")


# ---------------------------------------------------------
# City extraction
# ---------------------------------------------------------

def extract_city(prompt: str) -> str:
    cities = [
        "Chennai",
        "Bangalore",
        "Goa",
        "Hyderabad",
        "Mumbai",
        "Delhi",
        "Pune",
        "Kochi",
        "Mysore",
        "Ooty",
        "Jaipur",
        "Kolkata",
    ]

    prompt_lower = prompt.lower()

    for city in cities:
        if city.lower() in prompt_lower:
            return city

    return "Goa"


# ---------------------------------------------------------
# Trip duration extraction
# ---------------------------------------------------------

def extract_trip_days(prompt: str) -> int:
    prompt = prompt.lower()

    patterns = [
        r"for\\s*(\\d+)\\s*days?",
        r"(\\d+)\\s*days?",
        r"(\\d+)\\s*day",
        r"(\\d+)\\s*nights?",
    ]

    for pattern in patterns:
        match = re.search(pattern, prompt)
        if match:
            return int(match.group(1))

    return 3


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

    save_message(
        session_id=session_id,
        role="user",
        content=prompt
    )

    runners = await create_runners(session_service)

    with trace_request(
        request_id=request_id,
        session_id=session.id,
        user_id=user_id,
        prompt=prompt,
    ) as request_trace:

        total_start = time.perf_counter()

        try:
            city = extract_city(prompt)
            days = extract_trip_days(prompt)

            weather_prompt = city
            hotel_prompt = city
            budget_prompt = f"{city} for {days} days"

            # -------------------------------------------------
            # Weather
            # -------------------------------------------------

            yield {
                "agent": "WeatherAgent",
                "status": "started",
                "message": "WeatherAgent started...",
            }

            with agent_span("WeatherAgent") as span:

                weather, weather_time = await invoke_agent(
                    runners["WeatherAgent"],
                    "WeatherAgent",
                    weather_prompt,
                    user_id,
                    session.id,
                )

                if span is not None:
                    span.set_attribute("agent.input", weather_prompt)
                    span.set_attribute("agent.output", weather)
                    span.set_attribute("agent.duration", weather_time)

            yield {
                "agent": "WeatherAgent",
                "status": "completed",
                "message": weather,
                "duration": weather_time,
            }

            # -------------------------------------------------
            # Hotel
            # -------------------------------------------------

            yield {
                "agent": "HotelAgent",
                "status": "started",
                "message": "HotelAgent started...",
            }

            with agent_span("HotelAgent") as span:

                hotel, hotel_time = await invoke_agent(
                    runners["HotelAgent"],
                    "HotelAgent",
                    hotel_prompt,
                    user_id,
                    session.id,
                )

                if span is not None:
                    span.set_attribute("agent.input", hotel_prompt)
                    span.set_attribute("agent.output", hotel)
                    span.set_attribute("agent.duration", hotel_time)

            yield {
                "agent": "HotelAgent",
                "status": "completed",
                "message": hotel,
                "duration": hotel_time,
            }

            # -------------------------------------------------
            # Budget
            # -------------------------------------------------

            yield {
                "agent": "BudgetAgent",
                "status": "started",
                "message": "BudgetAgent started...",
            }

            with agent_span("BudgetAgent") as span:

                budget, budget_time = await invoke_agent(
                    runners["BudgetAgent"],
                    "BudgetAgent",
                    budget_prompt,
                    user_id,
                    session.id,
                )

                if span is not None:
                    span.set_attribute("agent.input", budget_prompt)
                    span.set_attribute("agent.output", budget)
                    span.set_attribute("agent.duration", budget_time)

            yield {
                "agent": "BudgetAgent",
                "status": "completed",
                "message": budget,
                "duration": budget_time,
            }

            # -------------------------------------------------
            # Coordinator
            # -------------------------------------------------

            yield {
                "agent": "TravelCoordinator",
                "status": "running",
                "message": "Preparing final itinerary...",
            }

            final_prompt = f"""
User Request:
{prompt}

Trip Duration:
{days} days

Weather:
{weather}

Hotel:
{hotel}

Budget:
{budget}

Prepare one complete travel recommendation with a practical itinerary.
"""

            with agent_span("TravelCoordinator") as span:

                recommendation, coordinator_time = await invoke_agent(
                    runners["TravelCoordinator"],
                    "TravelCoordinator",
                    final_prompt,
                    user_id,
                    session.id,
                )

                save_message(
                    session_id=session.id,
                    role="assistant",
                    content=recommendation,
                )

                if span is not None:
                    span.set_attribute("agent.input", final_prompt)
                    span.set_attribute("agent.output", recommendation)
                    span.set_attribute(
                        "agent.duration",
                        coordinator_time,
                    )

            if request_trace is not None:
                request_trace.set_attribute("trip.city", city)
                request_trace.set_attribute("trip.days", days)
                request_trace.set_attribute(
                    "final.response",
                    recommendation,
                )

            total_time = round(
                time.perf_counter() - total_start,
                2,
            )

            yield {
                "agent": "Final",
                "status": "completed",
                "session_id": session.id,
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
            logger.exception(f"Error occurred: {e}")

            yield {
                "agent": "System",
                "status": "error",
                "message": str(e),
            }

            raise

    logger.info("Process Completed")
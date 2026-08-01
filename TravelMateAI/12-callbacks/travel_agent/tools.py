"""
==============================================================
Day 6 - Custom Tool

A Tool is a Python function that an LLM can invoke
to retrieve information or perform an action.
==============================================================
"""
from opentelemetry import trace
import asyncio

tracer = trace.get_tracer(__name__)

async def get_weather(city: str) -> str:
    """
    Returns the current weather for a city.
    (Dummy implementation for learning.)
    """

    weather = {
        "goa": "Sunny, 32°C",
        "bangalore": "Cloudy, 25°C",
        "chennai": "Hot, 36°C",
        "kerala": "Rainy, 28°C",
        "delhi": "Hot, 40°C"
    }
    with tracer.start_as_current_span("get_weather_trace") as span:
        span.set_attribute("city", city)
        #print("wait for 5 secs")
        await asyncio.sleep(5)
        return weather.get(city.lower(), "Weather information unavailable.")

async def get_hotel_price_range(city: str) -> str:
    """
    Returns the hotel price range for a city.
    """
    range = {
        "goa": "3000-5000",
        "chennai": "1000-3000",
        "delhi": "3000-8000"
    }
    with tracer.start_as_current_span("get_hotel_price_range_trace") as span:
        span.set_attribute("city", city)
        #print("wait for 10 secs")
        await asyncio.sleep(10)
        return range.get(city.lower(), "Hotel range information unavailable")
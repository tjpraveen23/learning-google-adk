"""
==============================================================
Day 15 - Production Multi-Agent
Step 6: Tools with SQLite Caching

Features:
- Cache-aside pattern
- TTL based caching
- Cache hit / miss metadata
- Structured responses

Benefits:
- Faster repeated requests
- Reduced tool execution
- Better streaming visibility
==============================================================
"""

import asyncio

from .cache import (
    get_cache,
    set_cache,
)

from .config import Settings

# ---------------------------------------------------------
# Weather Tool
# ---------------------------------------------------------

async def get_weather(city: str):

    cache_key = f"weather:{city.lower()}"

    cached = get_cache(cache_key)

    if cached is not None:

        return {
            "result": cached["weather"],
            "cache_hit": True,
        }

    await asyncio.sleep(5)

    weather = {
        "goa": "Sunny, 32°C",
        "bangalore": "Cloudy, 25°C",
        "chennai": "Hot, 36°C",
        "kerala": "Rainy, 28°C",
        "delhi": "Hot, 40°C",
    }

    result = weather.get(
        city.lower(),
        "Weather information unavailable."
    )

    set_cache(
        cache_key=cache_key,
        value={"weather": result},
        ttl_seconds=Settings.WEATHER_CACHE_TTL,
        agent_name="WeatherAgent",
    )

    return result

# ---------------------------------------------------------
# Hotel Tool
# ---------------------------------------------------------

async def get_hotel_price_range(city: str):

    cache_key = f"hotel:{city.lower()}"

    cached = get_cache(cache_key)

    if cached is not None:

        return {
            "result": cached["hotel"],
            "cache_hit": True,
        }

    await asyncio.sleep(10)

    hotels = {
        "goa": "Sea View Resort - ₹3,500/night",
        "chennai": "Marina Hotel - ₹2,200/night",
        "delhi": "Connaught Inn - ₹5,500/night",
    }

    result = hotels.get(
        city.lower(),
        "Hotel information unavailable."
    )

    set_cache(
        cache_key=cache_key,
        value={"hotel": result},
        ttl_seconds=Settings.HOTEL_CACHE_TTL,
        agent_name="HotelAgent",
    )

    return result

# ---------------------------------------------------------
# Budget Tool
# ---------------------------------------------------------

async def estimate_budget(
    city: str,
    days: int,
):

    cache_key = f"budget:{city.lower()}:{days}"

    cached = get_cache(cache_key)

    if cached is not None:

        return {
            "result": cached["budget"],
            "cache_hit": True,
        }

    await asyncio.sleep(2)

    estimates = {
        "goa": 18000,
        "chennai": 12000,
        "delhi": 22000,
    }

    amount = estimates.get(
        city.lower(),
        15000,
    )

    result = f"Estimated budget: ₹{amount}"

    set_cache(
        cache_key=cache_key,
        value={"budget": result},
        ttl_seconds=Settings.BUDGET_CACHE_TTL,
        agent_name="BudgetAgent",
    )

    return result
"""
==============================================================
Day 15 - Production Multi-Agent
Step 6: Tools with SQLite Caching + Phoenix Tracing

Features:
- Cache-aside pattern
- TTL based caching
- Cache hit / miss metadata
- Tool tracing
- Consistent response format
- LLM fallback for unsupported cities
==============================================================
"""

import asyncio

from .cache import get_cache, set_cache
from .config import Settings
from .tracing import tool_span

# ---------------------------------------------------------
# Weather Tool
# ---------------------------------------------------------

async def get_weather(city: str):

    with tool_span("get_weather") as span:

        cache_key = f"weather:{city.lower()}"

        cached = get_cache(cache_key)

        if cached is not None:

            result = cached["weather"]

            if span is not None:
                span.set_attribute("tool.input.city", city)
                span.set_attribute("tool.output", result)
                span.set_attribute("cache.hit", True)

            return {
                "result": result,
                "cache_hit": True,
                "estimated": cached.get("estimated", False),
            }

        await asyncio.sleep(1)

        weather = {
            "goa": "Sunny, 32°C",
            "bangalore": "Cloudy, 25°C",
            "chennai": "Hot, 36°C",
            "kerala": "Rainy, 28°C",
            "delhi": "Hot, 40°C",
        }

        city_key = city.lower()

        if city_key in weather:
            result = weather[city_key]
            estimated = False
        else:
            result = (
                f"Estimate the likely weather for {city} based on a typical seasonal forecast. "
                "Clearly mention that this is an estimate."
            )
            estimated = True

        set_cache(
            cache_key=cache_key,
            value={
                "weather": result,
                "estimated": estimated,
            },
            ttl_seconds=Settings.WEATHER_CACHE_TTL,
            agent_name="WeatherAgent",
        )

        if span is not None:
            span.set_attribute("tool.input.city", city)
            span.set_attribute("tool.output", result)
            span.set_attribute("cache.hit", False)
            span.set_attribute("tool.estimated", estimated)

        return {
            "result": result,
            "cache_hit": False,
            "estimated": estimated,
        }

# ---------------------------------------------------------
# Hotel Tool
# ---------------------------------------------------------

async def get_hotel_price_range(city: str):

    with tool_span("get_hotel_price_range") as span:

        cache_key = f"hotel:{city.lower()}"

        cached = get_cache(cache_key)

        if cached is not None:

            result = cached["hotel"]

            if span is not None:
                span.set_attribute("tool.input.city", city)
                span.set_attribute("tool.output", result)
                span.set_attribute("cache.hit", True)

            return {
                "result": result,
                "cache_hit": True,
                "estimated": cached.get("estimated", False),
            }

        await asyncio.sleep(1)

        hotels = {
            "goa": "Sea View Resort - ₹3,500/night",
            "chennai": "Marina Hotel - ₹2,200/night",
            "delhi": "Connaught Inn - ₹5,500/night",
        }

        city_key = city.lower()

        if city_key in hotels:
            result = hotels[city_key]
            estimated = False
        else:
            result = (
                f"Estimate a reasonable mid-range hotel price per night in {city} for a typical traveler. "
                "Clearly mention that this is an estimate."
            )
            estimated = True

        set_cache(
            cache_key=cache_key,
            value={
                "hotel": result,
                "estimated": estimated,
            },
            ttl_seconds=Settings.HOTEL_CACHE_TTL,
            agent_name="HotelAgent",
        )

        if span is not None:
            span.set_attribute("tool.input.city", city)
            span.set_attribute("tool.output", result)
            span.set_attribute("cache.hit", False)
            span.set_attribute("tool.estimated", estimated)

        return {
            "result": result,
            "cache_hit": False,
            "estimated": estimated,
        }

# ---------------------------------------------------------
# Budget Tool
# ---------------------------------------------------------

async def estimate_budget(
    city: str,
    days: int,
):

    with tool_span("estimate_budget") as span:

        cache_key = f"budget:{city.lower()}:{days}"

        cached = get_cache(cache_key)

        if cached is not None:

            result = cached["budget"]

            if span is not None:
                span.set_attribute("tool.input.city", city)
                span.set_attribute("tool.input.days", days)
                span.set_attribute("tool.output", result)
                span.set_attribute("cache.hit", True)

            return {
                "result": result,
                "cache_hit": True,
                "estimated": cached.get("estimated", False),
            }

        await asyncio.sleep(1)

        estimates = {
            "goa": 18000,
            "chennai": 12000,
            "delhi": 22000,
        }

        city_key = city.lower()

        if city_key in estimates:
            amount = estimates[city_key]
            result = f"Estimated budget for {days} days: ₹{amount}"
            estimated = False
        else:
            result = (
                f"Estimate a reasonable travel budget for {days} days in {city}, including hotel, food, "
                "and local transportation. Clearly mention that this is an estimate."
            )
            estimated = True

        set_cache(
            cache_key=cache_key,
            value={
                "budget": result,
                "estimated": estimated,
            },
            ttl_seconds=Settings.BUDGET_CACHE_TTL,
            agent_name="BudgetAgent",
        )

        if span is not None:
            span.set_attribute("tool.input.city", city)
            span.set_attribute("tool.input.days", days)
            span.set_attribute("tool.output", result)
            span.set_attribute("cache.hit", False)
            span.set_attribute("tool.estimated", estimated)

        return {
            "result": result,
            "cache_hit": False,
            "estimated": estimated,
        }
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from travel_agent.cache import (
    get_cache,
    set_cache,
    clear_cache,
)

clear_cache()

print("First lookup (MISS):")
print(get_cache("weather:goa"))

set_cache(
    cache_key="weather:goa",
    value={"weather": "Sunny, 32°C"},
    ttl_seconds=60,
    agent_name="WeatherAgent",
)

print()

print("Second lookup (HIT):")
print(get_cache("weather:goa"))
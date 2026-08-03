import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from travel_agent.config import Settings

print("APP_NAME:", Settings.APP_NAME)
print("MODEL:", Settings.MODEL_NAME)
print("SESSION_DB:", Settings.SESSION_DB)
print("CACHE_DB:", Settings.CACHE_DB)
print("TRACE_DB:", Settings.TRACE_DB)
print("WEATHER_CACHE_TTL:", Settings.WEATHER_CACHE_TTL)
"""
==============================================================
Day 15 - Production Multi-Agent
Step 2: Centralized Configuration

All configuration comes from .env

Benefits:
- No hardcoded values
- Environment specific deployment
- CI/CD friendly
- Docker friendly
==============================================================
"""
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:

# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

    BASE_DIR = BASE_DIR
    DATA_DIR = BASE_DIR / "data"
    LOG_DIR = BASE_DIR / "logs"

    DATA_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)

    APP_NAME = os.getenv("APP_NAME", "travelmate")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

    MODEL_NAME = os.getenv("MODEL_NAME")

    SESSION_DB = str(DATA_DIR / "travelmate.db")
    CACHE_DB = str(DATA_DIR / "cache.db")
    TRACE_DB = str(DATA_DIR / "trace.db")

    WEATHER_CACHE_TTL = int(os.getenv("WEATHER_CACHE_TTL", "1800"))
    HOTEL_CACHE_TTL = int(os.getenv("HOTEL_CACHE_TTL", "3600"))
    BUDGET_CACHE_TTL = int(os.getenv("BUDGET_CACHE_TTL", "86400"))
    ITINERARY_CACHE_TTL = int(os.getenv("ITINERARY_CACHE_TTL", "900"))

    FILE_LOG_ENTRY = os.getenv("FILE_LOG_ENTRY", "no")
    TRACING_ENABLED = os.getenv("TRACING_ENABLED", "no")
    
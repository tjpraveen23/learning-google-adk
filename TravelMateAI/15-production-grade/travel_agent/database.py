"""
==============================================================
Day 15 - Production Multi-Agent
Step 4: Persistent SQLite Session Memory

Features:
- DatabaseSessionService
- SQLite persistence
- UUID session IDs
- Automatic session creation
- Reusable session service

Benefits:
- Conversation survives restart
- User preferences persist
- FastAPI and Streamlit share sessions
==============================================================
"""

import uuid
from google.adk.sessions import DatabaseSessionService
from .config import Settings
from .logger import get_logger

logger = get_logger("database")

# ---------------------------------------------------------
# Singleton session service - This is important because:
    # FastAPI should not create a new database connection for every request.
    # Streamlit should reuse the same service.
    # The orchestrator should share sessions across requests.
# ---------------------------------------------------------
session_service = DatabaseSessionService(db_url=f"sqlite+aiosqlite:///{Settings.SESSION_DB}")

# ---------------------------------------------------------
# Get or create a session
# ---------------------------------------------------------
async def get_or_create_session(
        user_id: str,
        session_id: str | None = None
):
    if session_id is None:
        session_id = str(uuid.uuid4())

    session = await session_service.get_session(
        app_name=Settings.APP_NAME,
        user_id=user_id,
        session_id=session_id
    )

    if session is None:
        session = await session_service.create_session(
            app_name=Settings.APP_NAME,
            user_id=user_id,
            session_id=session_id,
            state={
                "user_name": user_id,
                "preferences": []
            }
        )

        logger.info(f"Created Session {session_id}")
    else:
        logger.info(f"Loaded Session {session_id}")

    return session_service, session

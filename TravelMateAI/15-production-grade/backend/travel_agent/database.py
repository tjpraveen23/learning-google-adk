"""
==============================================================
Day 15 - Production Multi-Agent
Persistent SQLite Session Memory + Chat History

Features:
- DatabaseSessionService
- SQLite persistence
- Persistent chat history
- Session list
- Session history retrieval
==============================================================
"""

import sqlite3
import uuid
from pathlib import Path

from google.adk.sessions import DatabaseSessionService

from .config import Settings
from .logger import get_logger

logger = get_logger("database")

# ---------------------------------------------------------
# Database paths
# ---------------------------------------------------------

DB_PATH = Path(Settings.SESSION_DB)

# ---------------------------------------------------------
# ADK Session Service
# ---------------------------------------------------------

session_service = DatabaseSessionService(
    db_url=f"sqlite+aiosqlite:///{DB_PATH}"
)

# ---------------------------------------------------------
# Initialize chat tables
# ---------------------------------------------------------

def init_chat_tables():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


init_chat_tables()

# ---------------------------------------------------------
# Get or create ADK session
# ---------------------------------------------------------

async def get_or_create_session(
    user_id: str,
    session_id: str | None = None,
):
    if session_id is None:
        session_id = str(uuid.uuid4())

    session = await session_service.get_session(
        app_name=Settings.APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    if session is None:

        session = await session_service.create_session(
            app_name=Settings.APP_NAME,
            user_id=user_id,
            session_id=session_id,
            state={
                "user_name": user_id,
                "preferences": [],
            },
        )

        create_chat_session(
            session_id=session_id,
            user_id=user_id,
        )

        logger.info(f"Created Session {session_id}")

    else:
        logger.info(f"Loaded Session {session_id}")

    return session_service, session

# ---------------------------------------------------------
# Chat session functions
# ---------------------------------------------------------

def create_chat_session(
    session_id: str,
    user_id: str,
):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO chat_sessions
        (session_id, user_id, title)
        VALUES (?, ?, ?)
        """,
        (
            session_id,
            user_id,
            "New Travel Plan",
        ),
    )

    conn.commit()
    conn.close()


def save_message(
    session_id: str,
    role: str,
    content: str,
):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_messages
        (session_id, role, content)
        VALUES (?, ?, ?)
        """,
        (
            session_id,
            role,
            content,
        ),
    )

    if role == "user":

        cursor.execute(
            """
            UPDATE chat_sessions
            SET
                title = CASE
                    WHEN title = 'New Travel Plan'
                    THEN ?
                    ELSE title
                END,
                updated_at = CURRENT_TIMESTAMP
            WHERE session_id = ?
            """,
            (
                content[:40],
                session_id,
            ),
        )

    else:

        cursor.execute(
            """
            UPDATE chat_sessions
            SET updated_at = CURRENT_TIMESTAMP
            WHERE session_id = ?
            """,
            (session_id,),
        )

    conn.commit()
    conn.close()

# ---------------------------------------------------------
# List sessions
# ---------------------------------------------------------

def list_sessions(user_id: str):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            session_id,
            title,
            updated_at
        FROM chat_sessions
        WHERE user_id = ?
        ORDER BY updated_at DESC
        """,
        (user_id,),
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

# ---------------------------------------------------------
# Get chat history
# ---------------------------------------------------------

def get_session_history(session_id: str):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            role,
            content,
            created_at
        FROM chat_messages
        WHERE session_id = ?
        ORDER BY created_at ASC
        """,
        (session_id,),
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]
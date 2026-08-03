"""
==============================================================
Day 15 - Production Multi-Agent
Step 5: SQLite Cache Layer

Features:
- SQLite cache storage
- TTL support
- Cache hit / miss logging
- Automatic expiration
- JSON serialization
==============================================================
"""

import json
import sqlite3
from datetime import datetime, timedelta

from .config import Settings
from .logger import get_logger

logger = get_logger("cache")

# ---------------------------------------------------------
# Initialize cache database
# ---------------------------------------------------------

def initialize_cache():

    with sqlite3.connect(Settings.CACHE_DB) as conn:

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                cache_key TEXT PRIMARY KEY,
                cache_value TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                agent_name TEXT NOT NULL
            )
            """
        )

        conn.commit()


initialize_cache()

# ---------------------------------------------------------
# Get cache
# ---------------------------------------------------------

def get_cache(cache_key: str):

    with sqlite3.connect(Settings.CACHE_DB) as conn:

        cursor = conn.execute(
            """
            SELECT cache_value, expires_at
            FROM cache
            WHERE cache_key = ?
            """,
            (cache_key,),
        )

        row = cursor.fetchone()

    if row is None:

        logger.info(f"Cache MISS: {cache_key}")

        return None

    value, expires_at = row

    if datetime.now() > datetime.fromisoformat(expires_at):

        logger.info(f"Cache EXPIRED: {cache_key}")

        delete_cache(cache_key)

        return None

    logger.info(f"Cache HIT: {cache_key}")

    return json.loads(value)

# ---------------------------------------------------------
# Set cache
# ---------------------------------------------------------

def set_cache(
    cache_key: str,
    value,
    ttl_seconds: int,
    agent_name: str,
):

    created_at = datetime.now()

    expires_at = created_at + timedelta(seconds=ttl_seconds)

    with sqlite3.connect(Settings.CACHE_DB) as conn:

        conn.execute(
            """
            INSERT OR REPLACE INTO cache (
                cache_key,
                cache_value,
                created_at,
                expires_at,
                agent_name
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                cache_key,
                json.dumps(value),
                created_at.isoformat(),
                expires_at.isoformat(),
                agent_name,
            ),
        )

        conn.commit()

    logger.info(f"Cache STORED: {cache_key}")

# ---------------------------------------------------------
# Delete cache
# ---------------------------------------------------------

def delete_cache(cache_key: str):

    with sqlite3.connect(Settings.CACHE_DB) as conn:

        conn.execute(
            "DELETE FROM cache WHERE cache_key = ?",
            (cache_key,),
        )

        conn.commit()

# ---------------------------------------------------------
# Clear cache
# ---------------------------------------------------------

def clear_cache():

    with sqlite3.connect(Settings.CACHE_DB) as conn:

        conn.execute("DELETE FROM cache")

        conn.commit()

    logger.info("Cache CLEARED")
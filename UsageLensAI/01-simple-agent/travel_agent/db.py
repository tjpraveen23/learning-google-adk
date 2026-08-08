import sqlite3
from .config import Config


def get_connection():
    return sqlite3.connect(Config.DB_PATH)


def execute_query(sql, params=None):
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()

        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


def execute_non_query(sql, params=None):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        conn.commit()

    finally:
        conn.close()
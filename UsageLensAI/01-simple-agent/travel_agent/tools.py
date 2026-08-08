from .db import execute_query
from pathlib import Path

schema = Path("schema_relationship.txt").read_text(encoding="utf-8")

def query_usage_data(question: str):
    """
    This tool receives the user question.
    The ADK agent will generate the SQL based on the schema
    and execute it through this tool.
    """

    # Placeholder for POC.
    # Start with predefined mappings.

    question_lower = question.lower()

    if "inactive" in question_lower and "user" in question_lower:
        sql = """
        SELECT TOP 20
            u.user_name,
            g.group_name,
            MAX(c.last_modified_date) AS last_activity
        FROM users u
        LEFT JOIN groups g
            ON u.group_id = g.group_id
        LEFT JOIN contents c
            ON u.user_id = c.created_by
        GROUP BY
            u.user_name,
            g.group_name
        ORDER BY
            last_activity ASC
        """

    elif "zero view" in question_lower or "unused content" in question_lower:
        sql = """
        SELECT TOP 20
            content_id,
            view_count,
            last_modified_date
        FROM contents
        WHERE view_count = 0
        ORDER BY last_modified_date ASC
        """

    else:
        sql = "SELECT TOP 20 * FROM users"

    return execute_query(sql)
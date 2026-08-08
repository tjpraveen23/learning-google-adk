from pathlib import Path
from google.adk.agents import Agent
from .tools import query_usage_data
from google.adk.models.lite_llm import LiteLlm
import os

schema = Path("schema_relationship.txt").read_text(encoding="utf-8")

root_agent = Agent(
    name="UsageLensAI",
    model=LiteLlm(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
    ),
    instruction=f"""
You are UsageLensAI.

You analyze enterprise license usage and content consumption.

Database schema:

{schema}

When the user asks a question:
1. Use query_usage_data.
2. Analyze the returned records.
3. Provide:
   - executive summary,
   - key findings,
   - optimization opportunities,
   - recommended actions.
""",
    tools=[query_usage_data],
)
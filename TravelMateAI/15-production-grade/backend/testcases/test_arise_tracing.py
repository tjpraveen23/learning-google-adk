import time
import sys
import os

# Add backend directory to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from travel_agent.tracing import (
    start_request_span,
    start_agent_span,
    start_tool_span,
)

request_span = start_request_span(
    request_id="req-001",
    session_id="session-001",
    prompt="Plan a Chennai trip under 20000",
)

agent_span = start_agent_span("WeatherAgent")

tool_span = start_tool_span("get_weather")

time.sleep(1)

tool_span.end()

agent_span.end()

request_span.end()

print("Trace sent to Phoenix")
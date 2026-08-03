"""
==============================================================
Day 15 - Production Multi-Agent
Step 9: OpenTelemetry Tracing

Features:
- Root request span
- Agent spans
- Tool spans
- Request correlation
- Performance timing

Benefits:
- End-to-end observability
- Production diagnostics
- Arize / Jaeger integration
==============================================================
"""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from .config import Settings
from .logger import get_logger

logger = get_logger("tracing")
# ---------------------------------------------------------
# Tracer provider
# ---------------------------------------------------------

trace_provider = TracerProvider()

# We will add exporters later
trace.set_tracer_provider(trace_provider)

tracer = trace.get_tracer(Settings.APP_NAME)

# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------
def create_request_span(
        request_id: str,
        session_id: str,
        user_id: str
):
    span = tracer.start_span("Travel Request")

    span.set_attribute("request_id", request_id)
    span.set_attribute("session_id", session_id)
    span.set_attribute("user_id", user_id)

    return span

def create_agent_span(
    agent_name: str,
    request_id: str,
):
    span = tracer.start_span(agent_name)

    span.set_attribute(
        "agent.name",
        agent_name,
    )

    span.set_attribute(
        "request.id",
        request_id,
    )

    return span


def create_tool_span(
    tool_name: str,
    request_id: str,
):
    span = tracer.start_span(tool_name)

    span.set_attribute(
        "tool.name",
        tool_name,
    )

    span.set_attribute(
        "request.id",
        request_id,
    )

    return span
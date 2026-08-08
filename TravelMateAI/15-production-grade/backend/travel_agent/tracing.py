"""
==============================================================
TravelMate AI - Tracing

Features:
- Phoenix tracing enabled/disabled from .env
- Docker-compatible OTLP export
- Request spans
- Agent spans
- Tool spans
==============================================================
"""

from contextlib import contextmanager

from opentelemetry import trace
from opentelemetry.trace import NoOpTracerProvider

from .config import Settings

# ---------------------------------------------------------
# Initialize tracing
# ---------------------------------------------------------

tracer = None

if Settings.TRACING_ENABLED:

    from phoenix.otel import register

    provider = trace.get_tracer_provider()

    # Register Phoenix only once
    if provider.__class__.__name__ == "ProxyTracerProvider":

        tracer_provider = register(
            project_name="travelmate-ai"
        )

        trace.set_tracer_provider(tracer_provider)

    tracer = trace.get_tracer("travelmate-ai")

else:

    trace.set_tracer_provider(NoOpTracerProvider())
    tracer = None

# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def is_tracing_enabled() -> bool:
    return Settings.TRACING_ENABLED and tracer is not None

# ---------------------------------------------------------
# Request span
# ---------------------------------------------------------

@contextmanager
def request_span(
    request_id: str,
    session_id: str,
    user_id: str,
    prompt: str = "",
):
    if tracer is None:
        yield None
        return

    with tracer.start_as_current_span("Travel Request") as span:

        span.set_attribute("request.id", request_id)
        span.set_attribute("session.id", session_id)
        span.set_attribute("user.id", user_id)

        if prompt:
            span.set_attribute("prompt", prompt)

        yield span

# ---------------------------------------------------------
# Agent span
# ---------------------------------------------------------

@contextmanager
def agent_span(agent_name: str):
    if tracer is None:
        yield None
        return

    with tracer.start_as_current_span(agent_name) as span:

        span.set_attribute("agent.name", agent_name)

        yield span

# ---------------------------------------------------------
# Tool span
# ---------------------------------------------------------

@contextmanager
def tool_span(tool_name: str):
    if tracer is None:
        yield None
        return

    with tracer.start_as_current_span(tool_name) as span:

        span.set_attribute("tool.name", tool_name)

        yield span

# ---------------------------------------------------------
# Test trace
# ---------------------------------------------------------

def test_trace():
    if tracer is None:
        return

    with tracer.start_as_current_span("Phoenix Test") as span:
        span.set_attribute("test.source", "docker")
        span.set_attribute("test.value", "hello-phoenix")
"""
==============================================================
Day 15 - Production Multi-Agent
Step 11: FastAPI Production API

Endpoints:
GET  /health
POST /travel (streaming)

Features:
- Streaming responses
- Request IDs
- Production-ready API
==============================================================
"""

import json
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from travel_agent.orchestrator import process_travel_request_stream

app = FastAPI(
    title="TravelMate API",
    version="1.0.0",
)


# ---------------------------------------------------------
# Request model
# ---------------------------------------------------------

class TravelRequest(BaseModel):
    prompt: str
    user_id: str


# ---------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "healthy",
        "service": "travelmate",
    }


# ---------------------------------------------------------
# Streaming endpoint
# ---------------------------------------------------------
@app.post("/travel")
async def travel(request: TravelRequest):

    session_id = str(uuid4())

    async def event_generator():

        async for event in process_travel_request_stream(
            prompt=request.prompt,
            user_id=request.user_id,
            session_id=session_id,
        ):
            yield {
                "event": "message",
                "data": json.dumps(event, ensure_ascii=False),
            }

    return EventSourceResponse(event_generator())
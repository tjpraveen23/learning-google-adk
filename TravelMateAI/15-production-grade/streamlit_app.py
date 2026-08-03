"""
==============================================================
Day 15 - Production Multi-Agent
Step 12: Streamlit UI

Features:
- Left sidebar with chat history
- New session support
- Streaming agent updates
- Final recommendation
- Performance summary
==============================================================
"""

import json
import uuid
import requests
import streamlit as st
from sseclient import SSEClient

API_URL = "http://127.0.0.1:8000/travel"

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="TravelMate AI",
    page_icon="✈️",
    layout="wide",
)

# ---------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------

if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "current_session" not in st.session_state:
    session_id = str(uuid.uuid4())

    st.session_state.current_session = session_id

    st.session_state.sessions[session_id] = {
        "title": "New Chat",
        "messages": [],
    }

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

st.sidebar.title("💬 Chats")

if st.sidebar.button("+ New Session", use_container_width=True):

    session_id = str(uuid.uuid4())

    st.session_state.current_session = session_id

    st.session_state.sessions[session_id] = {
        "title": "New Chat",
        "messages": [],
    }

    st.rerun()

st.sidebar.divider()

# Chat history list

for session_id, session in st.session_state.sessions.items():

    title = session["title"]

    if st.sidebar.button(
        title,
        key=session_id,
        use_container_width=True,
    ):
        st.session_state.current_session = session_id
        st.rerun()

# ---------------------------------------------------------
# Main UI
# ---------------------------------------------------------

st.title("✈️ TravelMate AI")
st.caption("Production Multi-Agent Travel Planner")

current = st.session_state.sessions[
    st.session_state.current_session
]

# Display conversation history

for msg in current["messages"]:

    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# ---------------------------------------------------------
# User input
# ---------------------------------------------------------

prompt = st.chat_input(
    "Plan a trip (e.g., Chennai under ₹20,000)"
)

# ---------------------------------------------------------
# Streaming execution
# ---------------------------------------------------------

if prompt:

    # Save user message

    current["messages"].append(
        {
            "role": "user",
            "text": prompt,
        }
    )

    # Update session title

    if current["title"] == "New Chat":
        current["title"] = prompt[:40]

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        weather_box = st.empty()
        hotel_box = st.empty()
        budget_box = st.empty()
        coordinator_box = st.empty()

        final_box = st.empty()
        performance_box = st.empty()

        response = requests.post(
            API_URL,
            json={
                "prompt": prompt,
                "user_id": "praveen_tj",
            },
            stream=True,
            headers={
                "Accept": "text/event-stream"
            },
        )

        client = SSEClient(response)

        final_message = ""

        for sse in client.events():

            if not sse.data:
                continue

            event = json.loads(sse.data)

            agent = event.get("agent")
            status = event.get("status")
            message = event.get("message")

            # Weather Agent

            if agent == "WeatherAgent":

                if status == "started":
                    weather_box.info("🌤️ WeatherAgent started...")

                elif status == "completed":

                    duration = event.get("duration", 0)

                    weather_box.success(
                        f"🌤️ WeatherAgent completed ({duration} sec)\\n\\n{message}"
                    )

            # Hotel Agent

            elif agent == "HotelAgent":

                if status == "started":
                    hotel_box.info("🏨 HotelAgent started...")

                elif status == "completed":

                    duration = event.get("duration", 0)

                    hotel_box.success(
                        f"🏨 HotelAgent completed ({duration} sec)\\n\\n{message}"
                    )

            # Budget Agent

            elif agent == "BudgetAgent":

                if status == "started":
                    budget_box.info("💰 BudgetAgent started...")

                elif status == "completed":

                    duration = event.get("duration", 0)

                    budget_box.success(
                        f"💰 BudgetAgent completed ({duration} sec)\\n\\n{message}"
                    )

            # Coordinator

            elif agent == "TravelCoordinator":

                coordinator_box.info(
                    "🧠 TravelCoordinator preparing final itinerary..."
                )

            # Final Response

            elif agent == "Final":

                final_message = message

                final_box.markdown(
                    "## Final travel recommendation"
                )

                final_box.markdown(message)

                performance_box.markdown(
                    "### Performance summary"
                )

                performance_box.json(
                    event.get("performance", {})
                )

        # Save assistant response

        current["messages"].append(
            {
                "role": "assistant",
                "text": final_message,
            }
        )

    st.rerun()
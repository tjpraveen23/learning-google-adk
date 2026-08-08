"""
==============================================================
Day 15 - Production Multi-Agent
Step 12: Streamlit UI with Persistent Chat History

Features:
- Persistent chat history from backend
- Left sidebar with session list
- New session support
- Streaming agent updates
- Final recommendation
- Performance summary
==============================================================
"""

import json
import requests
import streamlit as st
from sseclient import SSEClient

import os

API_BASE = os.getenv(
    "API_BASE",
    "http://127.0.0.1:8000"
)
API_URL = f"{API_BASE}/travel"
USER_ID = "praveen"

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="TravelMate AI",
    page_icon="✈️",
    layout="wide",
)

# ---------------------------------------------------------
# Backend APIs
# ---------------------------------------------------------

def load_sessions():
    response = requests.get(
        f"{API_BASE}/sessions/{USER_ID}"
    )

    if response.status_code == 200:
        return response.json()

    return []


def load_history(session_id: str):
    response = requests.get(
        f"{API_BASE}/history/{session_id}"
    )

    if response.status_code == 200:
        return response.json()

    return []


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "current_session" not in st.session_state:
    st.session_state.current_session = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

st.sidebar.title("💬 Chats")

if st.sidebar.button(
    "+ New Session",
    use_container_width=True,
):
    st.session_state.current_session = None
    st.session_state.messages = []
    st.rerun()

st.sidebar.divider()

sessions = load_sessions()

for session in sessions:

    if st.sidebar.button(
        session["title"],
        key=session["session_id"],
        use_container_width=True,
    ):
        st.session_state.current_session = session["session_id"]
        st.session_state.messages = load_history(
            session["session_id"]
        )
        st.rerun()

# ---------------------------------------------------------
# Main UI
# ---------------------------------------------------------

st.title("✈️ TravelMate AI")
st.caption("Production Multi-Agent Travel Planner")

# Display history

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

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

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

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
                "user_id": USER_ID,
                "session_id": st.session_state.current_session,
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

            if agent == "WeatherAgent":

                if status == "started":
                    weather_box.info(
                        "🌤️ WeatherAgent started..."
                    )

                elif status == "completed":

                    duration = event.get("duration", 0)

                    weather_box.success(
                        f"🌤️ WeatherAgent completed ({duration} sec)\\n\\n{message}"
                    )

            elif agent == "HotelAgent":

                if status == "started":
                    hotel_box.info(
                        "🏨 HotelAgent started..."
                    )

                elif status == "completed":

                    duration = event.get("duration", 0)

                    hotel_box.success(
                        f"🏨 HotelAgent completed ({duration} sec)\\n\\n{message}"
                    )

            elif agent == "BudgetAgent":

                if status == "started":
                    budget_box.info(
                        "💰 BudgetAgent started..."
                    )

                elif status == "completed":

                    duration = event.get("duration", 0)

                    budget_box.success(
                        f"💰 BudgetAgent completed ({duration} sec)\\n\\n{message}"
                    )

            elif agent == "TravelCoordinator":

                coordinator_box.info(
                    "🧠 TravelCoordinator preparing final itinerary..."
                )

            elif agent == "Final":

                final_message = message

                st.session_state.current_session = event.get(
                    "session_id"
                )

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

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": final_message,
            }
        )

    st.rerun()
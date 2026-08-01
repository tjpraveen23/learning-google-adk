import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from travel_agent.agent import root_agent

APP_NAME = "travelmate"
USER_ID = "praveen_tj"
SESSION_ID = "session_01"

# Day 4: Structured way of storing use preferences in the state under session.
async def main():

    session_service = InMemorySessionService()
    initial_state = {
        "user_name":"praveen_tj",
        "user_preferences": """My favorite place Goa, Bangalore, Madurai. 
                              My travel budget range 20k. 
                              I like playing cricket.
                              I will plan on weekend or during holidays for 3 days"""
    }
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state
    )

    session = await session_service.get_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    )
    
    print("\n===== Session State =====")
    for key, value in session.state.items():
        print(f"{key}: {value}")
    print("=========================\n")

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print("=" * 60)
    print("TravelMate Chat")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:

        prompt = input("\nYou : ")

        if prompt.lower() == "exit":
            break

        user_message = types.Content(
            role="user",
            parts=[
                types.Part(text=prompt)
            ]
        )

        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=user_message,
        ):

            if event.is_final_response():
                print(f"\nTravelMate : {event.content.parts[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
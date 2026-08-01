import asyncio
import uuid
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types
from travel_agent.agent import root_agent
from google.adk.memory import InMemoryMemoryService

APP_NAME = "travelmate"
USER_ID = "praveen_tj"
SESSION_ID = "session_1"

# Day 10:
# DatabaseSessionService stores conversation history in SQLite,
# allowing the same conversation to continue even after
# restarting the application.
async def main():

    session_service = DatabaseSessionService(db_url="sqlite+aiosqlite:///travelmate.db")

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    if session is None:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
        )
        print(f"Created Session : {SESSION_ID}")
    else:
        print("Existing session loaded")

   
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
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
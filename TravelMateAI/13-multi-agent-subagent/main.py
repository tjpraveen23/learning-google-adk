import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.memory import InMemoryMemoryService
from travel_agent.coordinator import root_agent

APP_NAME = "travelmate"
USER_ID = "praveen_tj"
SESSION_ID = "session_01"

# Day 13: Multi-Agent - Check Sub-agent added in coordinator.py. This agent decide which agent to invoke and final response is produced
async def main():

    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
   
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
            print("=" * 60)
            print(f"Author     : {event.author}")
            print(f"Invocation : {event.invocation_id}")
            print(f"Final      : {event.is_final_response()}")

            if event.content:
                print(f"Role       : {event.content.role}")

                for part in event.content.parts:
                    if getattr(part, "text", None):
                        print(f"Text       : {part.text}")                        

if __name__ == "__main__":
    asyncio.run(main())
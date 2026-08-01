import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from travel_agent.agent import root_agent
from google.adk.memory import InMemoryMemoryService

APP_NAME = "travelmate"
USER_ID = "praveen_tj"
SESSION_ID = "session_01"

# Day 10: Display all the events like User request, Tool invoked, Tool response and LLM final response.
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

        event_no = 1

        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=user_message,
        ):

            print("\n" + "=" * 70)
            print(f"EVENT #{event_no}")
            print("=" * 70)

            print(f"Author : {event.author}")
            print(f"Role   : {event.content.role if event.content else 'N/A'}")
            print(f"Final  : {event.is_final_response()}")

            if event.content and event.content.parts:

                for i, part in enumerate(event.content.parts, start=1):

                    print(f"\nPart {i}")

                    # Normal text
                    if getattr(part, "text", None):
                        print(f"Text : {part.text}")

                    # Tool call from LLM
                    if getattr(part, "function_call", None):
                        print("\nTool Invoked")
                        print(f"Name      : {part.function_call.name}")
                        print(f"Arguments : {part.function_call.args}")

                    # Tool response
                    if getattr(part, "function_response", None):
                        print("\nTool Response")
                        print(f"Name   : {part.function_response.name}")
                        print(f"Result : {part.function_response.response}")

            event_no += 1

                     

if __name__ == "__main__":
    asyncio.run(main())
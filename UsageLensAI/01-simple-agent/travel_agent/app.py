import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent

APP_NAME = "usagelens"
USER_ID = "admin"
SESSION_ID = "session1"

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
        session_service=session_service,
    )

    while True:

        question = input("Ask UsageLensAI: ")

        if question.lower() in ["exit", "quit"]:
            break

        message = types.Content(
            role="user",
            parts=[types.Part(text=question)],
        )

        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=message,
        ):
            if event.is_final_response():
                print("\n" + event.content.parts[0].text + "\n")

if __name__ == "__main__":
    asyncio.run(main())
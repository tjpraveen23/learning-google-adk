import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from travel_agent.agent import root_agent
from google.adk.memory import InMemoryMemoryService

APP_NAME = "travelmate"
USER_ID = "praveen_tj"
SESSION_ID = "session_01"

# Day 5: ADK remembers information across multiple sessions using MemoryService
async def main():

    session_service = InMemorySessionService()

    #stores searchable memories that can be recalled in future sessions
    memory_service = InMemoryMemoryService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

   
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service  #Add Memory Service
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

    # Retrieve the completed session before saving it to memory.
    session = await session_service.get_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    )
    
    # Save the completed conversation into long-term memory.
    await memory_service.add_session_to_memory(session)
    print("\nSession added to Memory.")      

    # Search previously stored memories using a query.
    result = await memory_service.search_memory(
            app_name=APP_NAME,
            user_id=USER_ID,
            query="Luxury Hotels"
        )

    print("\n========== Memory Search Result ==========")

    if hasattr(result, "memories"):
        if result.memories:
            for i, memory in enumerate(result.memories, start=1):
                print(f"\nMemory {i}")
                print(memory)
        else:
            print("No memories found.")
    else:
        print(result)

print("==========================================")


if __name__ == "__main__":
    asyncio.run(main())
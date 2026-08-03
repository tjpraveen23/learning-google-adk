import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.memory import InMemoryMemoryService
from travel_agent import weather_agent, hotel_agent, budget_agent, coordinator_agent

APP_NAME = "travelmate"
USER_ID = "praveen_tj"
SESSION_ID = "session_01"


async def main():

    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
   
    weather_runner = Runner(
        agent=weather_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    hotel_runner = Runner(
        agent=hotel_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    budget_runner = Runner(
        agent=budget_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    coordinator_runner = Runner(
        agent=coordinator_agent,
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

        weather = await invoke_agent(
            weather_runner,
            "WeatherAgent",
            prompt
        )

        hotel = await invoke_agent(
            hotel_runner,
            "HotelAgent",
            prompt
        )

        budget = await invoke_agent(
            budget_runner,
            "BudgetAgent",
            prompt
        )   

        final_prompt = f"""
            User Request  
            {prompt}

            Weather Agent   
            {weather}

            Hotel Agent
            {hotel}

            Budget Agent
            {budget}

            Prepare one complete travel recommendation.
            """       
        final = await invoke_agent(
                coordinator_runner,
                "TravelCoordinator",
                final_prompt )           

async def invoke_agent(
    runner,
    agent_name,
    prompt,
):

    print("\n" + "=" * 70)
    print(f"Invoking : {agent_name}")
    print("=" * 70)

    user_message = types.Content(
        role="user",
        parts=[
            types.Part(text=prompt)
        ]
    )

    response = ""

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message,
    ):

        if event.is_final_response() and event.content:
            response = event.content.parts[0].text

    print(f"\n{agent_name} Response")
    print("-" * 70)
    print(response)

    return response

if __name__ == "__main__":
    asyncio.run(main())
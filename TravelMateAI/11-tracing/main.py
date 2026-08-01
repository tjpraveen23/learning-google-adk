import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from travel_agent.agent import root_agent
from travel_agent.simple_console_exporter import SimpleConsoleExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor, ConsoleSpanExporter)

APP_NAME = "travelmate"
USER_ID = "praveen_tj"
SESSION_ID = "session_01"

trace_provider = TracerProvider()

trace_provider.add_span_processor(BatchSpanProcessor(SimpleConsoleExporter()))

trace.set_tracer_provider(trace_provider)

tracer = trace.get_tracer("travelmate")

# Day 11: using Opentelementry (an open source observability framework). You can add span on each tool to trace the duration. 
#         Refer custom simple_console_exporter.py. Arize AI built on top of this framework for UI representation
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
            if event.is_final_response():
                print(event.content.parts[0].text)  

if __name__ == "__main__":
    asyncio.run(main())
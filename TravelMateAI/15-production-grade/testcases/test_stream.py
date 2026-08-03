import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from travel_agent.orchestrator import process_travel_request_stream

async def main():

    async for event in process_travel_request_stream(
        prompt="Plan a Chennai trip under 20000",
        user_id="praveen_tj",
    ):
        print(event)

asyncio.run(main())
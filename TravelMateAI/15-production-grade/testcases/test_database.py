import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from travel_agent.database import get_or_create_session

async def main():

    session_service, session = await get_or_create_session(
        user_id="praveen_tj"
    )

    print("Session ID:", session.id)
    print("State:", session.state)

if __name__ == "__main__":
    asyncio.run(main())
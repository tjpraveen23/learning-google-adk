import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from travel_agent.tools import get_weather

async def main():

    print("First call (should take ~5 sec)")
    result = await get_weather("Goa")
    print(result)

    print()

    print("Second call (should be cached)")
    result = await get_weather("Goa")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
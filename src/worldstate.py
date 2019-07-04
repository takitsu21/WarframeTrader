import asyncio, nest_asyncio, json
from aiohttp import ClientSession
from src.exceptions import *

def run(func = lambda x: x):
    """asyncio runner function using python 3.7"""
    return asyncio.run(func)

class WorldState:
    """Warframe worldstate data (alerts, cetusCycle, etc...)"""
    def __init__(self):
        self.root = "https://api.warframestat.us/"


    async def fetch(self, session, endpoint: str):
        async with session.get(self.root + endpoint) as r:
            try:
                return await r.json()
            except Exception:
                raise StatusError(await r.json(), r.status)

    async def data(self, platform: str, *endpoints: list) -> dict:
        endpoint = platform + "/" + '/'.join(endpoints)
        async with ClientSession(json_serialize=json.dumps) as session:
            responses = await self.fetch(session, endpoint)
        return responses

# if __name__ == "__main__":
#     worldstate = WorldState()
#     print(run(worldstate.data("pc","cetusCycle")))
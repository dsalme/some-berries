from httpx import AsyncClient
import os

POKE_BERRIES_ROOT_URL = os.getenv("POKE_BERRIES_ROOT_URL")

HEADERS = {
    'Content-Type': 'application/json'
}

class BerriesClient:
    def __init__(self):
        self.session = AsyncClient(
            headers=HEADERS,
            base_url=POKE_BERRIES_ROOT_URL,
        )

    async def get_berries(self):
        berries = await self.session.get('/api/v2/berry')
        berries.raise_for_status()
        return berries


client = BerriesClient()

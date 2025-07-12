import logging

import httpx

from bot.types import SendMessage


log = logging.getLogger(__name__)


class NapCatClient:
    def __init__(self, api: str, timeout: int = 300):
        self.api = api
        self.client = httpx.AsyncClient(timeout=timeout)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()

    async def send(self, message: SendMessage) -> dict:
        log.info(message.model_dump_json(indent=4))
        response = await self.client.post(
            f"{self.api}/send_msg",
            json=message.model_dump(),
        )
        assert response.is_success
        return response.json()

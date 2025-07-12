import asyncio

from fastapi import FastAPI

from bot.api import router
from bot.plugins import command


async def lifespan(app: FastAPI):
    async with command:
        asyncio.create_task(command.arun())
        yield
        command.stop()


app = FastAPI(lifespan=lifespan)
app.include_router(router)

import asyncio
import logging
import traceback

from fastapi import APIRouter, Body

from bot.plugins import command
from bot.types import ReceiveMessage


router = APIRouter()
log = logging.getLogger(__name__)


@router.post(
    "",
    description="消息上报",
)
async def receive(message: dict = Body()):
    try:
        receive: ReceiveMessage = ReceiveMessage.model_validate(message)
        await asyncio.wait_for(command.put(receive), timeout=1)
    except ValueError:
        pass
    except Exception:
        log.error(traceback.format_exc())
    return "ok"

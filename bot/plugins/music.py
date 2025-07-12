import logging

import httpx

from bot.command import Command
from bot.napcat import NapCatClient
from bot.types import ReceiveMessage, SendMessage, MusicMessage


command = Command()
log = logging.getLogger(__name__)


@command("点歌.*?")
async def card(napcat: NapCatClient, receive: ReceiveMessage):
    keyword = receive.content.removeprefix("点歌").strip()
    url = f"https://www.hhlqilongzhu.cn/api/joox/juhe_music.php?msg={keyword}&type=json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        songid = None
        for music in response.json():
            if music["app"] == "wy":
                songid = music["songid"]
                break
    if songid:
        await napcat.send(
            SendMessage(
                user_id=receive.user_id,
                group_id=receive.group_id,
                message_type=receive.message_type,
                message=MusicMessage.from_music(
                    type="163",
                    id=str(songid),
                ),
            )
        )

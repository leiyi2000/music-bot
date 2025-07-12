from typing import Callable, Any, List, Dict

import re
import asyncio
import logging

from bot.napcat import NapCatClient
from bot.settings import NAPCAT_API
from bot.types import ReceiveMessage


log = logging.getLogger(__name__)


class Route:
    def __init__(
        self,
        name: str,
        pattern: re.Pattern,
        func: Callable[..., Any],
        func_kwargs: Dict[str, Any],
    ) -> None:
        self.name = name
        self.pattern = pattern
        self.func = func
        self.func_kwargs = func_kwargs

    async def match(self, receive: ReceiveMessage) -> bool:
        for message in receive.message:
            if getattr(message, "type") == "text" and self.pattern.match(
                message.data.text
            ):
                receive.content = message.data.text
                return True
        return False


class Command:
    def __init__(self):
        self._stop = asyncio.Event()
        self.routes: List[Route] = []
        self.client = NapCatClient(NAPCAT_API)
        self.queue = asyncio.Queue(maxsize=1024)

    def add_route(self, route: Route):
        self.routes.append(route)

    async def put(self, receive: ReceiveMessage):
        await self.queue.put(receive)

    def stop(self):
        self._stop.set()

    def __call__(
        self,
        pattern: str,
        *,
        name: str = None,
        func_kwargs: Dict[str, Any] = {},
    ):
        """command装饰器.

        Args:
            pattern (str): 指令正则匹配.
            func (Callable[..., Any]): 命令处理函数.
            name (str, optional): 名称.
            func_kwargs (Dict[str, Any], optional): func额外参数.
        """

        def decorator(func: Callable[..., Any]):
            route = Route(
                name or getattr(func, "__name__", "unknown"),
                re.compile(pattern),
                func,
                func_kwargs,
            )
            self.add_route(route)
            return func

        return decorator

    async def match(self, receive: ReceiveMessage) -> Route | None:
        for route in self.routes:
            if await route.match(receive):
                return route

    def include_command(self, command: "Command"):
        for route in command.routes:
            self.add_route(route)

    async def __aenter__(self):
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.__aexit__(exc_type, exc_value, traceback)

    async def arun(self):
        async with asyncio.TaskGroup() as tg:
            while not self._stop.is_set():
                receive: ReceiveMessage = await self.queue.get()
                log.info(f"receive: {receive.model_dump_json(indent=4)}")
                if route := await self.match(receive):
                    task = route.func(self.client, receive, **route.func_kwargs)
                    tg.create_task(task)
                if tg._errors:
                    tg._errors.clear()

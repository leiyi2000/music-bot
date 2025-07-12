from fastapi import APIRouter

from bot.api import message


router = APIRouter()


@router.get("/health", description="健康检查", tags=["探针"])
async def health():
    return True


router.include_router(
    message.router,
    prefix="/message",
    tags=["消息上报"],
)

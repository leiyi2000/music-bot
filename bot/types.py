from typing import List, Literal

from pydantic import BaseModel


class TextMessageData(BaseModel):
    text: str


class MusicMessageData(BaseModel):
    id: str | None = None
    url: str | None = None
    image: str | None = None
    singer: str | None = None
    title: str | None = None
    content: str | None = None
    type: Literal["qq", "163", "kugou", "migu", "kuwo", "custom"]


class RecordMessageData(BaseModel):
    # 语音文件路径、URL 或 Base64 编码
    file: str


class TextMessage(BaseModel):
    type: Literal["text"] = "text"
    data: TextMessageData

    @classmethod
    def from_text(cls, text: str):
        return cls(data=TextMessageData(text=text))


class MusicMessage(BaseModel):
    type: Literal["music"] = "music"
    data: MusicMessageData

    @classmethod
    def from_music(
        cls,
        type: Literal["qq", "163", "kugou", "migu", "kuwo", "custom"],
        id: str | None = None,
        url: str | None = None,
        image: str | None = None,
        singer: str | None = None,
        title: str | None = None,
        content: str | None = None,
    ):
        return cls(
            data=MusicMessageData(
                id=id,
                type=type,
                url=url,
                image=image,
                singer=singer,
                title=title,
                content=content,
            )
        )


class RecordMessage(BaseModel):
    type: Literal["record"] = "record"
    data: RecordMessageData

    @classmethod
    def from_record(cls, file: str):
        return cls(data=RecordMessageData(file=file))


class ReceiveMessage(BaseModel):
    user_id: int | None = None
    group_id: int | None = None
    message_type: Literal["private", "group"]
    message: List[TextMessage]
    time: int
    content: str | None = None


class SendMessage(BaseModel):
    user_id: int | None = None
    group_id: int | None = None
    message_type: Literal["private", "group"]
    message: TextMessage | MusicMessage | RecordMessage

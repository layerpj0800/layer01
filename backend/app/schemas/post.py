from typing import Literal

from pydantic import BaseModel


class PostBase(BaseModel):
    channel_id: int
    content: str
    type: Literal["general", "stock-briefing"]


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True

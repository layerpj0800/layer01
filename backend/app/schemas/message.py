from pydantic import BaseModel


class MessageBase(BaseModel):
    content: str
    pinned: bool = False
    attachment: str | None = None


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int

    class Config:
        orm_mode = True

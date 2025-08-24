from pydantic import BaseModel


class ChannelBase(BaseModel):
    title: str
    is_private: bool = False


class ChannelCreate(ChannelBase):
    pass


class ChannelRead(ChannelBase):
    id: int
    creator_id: int

    class Config:
        orm_mode = True

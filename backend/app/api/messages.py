import asyncio
import json

from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageRead

router = APIRouter(prefix="/messages", tags=["messages"])

listeners: list[asyncio.Queue] = []


@router.get("/", response_model=list[MessageRead])
async def get_messages(session: AsyncSession = Depends(get_session)) -> list[MessageRead]:
    result = await session.execute(select(Message).order_by(Message.id))
    return [MessageRead.from_orm(m) for m in result.scalars().all()]


@router.post("/", response_model=MessageRead)
async def send_message(
    data: MessageCreate, session: AsyncSession = Depends(get_session)
) -> MessageRead:
    message = Message(**data.dict())
    session.add(message)
    await session.commit()
    await session.refresh(message)
    message_read = MessageRead.from_orm(message)
    for queue in listeners:
        await queue.put(message_read.dict())
    return message_read


@router.get("/stream")
async def stream() -> EventSourceResponse:
    queue: asyncio.Queue = asyncio.Queue()
    listeners.append(queue)

    async def event_generator():
        try:
            while True:
                data = await queue.get()
                yield {
                    "event": "message",
                    "data": json.dumps(data),
                }
        finally:
            listeners.remove(queue)

    return EventSourceResponse(event_generator())

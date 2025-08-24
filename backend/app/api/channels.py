from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import require_role, require_subscriber
from app.core.database import get_session
from app.models.channel import Channel
from app.schemas.channel import ChannelCreate, ChannelRead

router = APIRouter(prefix="/channels", tags=["channels"])


@router.get("/", response_model=list[ChannelRead])
async def list_channels(
    session: AsyncSession = Depends(get_session),
    user=Depends(require_subscriber),
):
    result = await session.execute(select(Channel))
    return result.scalars().all()


@router.post("/", response_model=ChannelRead)
async def create_channel(
    payload: ChannelCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_role("creator")),
):
    channel = Channel(creator_id=user.id, **payload.dict())
    session.add(channel)
    await session.commit()
    await session.refresh(channel)
    return channel


@router.put("/{channel_id}", response_model=ChannelRead)
async def update_channel(
    channel_id: int,
    payload: ChannelCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_role("creator")),
):
    channel = await session.get(Channel, channel_id)
    if channel is None or channel.creator_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
    for field, value in payload.dict().items():
        setattr(channel, field, value)
    await session.commit()
    await session.refresh(channel)
    return channel


@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(
    channel_id: int,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_role("creator")),
):
    channel = await session.get(Channel, channel_id)
    if channel is None or channel.creator_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
    await session.delete(channel)
    await session.commit()

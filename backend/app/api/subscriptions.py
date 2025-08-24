from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import get_current_user, require_role
from app.core.database import get_session
from app.models.channel import Channel
from app.models.plan import Plan
from app.models.subscription import Subscription
from app.schemas.subscription import (
    PlanCreate,
    PlanRead,
    SubscriptionCreate,
    SubscriptionRead,
)

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.post("/plans", response_model=PlanRead)
async def create_plan(
    payload: PlanCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_role("creator")),
):
    result = await session.execute(
        select(Channel).where(Channel.id == payload.channel_id)
    )
    channel = result.scalar_one_or_none()
    if channel is None or channel.creator_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
    plan = Plan(**payload.dict())
    session.add(plan)
    await session.commit()
    await session.refresh(plan)
    return plan


@router.post("/", response_model=SubscriptionRead)
async def subscribe(
    payload: SubscriptionCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    result = await session.execute(select(Plan).where(Plan.id == payload.plan_id))
    plan = result.scalar_one_or_none()
    if plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    subscription = Subscription(
        user_id=user.id,
        plan_id=plan.id,
        status="active",
        current_period_end=Subscription.default_period_end(),
        merchant_uid=str(uuid4()),
    )
    session.add(subscription)
    await session.commit()
    await session.refresh(subscription)
    return subscription

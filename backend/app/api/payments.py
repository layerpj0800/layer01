from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_session
from app.models.subscription import Subscription
from app.models.payment_event import PaymentEvent
from app.schemas.subscription import IamportWebhook

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/iamport-webhook")
async def iamport_webhook(
    payload: IamportWebhook,
    session: AsyncSession = Depends(get_session),
    x_signature: str = Header(..., alias="X-Iamport-Signature"),
):
    if x_signature != settings.iamport_webhook_secret:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid signature")

    result = await session.execute(
        select(Subscription).where(Subscription.merchant_uid == payload.merchant_uid)
    )
    subscription = result.scalar_one_or_none()
    if subscription:
        subscription.status = payload.status
    event = PaymentEvent(
        provider="iamport",
        type=payload.status,
        payload_json=payload.dict(),
        subscription_id=subscription.id if subscription else None,
    )
    session.add(event)
    await session.commit()
    return {"ok": True}

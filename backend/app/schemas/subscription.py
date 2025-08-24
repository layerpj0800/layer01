from datetime import datetime

from pydantic import BaseModel


class PlanCreate(BaseModel):
    channel_id: int
    price: int
    interval: str = "month"
    trial_days: int = 0


class PlanRead(PlanCreate):
    id: int

    class Config:
        orm_mode = True


class SubscriptionCreate(BaseModel):
    plan_id: int


class SubscriptionRead(BaseModel):
    id: int
    plan_id: int
    status: str
    current_period_end: datetime
    merchant_uid: str

    class Config:
        orm_mode = True


class IamportWebhook(BaseModel):
    merchant_uid: str
    status: str
    imp_uid: str | None = None
    # Add any additional fields you require from Iamport webhook payload

from datetime import datetime, timedelta

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    plan_id: Mapped[int] = mapped_column(ForeignKey("plans.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(20), default="active")
    current_period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    merchant_uid: Mapped[str] = mapped_column(String(255), unique=True)

    @staticmethod
    def default_period_end() -> datetime:
        return datetime.utcnow() + timedelta(days=30)

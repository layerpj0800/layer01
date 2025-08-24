from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id", ondelete="CASCADE"))
    price: Mapped[int] = mapped_column(Integer)
    interval: Mapped[str] = mapped_column(String(20), default="month")
    trial_days: Mapped[int] = mapped_column(Integer, default=0)

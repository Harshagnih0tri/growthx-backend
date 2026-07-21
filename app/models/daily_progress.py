"""Daily Progress database model."""

import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class DailyProgress(Base):
    __tablename__ = "daily_progress"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    progress_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    study_hours: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    gym_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    walk_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    water_intake: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    sleep_hours: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    weight: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
    )

    user = relationship(
        "User",
        back_populates="daily_progress",
    )
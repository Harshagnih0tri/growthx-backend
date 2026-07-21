"""Repository layer for Daily Progress."""

import uuid

from sqlalchemy.orm import Session

from app.models.daily_progress import DailyProgress
from app.models.user import User
from app.schemas.daily_progress import (
    DailyProgressCreate,
    DailyProgressUpdate,
)


def create_progress(
    db: Session,
    current_user: User,
    payload: DailyProgressCreate,
) -> DailyProgress:
    progress = DailyProgress(
        user_id=current_user.id,
        **payload.model_dump(),
    )

    db.add(progress)
    db.commit()
    db.refresh(progress)

    return progress


def get_all_progress(
    db: Session,
    current_user: User,
) -> list[DailyProgress]:
    return (
        db.query(DailyProgress)
        .filter(DailyProgress.user_id == current_user.id)
        .order_by(DailyProgress.progress_date.desc())
        .all()
    )


def get_progress_by_id(
    db: Session,
    current_user: User,
    progress_id: uuid.UUID,
) -> DailyProgress | None:
    return (
        db.query(DailyProgress)
        .filter(
            DailyProgress.id == progress_id,
            DailyProgress.user_id == current_user.id,
        )
        .first()
    )


def update_progress(
    db: Session,
    progress: DailyProgress,
    payload: DailyProgressUpdate,
) -> DailyProgress:
    update_data = payload.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(progress, key, value)

    db.commit()
    db.refresh(progress)

    return progress


def delete_progress(
    db: Session,
    progress: DailyProgress,
) -> None:
    db.delete(progress)
    db.commit()
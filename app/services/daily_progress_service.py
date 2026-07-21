"""Business logic for Daily Progress."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User

from app.repositories.daily_progress_repository import (
    create_progress,
    delete_progress,
    get_all_progress,
    get_progress_by_id,
    update_progress,
)

from app.schemas.daily_progress import (
    DailyProgressCreate,
    DailyProgressRead,
    DailyProgressUpdate,
)


def create_new_progress(
    db: Session,
    current_user: User,
    payload: DailyProgressCreate,
) -> DailyProgressRead:
    progress = create_progress(
        db,
        current_user,
        payload,
    )

    return DailyProgressRead.model_validate(progress)


def list_user_progress(
    db: Session,
    current_user: User,
) -> list[DailyProgressRead]:
    progress = get_all_progress(
        db,
        current_user,
    )

    return [
        DailyProgressRead.model_validate(item)
        for item in progress
    ]


def get_single_progress(
    db: Session,
    current_user: User,
    progress_id: uuid.UUID,
) -> DailyProgressRead:
    progress = get_progress_by_id(
        db,
        current_user,
        progress_id,
    )

    if progress is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daily progress not found",
        )

    return DailyProgressRead.model_validate(progress)


def update_existing_progress(
    db: Session,
    current_user: User,
    progress_id: uuid.UUID,
    payload: DailyProgressUpdate,
) -> DailyProgressRead:
    progress = get_progress_by_id(
        db,
        current_user,
        progress_id,
    )

    if progress is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daily progress not found",
        )

    progress = update_progress(
        db,
        progress,
        payload,
    )

    return DailyProgressRead.model_validate(progress)


def delete_user_progress(
    db: Session,
    current_user: User,
    progress_id: uuid.UUID,
) -> None:
    progress = get_progress_by_id(
        db,
        current_user,
        progress_id,
    )

    if progress is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daily progress not found",
        )

    delete_progress(
        db,
        progress,
    )
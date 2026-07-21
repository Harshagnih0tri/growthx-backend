"""API routes for Daily Progress."""

import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.daily_progress import (
    DailyProgressCreate,
    DailyProgressRead,
    DailyProgressUpdate,
)

from app.services.daily_progress_service import (
    create_new_progress,
    delete_user_progress,
    get_single_progress,
    list_user_progress,
    update_existing_progress,
)

router = APIRouter(
    prefix="/daily-progress",
    tags=["Daily Progress"],
)


@router.post(
    "",
    response_model=DailyProgressRead,
    status_code=status.HTTP_201_CREATED,
)
def create_progress(
    payload: DailyProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_new_progress(
        db,
        current_user,
        payload,
    )


@router.get(
    "",
    response_model=list[DailyProgressRead],
)
def get_all_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_user_progress(
        db,
        current_user,
    )


@router.get(
    "/{progress_id}",
    response_model=DailyProgressRead,
)
def get_progress(
    progress_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_single_progress(
        db,
        current_user,
        progress_id,
    )


@router.put(
    "/{progress_id}",
    response_model=DailyProgressRead,
)
def update_progress(
    progress_id: uuid.UUID,
    payload: DailyProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_existing_progress(
        db,
        current_user,
        progress_id,
        payload,
    )


@router.delete(
    "/{progress_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_progress(
    progress_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_user_progress(
        db,
        current_user,
        progress_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
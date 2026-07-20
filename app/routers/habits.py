"""Habit CRUD endpoints — all scoped to the authenticated user."""

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitUpdate, HabitRead
from app.services.habit_service import (
    create_new_habit,
    list_user_habits,
    get_single_habit,
    update_existing_habit,
    delete_user_habit,
)

router = APIRouter(prefix="/habits", tags=["Habits"])


@router.post("/", response_model=HabitRead, status_code=status.HTTP_201_CREATED)
def create_habit_endpoint(
    payload: HabitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_new_habit(db, current_user, payload)


@router.get("/", response_model=list[HabitRead])
def list_habits_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_user_habits(db, current_user)


@router.get("/{habit_id}", response_model=HabitRead)
def get_habit_endpoint(
    habit_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_single_habit(db, current_user, habit_id)


@router.put("/{habit_id}", response_model=HabitRead)
def update_habit_endpoint(
    habit_id: uuid.UUID,
    payload: HabitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_existing_habit(db, current_user, habit_id, payload)


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit_endpoint(
    habit_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_user_habit(db, current_user, habit_id)
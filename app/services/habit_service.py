"""Business logic for habit CRUD, scoped to the authenticated user."""

import uuid

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.habit import Habit
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitUpdate
from app.repositories.habit_repository import (
    create_habit,
    get_habits_by_user,
    get_habit_by_id,
    update_habit,
    delete_habit,
)


def create_new_habit(db: Session, current_user: User, payload: HabitCreate) -> Habit:
    """Create a habit owned by the currently authenticated user."""
    return create_habit(
        db,
        user_id=current_user.id,
        name=payload.name,
        description=payload.description,
        frequency=payload.frequency,
    )


def list_user_habits(db: Session, current_user: User) -> list[Habit]:
    """Return all habits belonging to the currently authenticated user."""
    return get_habits_by_user(db, current_user.id)


def get_single_habit(db: Session, current_user: User, habit_id: uuid.UUID) -> Habit:
    """Fetch one habit, raising 404 if it doesn't exist or isn't owned by this user."""
    habit = get_habit_by_id(db, habit_id, current_user.id)
    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )
    return habit


def update_existing_habit(
    db: Session, current_user: User, habit_id: uuid.UUID, payload: HabitUpdate
) -> Habit:
    """Update only the fields provided, after verifying ownership."""
    habit = get_single_habit(db, current_user, habit_id)

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return habit

    return update_habit(db, habit, updates)


def delete_user_habit(db: Session, current_user: User, habit_id: uuid.UUID) -> None:
    """Delete a habit after verifying ownership."""
    habit = get_single_habit(db, current_user, habit_id)
    delete_habit(db, habit)
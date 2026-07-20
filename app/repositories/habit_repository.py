"""Database access layer for Habit — no business logic here."""

import uuid

from sqlalchemy.orm import Session

from app.models.habit import Habit


def create_habit(db: Session, user_id: uuid.UUID, name: str, description: str | None, frequency: str) -> Habit:
    """Insert a new habit row owned by user_id."""
    habit = Habit(
        user_id=user_id,
        name=name,
        description=description,
        frequency=frequency,
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


def get_habits_by_user(db: Session, user_id: uuid.UUID) -> list[Habit]:
    """Return all habits belonging to a specific user."""
    return db.query(Habit).filter(Habit.user_id == user_id).all()


def get_habit_by_id(db: Session, habit_id: uuid.UUID, user_id: uuid.UUID) -> Habit | None:
    """Fetch a single habit, scoped to its owner. Returns None if not found or not owned."""
    return db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user_id).first()


def update_habit(db: Session, habit: Habit, updates: dict) -> Habit:
    """Apply partial field updates to an existing habit object and persist."""
    for field, value in updates.items():
        setattr(habit, field, value)
    db.commit()
    db.refresh(habit)
    return habit


def delete_habit(db: Session, habit: Habit) -> None:
    """Delete a habit row."""
    db.delete(habit)
    db.commit()
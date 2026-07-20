"""Pydantic schemas for Habit — request/response validation (not DB shape)."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class HabitBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    frequency: str = Field(default="daily", max_length=50)


class HabitCreate(HabitBase):
    pass


class HabitUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    frequency: str | None = Field(default=None, max_length=50)


class HabitRead(HabitBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
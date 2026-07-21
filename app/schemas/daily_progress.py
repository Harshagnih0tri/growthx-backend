"""Pydantic schemas for Daily Progress."""

import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DailyProgressBase(BaseModel):
    progress_date: date
    study_hours: float = 0
    gym_completed: bool = False
    walk_completed: bool = False
    water_intake: float = 0
    sleep_hours: float = 0
    weight: float = 0


class DailyProgressCreate(DailyProgressBase):
    pass


class DailyProgressUpdate(BaseModel):
    progress_date: Optional[date] = None
    study_hours: Optional[float] = None
    gym_completed: Optional[bool] = None
    walk_completed: Optional[bool] = None
    water_intake: Optional[float] = None
    sleep_hours: Optional[float] = None
    weight: Optional[float] = None


class DailyProgressRead(DailyProgressBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
from pydantic import BaseModel
import uuid


class GoalBase(BaseModel):
    target_weight: float
    daily_study_goal: float
    daily_water_goal: float
    daily_sleep_goal: float


class GoalCreate(GoalBase):
    pass


class GoalUpdate(GoalBase):
    pass


class GoalResponse(GoalBase):
    user_id: uuid.UUID

    class Config:
        from_attributes = True
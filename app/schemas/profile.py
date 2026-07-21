import uuid

from pydantic import BaseModel


class ProfileBase(BaseModel):
    age: int
    gender: str
    height: float
    weight: float


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    user_id: uuid.UUID

    class Config:
        from_attributes = True
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile import (
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
)


class ProfileService:

    @staticmethod
    def get_profile(
        db: Session,
        current_user: User,
    ):
        profile = ProfileRepository.get_profile(
            db,
            current_user,
        )

        if not profile:
            return None

        return ProfileResponse.model_validate(profile)

    @staticmethod
    def create_profile(
        db: Session,
        current_user: User,
        profile_data: ProfileCreate,
    ):
        existing_profile = ProfileRepository.get_profile(
            db,
            current_user,
        )

        if existing_profile:
            raise HTTPException(
                status_code=400,
                detail="Profile already exists",
            )

        profile = ProfileRepository.create_profile(
            db,
            current_user,
            profile_data,
        )

        return ProfileResponse.model_validate(profile)

    @staticmethod
    def update_profile(
        db: Session,
        current_user: User,
        profile_data: ProfileUpdate,
    ):
        profile = ProfileRepository.get_profile(
            db,
            current_user,
        )

        if not profile:
            return None

        profile = ProfileRepository.update_profile(
            db,
            profile,
            profile_data,
        )

        return ProfileResponse.model_validate(profile)
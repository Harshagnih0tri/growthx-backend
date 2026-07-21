from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.models.user import User
from app.schemas.profile import ProfileCreate, ProfileUpdate


class ProfileRepository:

    @staticmethod
    def get_profile(
        db: Session,
        current_user: User,
    ):
        return (
            db.query(Profile)
            .filter(Profile.user_id == current_user.id)
            .first()
        )

    @staticmethod
    def create_profile(
        db: Session,
        current_user: User,
        profile_data: ProfileCreate,
    ):
        profile = Profile(
            user_id=current_user.id,
            **profile_data.model_dump(),
        )

        db.add(profile)
        db.commit()
        db.refresh(profile)

        return profile

    @staticmethod
    def update_profile(
        db: Session,
        profile: Profile,
        profile_data: ProfileUpdate,
    ):
        for key, value in profile_data.model_dump().items():
            setattr(profile, key, value)

        db.commit()
        db.refresh(profile)

        return profile
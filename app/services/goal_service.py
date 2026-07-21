from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.goal_repository import GoalRepository
from app.schemas.goal import GoalCreate, GoalResponse, GoalUpdate


class GoalService:

    @staticmethod
    def get_goal(
        db: Session,
        current_user: User,
    ):
        goal = GoalRepository.get_goal(db, current_user)

        if not goal:
            return None

        return GoalResponse.model_validate(goal)

    @staticmethod
    def create_goal(
        db: Session,
        current_user: User,
        goal_data: GoalCreate,
    ):
        # Check if goal already exists
        existing_goal = GoalRepository.get_goal(
            db,
            current_user,
        )

        if existing_goal:
            raise HTTPException(
                status_code=400,
                detail="Goal already exists",
            )

        goal = GoalRepository.create_goal(
            db,
            current_user,
            goal_data,
        )

        return GoalResponse.model_validate(goal)

    @staticmethod
    def update_goal(
        db: Session,
        current_user: User,
        goal_data: GoalUpdate,
    ):
        goal = GoalRepository.get_goal(db, current_user)

        if not goal:
            return None

        goal = GoalRepository.update_goal(
            db,
            goal,
            goal_data,
        )

        return GoalResponse.model_validate(goal)
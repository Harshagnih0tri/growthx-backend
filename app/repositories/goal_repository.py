from sqlalchemy.orm import Session

from app.models.goal import Goal
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalUpdate


class GoalRepository:

    @staticmethod
    def get_goal(db: Session, current_user: User):
        return (
            db.query(Goal)
            .filter(Goal.user_id == current_user.id)
            .first()
        )

    @staticmethod
    def create_goal(
        db: Session,
        current_user: User,
        goal_data: GoalCreate,
    ):
        goal = Goal(
            user_id=current_user.id,
            **goal_data.model_dump(),
        )

        db.add(goal)
        db.commit()
        db.refresh(goal)

        return goal

    @staticmethod
    def update_goal(
        db: Session,
        goal: Goal,
        goal_data: GoalUpdate,
    ):
        for key, value in goal_data.model_dump().items():
            setattr(goal, key, value)

        db.commit()
        db.refresh(goal)

        return goal
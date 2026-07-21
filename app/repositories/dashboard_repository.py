from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.habit import Habit
from app.models.daily_progress import DailyProgress


class DashboardRepository:
    @staticmethod
    def get_dashboard_data(db: Session, current_user: User):
        total_habits = (
            db.query(func.count(Habit.id))
            .filter(Habit.user_id == current_user.id)
            .scalar()
        )

        total_progress_entries = (
            db.query(func.count(DailyProgress.id))
            .filter(DailyProgress.user_id == current_user.id)
            .scalar()
        )

        return {
            "name": current_user.name,
            "total_habits": total_habits,
            "total_progress_entries": total_progress_entries,
        }
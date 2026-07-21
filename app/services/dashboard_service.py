from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.dashboard_repository import DashboardRepository
from app.schemas.dashboard import DashboardResponse


class DashboardService:

    @staticmethod
    def get_dashboard(db: Session, current_user: User):

        data = DashboardRepository.get_dashboard_data(
            db=db,
            current_user=current_user,
        )

        return DashboardResponse(**data)
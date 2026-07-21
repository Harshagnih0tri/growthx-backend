from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalResponse, GoalUpdate
from app.services.goal_service import GoalService

router = APIRouter(
    prefix="/goals",
    tags=["Goals"],
)


@router.get(
    "",
    response_model=GoalResponse,
)
def get_goal(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = GoalService.get_goal(db, current_user)

    if not goal:
        raise HTTPException(
            status_code=404,
            detail="Goal not found",
        )

    return goal


@router.post(
    "",
    response_model=GoalResponse,
)
def create_goal(
    goal_data: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return GoalService.create_goal(
        db,
        current_user,
        goal_data,
    )


@router.put(
    "",
    response_model=GoalResponse,
)
def update_goal(
    goal_data: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = GoalService.update_goal(
        db,
        current_user,
        goal_data,
    )

    if not goal:
        raise HTTPException(
            status_code=404,
            detail="Goal not found",
        )

    return goal
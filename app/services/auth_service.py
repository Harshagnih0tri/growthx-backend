"""Business logic for user registration and login."""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.user_repository import get_user_by_email, create_user
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User


def register_user(db: Session, payload: UserCreate) -> User:
    """Validate uniqueness, hash the password, and persist a new user."""
    existing_user = get_user_by_email(db, payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_pw = hash_password(payload.password)
    return create_user(db, payload.name, payload.email, hashed_pw)


def authenticate_user(db: Session, payload: UserLogin) -> str:
    """Verify credentials, ensure account is active, and return a signed JWT."""
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated",
        )

    return create_access_token(data={"sub": user.email})
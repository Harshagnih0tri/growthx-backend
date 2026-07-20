"""Database access layer for User — no business logic here."""

from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    """Fetch a single user by email, or None if no match."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, name: str, email: str, hashed_password: str) -> User:
    """Insert a new user row and return the persisted object."""
    user = User(name=name, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
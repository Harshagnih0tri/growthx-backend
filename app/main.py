"""
Application entrypoint.

Why this file stays thin:
    main.py should only ASSEMBLE the app — create the FastAPI instance,
    attach middleware, and include routers. It should never contain
    business logic or route handlers directly. That logic lives in
    routers/ + services/, which we add feature by feature.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db, verify_db_connection as check_db, Base, engine
from app.routers import (
    auth,
    users,
    habits,
    daily_progress,
    dashboard,
    goal,
    profile,
    ai,
    conversations,
    documents,
)

# Import every model at least once so Base.metadata knows about all tables
# before create_all() runs on startup.
from app.models.user import User
from app.models.habit import Habit
from app.models.daily_progress import DailyProgress
from app.models.goal import Goal
from app.models.profile import Profile
from app.models.conversation import Conversation, Message
from app.models.document import Document, DocumentChunk

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(habits.router)
app.include_router(daily_progress.router)
app.include_router(dashboard.router)
app.include_router(goal.router)
app.include_router(profile.router)
app.include_router(ai.router)
app.include_router(conversations.router)
app.include_router(documents.router)


@app.on_event("startup")
def on_startup():
    """Fails fast at boot if PostgreSQL is unreachable, instead of failing later on a random request."""
    check_db()
    Base.metadata.create_all(bind=engine)
    print("Database connection verified. Tables ensured.")


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.ENV}


@app.get("/db-health", tags=["System"])
def db_health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
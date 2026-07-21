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
from app.routers import auth, users
from app.routers import auth, users, habits
from app.models.user import User
from app.models.habit import Habit
from app.models.daily_progress import DailyProgress
from app.routers.auth import router as auth_router
from app.routers.habits import router as habit_router
from app.routers.daily_progress import router as daily_progress_router
from app.routers.daily_progress import router as daily_progress_router
...
from app.routers.dashboard import router as dashboard_router
from app.routers.goal import router as goal_router
app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    debug=settings.DEBUG,
)
app.include_router(habits.router)
app.include_router(auth.router)
app.include_router(users.router)

# CORS: required so the Flutter app (running on a different origin/port)
# can call this API. We'll tighten allow_origins to specific domains
# once we deploy — wildcard "*" is fine for local dev only.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(habit_router)
app.include_router(daily_progress_router)
app.include_router(dashboard_router)
app.include_router(goal_router)
@app.on_event("startup")
def on_startup():
    """Fails fast at boot if PostgreSQL is unreachable, instead of failing later on a random request."""
    check_db()
    Base.metadata.create_all(bind=engine)
    print("Database connection verified. Tables ensured.")


@app.get("/health", tags=["System"])
def health_check():
    """
    Basic liveness check — no DB dependency, so it works even before
    PostgreSQL is wired up. Load balancers / uptime monitors hit this
    in production to know the service is alive.
    """
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.ENV}


@app.get("/db-health", tags=["System"])
def db_health_check(db: Session = Depends(get_db)):
    """Confirms the app can actually reach PostgreSQL (runs SELECT 1)."""
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
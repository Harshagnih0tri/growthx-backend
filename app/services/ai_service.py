"""AI service — the only place in the app that talks to the Groq API.

Phase 2 adds context injection: before sending the user's message,
we build a system prompt from their real profile, goals, habits, and
recent daily progress, pulled via the existing repository layer.
"""

from sqlalchemy.orm import Session

from groq import Groq
from fastapi import HTTPException, status

from app.config import settings
from app.models.user import User
from app.repositories.profile_repository import ProfileRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.daily_progress_repository import get_all_progress
from app.repositories.habit_repository import get_habits_by_user

if settings.GROQ_API_KEY:
    client = Groq(api_key=settings.GROQ_API_KEY)
else:
    client = None


def _build_user_context(db: Session, current_user: User) -> str:
    """Gather the user's profile, goals, habits, and recent progress into a text block."""
    lines: list[str] = []

    profile = ProfileRepository.get_profile(db, current_user)
    if profile:
        lines.append(
            f"Profile: age {profile.age}, gender {profile.gender}, "
            f"height {profile.height}cm, weight {profile.weight}kg."
        )
    else:
        lines.append("Profile: not set up yet.")

    goal = GoalRepository.get_goal(db, current_user)
    if goal:
        lines.append(
            f"Goals: target weight {goal.target_weight}kg, "
            f"daily study goal {goal.daily_study_goal}h, "
            f"daily water goal {goal.daily_water_goal}L, "
            f"daily sleep goal {goal.daily_sleep_goal}h."
        )
    else:
        lines.append("Goals: none set yet.")

    habits = get_habits_by_user(db, current_user.id)
    if habits:
        habit_names = ", ".join(f"{h.name} ({h.frequency})" for h in habits)
        lines.append(f"Habits being tracked: {habit_names}.")
    else:
        lines.append("Habits: none tracked yet.")

    recent_progress = get_all_progress(db, current_user)[:5]
    if recent_progress:
        progress_lines = []
        for p in recent_progress:
            progress_lines.append(
                f"{p.progress_date}: study {p.study_hours}h, "
                f"water {p.water_intake}L, sleep {p.sleep_hours}h, "
                f"weight {p.weight}kg, "
                f"gym {'done' if p.gym_completed else 'skipped'}, "
                f"walk {'done' if p.walk_completed else 'skipped'}"
            )
        lines.append("Recent daily progress (most recent first):\n" + "\n".join(progress_lines))
    else:
        lines.append("Daily progress: no entries logged yet.")

    return "\n".join(lines)


def send_chat_message(db: Session, current_user: User, message: str) -> str:
    """Send a user message to Groq, grounded in their real profile/goals/habits/progress."""
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GROQ_API_KEY is not configured on the server.",
        )

    user_context = _build_user_context(db, current_user)

    system_prompt = (
        "You are GrowthX, a personal productivity and self-improvement coach. "
        "You know the following real information about the user you are talking to. "
        "Use it to give specific, personalized advice instead of generic answers. "
        "Do not repeat this data back verbatim unless asked — use it to inform your reply.\n\n"
        f"{user_context}"
    )

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
    )

    return response.choices[0].message.content
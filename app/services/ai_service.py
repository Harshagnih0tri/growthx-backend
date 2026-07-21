"""AI service — the only place in the app that talks to the Groq API."""

from groq import Groq
from fastapi import HTTPException, status

from app.config import settings

if settings.GROQ_API_KEY:
    client = Groq(api_key=settings.GROQ_API_KEY)
else:
    client = None


def send_chat_message(message: str) -> str:
    """Send a single user message to Groq and return the assistant's reply."""
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GROQ_API_KEY is not configured on the server.",
        )

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "user", "content": message},
        ],
    )

    return response.choices[0].message.content
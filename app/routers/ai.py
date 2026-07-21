"""AI chat endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.ai import ChatRequest, ChatResponse
from app.services.ai_service import send_chat_message

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/chat", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reply, conversation_id = send_chat_message(
        db, current_user, payload.message, payload.conversation_id
    )
    return {"reply": reply, "conversation_id": conversation_id}
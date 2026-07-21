"""Endpoints for reading conversation history — listing and detail view."""

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.conversation import ConversationSummary, ConversationDetail
from app.services.conversation_service import list_conversations, get_conversation_detail

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.get("/", response_model=list[ConversationSummary])
def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_conversations(db, current_user)


@router.get("/{conversation_id}", response_model=ConversationDetail)
def get_conversation_by_id(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_conversation_detail(db, current_user, conversation_id)
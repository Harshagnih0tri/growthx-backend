"""Business logic for reading conversation history (listing and detail view)."""

import uuid

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.conversation import Conversation
from app.repositories.conversation_repository import (
    get_conversations_by_user,
    get_conversation,
    get_messages,
)
from app.schemas.conversation import ConversationSummary, ConversationDetail

PREVIEW_LENGTH = 50


def _build_preview(conversation: Conversation) -> str:
    """Return a short preview string from the conversation's first user message."""
    for msg in conversation.messages:
        if msg.role == "user":
            text = msg.content.strip()
            if len(text) > PREVIEW_LENGTH:
                return text[:PREVIEW_LENGTH] + "..."
            return text
    return "New conversation"


def list_conversations(db: Session, current_user: User) -> list[ConversationSummary]:
    """Return a lightweight summary of every conversation belonging to the current user."""
    conversations = get_conversations_by_user(db, current_user.id)

    return [
        ConversationSummary(
            id=conv.id,
            created_at=conv.created_at,
            preview=_build_preview(conv),
        )
        for conv in conversations
    ]


def get_conversation_detail(
    db: Session, current_user: User, conversation_id: uuid.UUID
) -> ConversationDetail:
    """Fetch a single conversation with its full message history."""
    conversation = get_conversation(db, conversation_id, current_user.id)
    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    messages = get_messages(db, conversation.id)

    return ConversationDetail(
        id=conversation.id,
        created_at=conversation.created_at,
        messages=messages,
    )
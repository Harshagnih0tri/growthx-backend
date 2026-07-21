"""Database access layer for Conversation and Message — no business logic here."""

import uuid

from sqlalchemy.orm import Session

from app.models.conversation import Conversation, Message


def create_conversation(db: Session, user_id: uuid.UUID) -> Conversation:
    """Start a new, empty conversation owned by user_id."""
    conversation = Conversation(user_id=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_conversation(db: Session, conversation_id: uuid.UUID, user_id: uuid.UUID) -> Conversation | None:
    """Fetch a conversation, scoped to its owner. Returns None if not found or not owned."""
    return (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == user_id)
        .first()
    )


def add_message(db: Session, conversation_id: uuid.UUID, role: str, content: str) -> Message:
    """Append one message to a conversation."""
    message = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages(db: Session, conversation_id: uuid.UUID) -> list[Message]:
    """Return all messages in a conversation, oldest first."""
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
        .all()
    )

def get_conversations_by_user(db: Session, user_id: uuid.UUID) -> list[Conversation]:
    """Return all conversations belonging to a user, most recent first."""
    return (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
        .all()
    )
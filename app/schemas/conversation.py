"""Pydantic schemas for reading Conversations and Messages."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MessageRead(BaseModel):
    id: uuid.UUID
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationSummary(BaseModel):
    id: uuid.UUID
    created_at: datetime
    preview: str

    model_config = ConfigDict(from_attributes=True)


class ConversationDetail(BaseModel):
    id: uuid.UUID
    created_at: datetime
    messages: list[MessageRead]

    model_config = ConfigDict(from_attributes=True)
import uuid

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    conversation_id: uuid.UUID | None = None


class ChatResponse(BaseModel):
    reply: str
    conversation_id: uuid.UUID

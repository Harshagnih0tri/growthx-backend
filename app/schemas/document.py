"""Pydantic schemas for Document upload and listing."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentRead(BaseModel):
    id: uuid.UUID
    filename: str
    created_at: datetime
    chunk_count: int

    model_config = ConfigDict(from_attributes=True)
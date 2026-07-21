"""Retrieval service — finds the most relevant document chunks for a query.

Simple linear cosine-similarity scan over a user's stored chunks.
No vector index, no external vector DB — fine at this project's scale,
and the natural place to swap in pgvector/a dedicated vector DB later.
"""

import numpy as np
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.document import DocumentChunk
from app.repositories.document_repository import get_chunks_by_user
from app.services.embedding_service import embed_text

TOP_K = 3  # how many chunks to retrieve per question


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Standard cosine similarity between two vectors."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))


def retrieve_relevant_chunks(db: Session, current_user: User, query: str) -> list[DocumentChunk]:
    """Return the top-K most relevant chunks (from this user's documents only) for a query."""
    chunks = get_chunks_by_user(db, current_user.id)
    if not chunks:
        return []

    query_vector = np.array(embed_text(query))

    scored = [
        (chunk, _cosine_similarity(query_vector, np.array(chunk.embedding)))
        for chunk in chunks
    ]
    scored.sort(key=lambda pair: pair[1], reverse=True)

    return [chunk for chunk, _score in scored[:TOP_K]]
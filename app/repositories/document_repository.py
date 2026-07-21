"""Database access layer for Document and DocumentChunk — no business logic here."""

import uuid

from sqlalchemy.orm import Session

from app.models.document import Document, DocumentChunk


def create_document(db: Session, user_id: uuid.UUID, filename: str) -> Document:
    """Create a new (initially empty) Document row."""
    document = Document(user_id=user_id, filename=filename)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def add_chunks(
    db: Session,
    document_id: uuid.UUID,
    user_id: uuid.UUID,
    chunks: list[str],
    embeddings: list[list[float]],
) -> list[DocumentChunk]:
    """Bulk-insert chunks + their embeddings for a document."""
    chunk_rows = [
        DocumentChunk(
            document_id=document_id,
            user_id=user_id,
            chunk_index=i,
            content=chunk_text,
            embedding=embedding,
        )
        for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings))
    ]
    db.add_all(chunk_rows)
    db.commit()
    return chunk_rows


def get_documents_by_user(db: Session, user_id: uuid.UUID) -> list[Document]:
    """Return all documents belonging to a user, most recent first."""
    return (
        db.query(Document)
        .filter(Document.user_id == user_id)
        .order_by(Document.created_at.desc())
        .all()
    )


def get_chunks_by_user(db: Session, user_id: uuid.UUID) -> list[DocumentChunk]:
    """Return every chunk (across all documents) belonging to a user — used for retrieval."""
    return db.query(DocumentChunk).filter(DocumentChunk.user_id == user_id).all()
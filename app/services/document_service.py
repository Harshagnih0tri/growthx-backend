"""Business logic for uploading and processing documents (the ingestion side of RAG)."""

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from pypdf import PdfReader
import io

from app.models.user import User
from app.repositories.document_repository import (
    create_document,
    add_chunks,
    get_documents_by_user,
)
from app.services.embedding_service import embed_texts
from app.schemas.document import DocumentRead

CHUNK_SIZE = 500  # characters per chunk — simple fixed-size splitting, no overlap tuning


def _extract_text(file_bytes: bytes) -> str:
    """Extract all text from a PDF's raw bytes."""
    reader = PdfReader(io.BytesIO(file_bytes))
    pages_text = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages_text)


def _chunk_text(text: str) -> list[str]:
    """Split text into fixed-size chunks, dropping empty/whitespace-only ones."""
    raw_chunks = [text[i : i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
    return [c.strip() for c in raw_chunks if c.strip()]


def upload_document(db: Session, current_user: User, file: UploadFile) -> DocumentRead:
    """Extract, chunk, embed, and persist an uploaded PDF."""
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported.",
        )

    file_bytes = file.file.read()
    text = _extract_text(file_bytes)

    if not text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No extractable text found in this PDF (it may be a scanned image).",
        )

    chunks = _chunk_text(text)
    embeddings = embed_texts(chunks)

    document = create_document(db, current_user.id, file.filename)
    add_chunks(db, document.id, current_user.id, chunks, embeddings)

    return DocumentRead(
        id=document.id,
        filename=document.filename,
        created_at=document.created_at,
        chunk_count=len(chunks),
    )


def list_documents(db: Session, current_user: User) -> list[DocumentRead]:
    """Return all documents belonging to the current user, with chunk counts."""
    documents = get_documents_by_user(db, current_user.id)
    return [
        DocumentRead(
            id=doc.id,
            filename=doc.filename,
            created_at=doc.created_at,
            chunk_count=len(doc.chunks),
        )
        for doc in documents
    ]
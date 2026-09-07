"""Embedding service — wraps Google's Gemini embeddings API.

Was a locally-loaded sentence-transformers model. That pulled in
PyTorch + transformers + scikit-learn/scipy (a few hundred MB to 1GB+
just to import and load weights), which doesn't fit in a 512MB
free-tier deployment. Swapped to a hosted API call instead — same
public interface (embed_text/embed_texts) so nothing else in the app
(retrieval_service.py, document_service.py) needed to change.
"""

from google import genai
from google.genai import types

from app.config import settings

_client: genai.Client | None = None

EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSIONS = 768  # smaller than the 3072 default -> faster linear scan, less DB storage


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def embed_text(text: str) -> list[float]:
    """Embed a single string — used for the user's query at retrieval time."""
    result = _get_client().models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=EMBEDDING_DIMENSIONS,
        ),
    )
    return list(result.embeddings[0].values)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed multiple strings at once — used for document chunks at ingestion time.

    One call, one embedding per item (contents=list[str] -> one embedding
    per element), which is what the ingestion side needs.
    """
    result = _get_client().models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=EMBEDDING_DIMENSIONS,
        ),
    )
    return [list(e.values) for e in result.embeddings]

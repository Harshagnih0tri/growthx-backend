"""Embedding service — wraps a local sentence-transformers model.

Kept isolated in its own file, same reasoning as ai_service.py isolating
the LLM provider: if we ever swap embedding models/providers, only
this file changes.
"""

from sentence_transformers import SentenceTransformer

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    """Load the embedding model once, on first use, then reuse it (it's slow to load)."""
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_text(text: str) -> list[float]:
    """Turn a single string into a fixed-length embedding vector."""
    model = _get_model()
    vector = model.encode(text, convert_to_numpy=True)
    return vector.tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed multiple strings at once (more efficient than calling embed_text in a loop)."""
    model = _get_model()
    vectors = model.encode(texts, convert_to_numpy=True)
    return vectors.tolist()
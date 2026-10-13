"""Shared vector store — proxy to app.db.vector_store."""
from app.db.vector_store import get_vectorstore, get_embeddings  # noqa: F401

__all__ = ["get_vectorstore", "get_embeddings"]

"""Shared RAG service — proxy to app.services.rag_service."""
from app.services.rag_service import get_course_context  # noqa: F401

__all__ = ["get_course_context"]

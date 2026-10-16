"""Shared utilities for all Maguru AI Agents."""
from .config import settings
from .llm import get_llm, get_llm_pool
from .checkpointer import get_checkpointer, close_checkpointer
from .store import get_store, close_store, get_student_profile, update_student_profile
from .vector_store import get_vectorstore, get_embeddings
from .rag_service import get_course_context

__all__ = [
    "settings",
    "get_llm", "get_llm_pool",
    "get_checkpointer", "close_checkpointer",
    "get_store", "close_store",
    "get_student_profile", "update_student_profile",
    "get_vectorstore", "get_embeddings",
    "get_course_context",
]

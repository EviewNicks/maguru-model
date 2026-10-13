"""Shared LLM provider — proxy to app.core.llm."""
from app.core.llm import get_llm, get_llm_pool  # noqa: F401

__all__ = ["get_llm", "get_llm_pool"]

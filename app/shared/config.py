"""Shared config — proxy to app.core.config (single source of truth)."""
from app.core.config import settings  # noqa: F401

__all__ = ["settings"]

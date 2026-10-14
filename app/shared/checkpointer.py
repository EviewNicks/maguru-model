"""Shared checkpointer — proxy to app.db.checkpointer."""
from app.db.checkpointer import get_checkpointer, close_checkpointer  # noqa: F401

__all__ = ["get_checkpointer", "close_checkpointer"]

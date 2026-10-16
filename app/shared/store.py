"""Shared store — proxy to app.db.store."""
from app.db.store import (
    get_store,
    close_store,
    get_student_profile,
    update_student_profile,
)

__all__ = [
    "get_store",
    "close_store",
    "get_student_profile",
    "update_student_profile",
]

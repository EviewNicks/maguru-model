"""
Unit and integration tests for LangGraph Store provider and cross-thread student memory.
Tests verify:
- Store initialization with singleton pattern
- Graceful fallback to InMemoryStore when requested or on connection failure
- Student profile persistence and retrieval across different thread_ids
- Safe closure of the store connection pool on application shutdown
"""
from unittest.mock import patch, MagicMock
import pytest
from langgraph.store.memory import InMemoryStore
from app.db.store import (
    get_store,
    close_store,
    get_student_profile,
    update_student_profile,
)
import app.db.store as store_module


@pytest.fixture(autouse=True)
def reset_store_state():
    """Ensure store singletons are reset before and after each test."""
    close_store()
    store_module._in_memory_store = None
    store_module._postgres_store = None
    store_module._postgres_store_pool = None
    yield
    close_store()
    store_module._in_memory_store = None
    store_module._postgres_store = None
    store_module._postgres_store_pool = None


def test_fallback_to_in_memory_store_when_forced(monkeypatch):
    """Verify that FORCE_MEMORY_STORE=1 forces InMemoryStore fallback."""
    monkeypatch.setenv("FORCE_MEMORY_STORE", "1")
    store = get_store()
    assert isinstance(store, InMemoryStore)


def test_fallback_to_in_memory_store_when_no_db_url(monkeypatch):
    """Verify InMemoryStore is returned when DATABASE_URL is empty."""
    monkeypatch.setattr(store_module.settings, "DATABASE_URL", "")
    monkeypatch.setenv("DATABASE_URL", "")
    store = get_store()
    assert isinstance(store, InMemoryStore)


def test_fallback_to_in_memory_store_on_connection_error(monkeypatch):
    """Verify InMemoryStore is returned if Postgres connection pool throws an exception."""
    monkeypatch.setattr(store_module.settings, "DATABASE_URL", "postgresql://invalid:5432/bad")
    with patch("psycopg_pool.ConnectionPool", side_effect=Exception("Connection refused")):
        store = get_store()
        assert isinstance(store, InMemoryStore)


def test_student_profile_put_and_get():
    """Verify updating and retrieving student learning profile."""
    student_id = "test-student-42"
    updates = {
        "weaknesses": ["nested_loops", "recursion"],
        "mastered": ["variables", "if_else"],
        "learning_style": "analogy-first",
    }

    updated = update_student_profile(student_id, updates)
    assert updated["weaknesses"] == ["nested_loops", "recursion"]
    assert updated["learning_style"] == "analogy-first"

    retrieved = get_student_profile(student_id)
    assert retrieved == updated


def test_student_profile_cross_thread_memory():
    """Verify that student profile is retained across multiple distinct thread_ids."""
    student_id = "student-cross-thread"
    update_student_profile(student_id, {"weaknesses": ["list_comprehensions"]})

    # Thread 1 accesses profile
    prof_thread_1 = get_student_profile(student_id)
    assert prof_thread_1.get("weaknesses") == ["list_comprehensions"]

    # Thread 2 modifies profile
    update_student_profile(student_id, {"mastered": ["tuples"]})

    # Thread 3 accesses merged profile
    prof_thread_3 = get_student_profile(student_id)
    assert prof_thread_3.get("weaknesses") == ["list_comprehensions"]
    assert prof_thread_3.get("mastered") == ["tuples"]


def test_close_store_cleans_pool():
    """Verify close_store closes the active connection pool without errors."""
    mock_pool = MagicMock()
    store_module._postgres_store_pool = mock_pool
    store_module._postgres_store = MagicMock()

    close_store()

    mock_pool.close.assert_called_once()
    assert store_module._postgres_store_pool is None
    assert store_module._postgres_store is None

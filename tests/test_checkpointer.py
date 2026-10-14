"""
Unit tests for LangGraph Checkpointer Provider and connection pooling.
Tests verify:
- PostgresSaver instantiation with connection pooling
- Graceful fallback to InMemorySaver when requested or on connection failure
- Safe closure of the connection pool on application shutdown
"""
from unittest.mock import patch, MagicMock
import pytest
from langgraph.checkpoint.memory import InMemorySaver
from app.db.checkpointer import get_checkpointer, close_checkpointer
import app.db.checkpointer as checkpointer_module


@pytest.fixture(autouse=True)
def reset_checkpointer_state():
    """Ensure checkpointer singletons are reset before and after each test."""
    close_checkpointer()
    checkpointer_module._in_memory_checkpointer = None
    checkpointer_module._postgres_checkpointer = None
    checkpointer_module._postgres_pool = None
    yield
    close_checkpointer()
    checkpointer_module._in_memory_checkpointer = None
    checkpointer_module._postgres_checkpointer = None
    checkpointer_module._postgres_pool = None


def test_fallback_to_in_memory_when_forced(monkeypatch):
    """Verify that FORCE_MEMORY_SAVER=1 forces InMemorySaver fallback."""
    monkeypatch.setenv("FORCE_MEMORY_SAVER", "1")
    saver = get_checkpointer()
    assert isinstance(saver, InMemorySaver)


def test_fallback_to_in_memory_when_no_db_url(monkeypatch):
    """Verify InMemorySaver is returned when DATABASE_URL is empty."""
    monkeypatch.setattr(checkpointer_module.settings, "DATABASE_URL", "")
    monkeypatch.setenv("DATABASE_URL", "")
    saver = get_checkpointer()
    assert isinstance(saver, InMemorySaver)


def test_fallback_to_in_memory_on_connection_error(monkeypatch):
    """Verify InMemorySaver is returned if Postgres connection pool throws an exception."""
    monkeypatch.setattr(checkpointer_module.settings, "DATABASE_URL", "postgresql://invalid:5432/bad")
    with patch("psycopg_pool.ConnectionPool", side_effect=Exception("Connection refused")):
        saver = get_checkpointer()
        assert isinstance(saver, InMemorySaver)


def test_close_checkpointer_cleans_pool():
    """Verify close_checkpointer closes the active pool without errors."""
    mock_pool = MagicMock()
    checkpointer_module._postgres_pool = mock_pool
    checkpointer_module._postgres_checkpointer = MagicMock()

    close_checkpointer()

    mock_pool.close.assert_called_once()
    assert checkpointer_module._postgres_pool is None
    assert checkpointer_module._postgres_checkpointer is None

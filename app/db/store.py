"""
LangGraph Store Provider for cross-thread persistent student profile & adaptive memory.
Supports PostgreSQL (PostgresStore) for production with seamless fallback to InMemoryStore.
"""
import os
import logging
from typing import Optional, Any, Dict
from langgraph.store.memory import InMemoryStore
from app.core.config import settings

logger = logging.getLogger(__name__)

_in_memory_store: Optional[InMemoryStore] = None
_postgres_store: Optional[Any] = None
_postgres_store_pool: Optional[Any] = None


def get_store() -> Any:
    """Get LangGraph Store for cross-thread long-term memory.

    Returns PostgresStore backed by connection pool in production,
    or falls back to InMemoryStore for local development/testing.
    """
    global _in_memory_store, _postgres_store, _postgres_store_pool

    # Fast return if already initialized
    if _postgres_store is not None:
        return _postgres_store

    db_url = settings.DATABASE_URL or os.getenv("DATABASE_URL", "")
    force_memory = os.getenv("FORCE_MEMORY_STORE", "").strip().lower() in ("1", "true", "yes")

    if db_url and not force_memory:
        try:
            from psycopg_pool import ConnectionPool
            from psycopg.rows import dict_row
            from langgraph.store.postgres import PostgresStore

            logger.info("Initializing LangGraph PostgresStore connection pool...")
            _postgres_store_pool = ConnectionPool(
                conninfo=db_url,
                min_size=1,
                max_size=10,
                kwargs={"autocommit": True, "prepare_threshold": 0, "row_factory": dict_row},
            )
            _postgres_store = PostgresStore(_postgres_store_pool)
            _postgres_store.setup()
            logger.info("Successfully initialized LangGraph PostgresStore.")
            return _postgres_store
        except Exception as e:
            logger.warning(
                f"Could not initialize PostgresStore ({str(e)}). Falling back to InMemoryStore."
            )
            if _postgres_store_pool is not None:
                try:
                    _postgres_store_pool.close()
                except Exception:
                    pass
                _postgres_store_pool = None
            _postgres_store = None

    if _in_memory_store is None:
        _in_memory_store = InMemoryStore()
        logger.info("Initialized LangGraph InMemoryStore.")

    return _in_memory_store


def close_store() -> None:
    """Safely drain and close the PostgresStore connection pool on application shutdown."""
    global _postgres_store_pool, _postgres_store
    if _postgres_store_pool is not None:
        try:
            logger.info("Closing LangGraph PostgresStore connection pool...")
            _postgres_store_pool.close()
            logger.info("LangGraph PostgresStore connection pool closed.")
        except Exception as e:
            logger.warning(f"Error while closing PostgresStore connection pool: {str(e)}")
        finally:
            _postgres_store_pool = None
            _postgres_store = None


def get_student_profile(student_id: str) -> Dict[str, Any]:
    """Retrieve long-term student learning profile across all threads."""
    if not student_id:
        return {}
    try:
        store = get_store()
        namespace = ("students", student_id)
        item = store.get(namespace, "profile")
        if item and hasattr(item, "value") and isinstance(item.value, dict):
            return item.value
        return {}
    except Exception as e:
        logger.warning(f"Failed to retrieve student profile for '{student_id}': {str(e)}")
        return {}


def update_student_profile(student_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update or merge long-term student learning profile across all threads."""
    if not student_id:
        return {}
    try:
        store = get_store()
        namespace = ("students", student_id)
        current = get_student_profile(student_id)
        merged = {**current, **updates}
        store.put(namespace, "profile", merged)
        return merged
    except Exception as e:
        logger.warning(f"Failed to update student profile for '{student_id}': {str(e)}")
        return {}

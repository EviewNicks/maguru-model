"""LangGraph Checkpointer Provider for multi-turn state persistence."""
import os
import logging
from typing import Optional, Any
from langgraph.checkpoint.memory import InMemorySaver
from app.core.config import settings

logger = logging.getLogger(__name__)

_in_memory_checkpointer: Optional[InMemorySaver] = None
_postgres_checkpointer: Optional[Any] = None
_postgres_pool: Optional[Any] = None


def get_checkpointer() -> Any:
    """Get checkpointer for LangGraph state persistence.

    Returns PostgresSaver backed by a psycopg connection pool for production,
    or falls back to InMemorySaver for local development/testing.
    """
    global _in_memory_checkpointer, _postgres_checkpointer, _postgres_pool

    # Fast return if postgres checkpointer is already initialized
    if _postgres_checkpointer is not None:
        return _postgres_checkpointer

    # Check if PostgresSaver should and can be initialized
    db_url = settings.DATABASE_URL or os.getenv("DATABASE_URL", "")
    force_memory = os.getenv("FORCE_MEMORY_SAVER", "").strip().lower() in ("1", "true", "yes")

    if db_url and not force_memory:
        try:
            from psycopg_pool import ConnectionPool
            from psycopg.rows import dict_row
            from langgraph.checkpoint.postgres import PostgresSaver

            logger.info("Initializing LangGraph PostgresSaver connection pool...")
            # prepare_threshold=0 is required for Supabase transaction/session poolers
            _postgres_pool = ConnectionPool(
                conninfo=db_url,
                min_size=1,
                max_size=10,
                kwargs={"autocommit": True, "prepare_threshold": 0, "row_factory": dict_row},
            )
            _postgres_checkpointer = PostgresSaver(_postgres_pool)
            _postgres_checkpointer.setup()
            logger.info("Successfully initialized LangGraph PostgresSaver checkpointer.")
            return _postgres_checkpointer
        except Exception as e:
            logger.warning(
                f"Could not initialize PostgresSaver ({str(e)}). Falling back to InMemorySaver."
            )
            if _postgres_pool is not None:
                try:
                    _postgres_pool.close()
                except Exception:
                    pass
                _postgres_pool = None
            _postgres_checkpointer = None

    if _in_memory_checkpointer is None:
        _in_memory_checkpointer = InMemorySaver()
        logger.info("Initialized LangGraph InMemorySaver checkpointer.")

    return _in_memory_checkpointer


def close_checkpointer() -> None:
    """Safely drain and close the Postgres connection pool on application shutdown."""
    global _postgres_pool, _postgres_checkpointer
    if _postgres_pool is not None:
        try:
            logger.info("Closing LangGraph PostgresSaver connection pool...")
            _postgres_pool.close()
            logger.info("LangGraph PostgresSaver connection pool closed.")
        except Exception as e:
            logger.warning(f"Error while closing PostgresSaver connection pool: {str(e)}")
        finally:
            _postgres_pool = None
            _postgres_checkpointer = None

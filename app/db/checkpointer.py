"""LangGraph Checkpointer Provider for multi-turn state persistence."""
import os
import logging
from typing import Optional, Any
from langgraph.checkpoint.memory import InMemorySaver
from app.core.config import settings

logger = logging.getLogger(__name__)

_in_memory_checkpointer: Optional[InMemorySaver] = None

def get_checkpointer() -> Any:
    """Get checkpointer for LangGraph state persistence.
    
    Returns InMemorySaver for local development/testing or fallback,
    and supports connection to PostgreSQL checkpointer in production.
    """
    global _in_memory_checkpointer
    
    # Check if PostgresSaver can be initialized
    db_url = settings.DATABASE_URL or os.getenv("DATABASE_URL", "")
    if db_url and not os.getenv("FORCE_MEMORY_SAVER", ""):
        try:
            # Attempt to use PostgresSaver if available
            from langgraph.checkpoint.postgres import PostgresSaver
            # Use connection string
            saver = PostgresSaver.from_conn_string(db_url)
            saver.setup()
            logger.info("Successfully initialized LangGraph PostgresSaver checkpointer.")
            return saver
        except Exception as e:
            logger.warning(
                f"Could not initialize PostgresSaver ({str(e)}). Falling back to InMemorySaver."
            )

    if _in_memory_checkpointer is None:
        _in_memory_checkpointer = InMemorySaver()
        logger.info("Initialized LangGraph InMemorySaver checkpointer.")
        
    return _in_memory_checkpointer

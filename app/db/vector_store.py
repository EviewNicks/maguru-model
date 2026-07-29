import os
import logging
from typing import Optional
from langchain_community.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings

logger = logging.getLogger(__name__)

def get_embeddings() -> OpenAIEmbeddings:
    """Get embedding model instance configured via OpenRouter/OpenAI."""
    api_key = settings.OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY", "")
    return OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        openai_api_key=api_key,
        openai_api_base=settings.OPENROUTER_BASE_URL
    )

def get_vectorstore(collection_name: str = "maguru_course_knowledge") -> Optional[PGVector]:
    """Get or initialize PGVector store instance connecting to Supabase PostgreSQL."""
    db_url = settings.DATABASE_URL or os.getenv("DATABASE_URL", "")
    if not db_url:
        logger.warning("DATABASE_URL is not set. PGVector store will be unavailable.")
        return None

    try:
        return PGVector(
            connection_string=db_url,
            embedding_function=get_embeddings(),
            collection_name=collection_name
        )
    except Exception as e:
        logger.error(f"Failed to connect to PGVector database: {str(e)}", exc_info=True)
        return None

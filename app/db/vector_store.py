"""Modern Vector Store Provider with langchain-postgres and fallback."""
import os
import logging
from typing import Optional, Any
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings

logger = logging.getLogger(__name__)

def get_embeddings() -> OpenAIEmbeddings:
    """Get embedding model instance configured via OpenRouter/OpenAI."""
    api_key = settings.OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY", "")
    return OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        openai_api_key=api_key or "sk-placeholder",
        openai_api_base=settings.OPENROUTER_BASE_URL
    )

def get_vectorstore(collection_name: str = "maguru_course_knowledge") -> Optional[Any]:
    """Get or initialize PGVector store instance connecting to Supabase PostgreSQL.
    
    Prefers modern `langchain_postgres.PGVector` with fallback to `langchain_community.vectorstores.PGVector`.
    """
    db_url = settings.DATABASE_URL or os.getenv("DATABASE_URL", "")
    if not db_url:
        logger.warning("DATABASE_URL is not set. PGVector store will be unavailable.")
        return None

    # Try modern langchain_postgres first
    try:
        from langchain_postgres import PGVector
        return PGVector(
            connection=db_url,
            embeddings=get_embeddings(),
            collection_name=collection_name
        )
    except ImportError:
        pass
    except Exception as e:
        logger.warning(f"Failed to initialize langchain_postgres ({str(e)}). Trying community PGVector.")

    # Fallback to community PGVector
    try:
        from langchain_community.vectorstores import PGVector as CommunityPGVector
        return CommunityPGVector(
            connection_string=db_url,
            embedding_function=get_embeddings(),
            collection_name=collection_name
        )
    except Exception as e:
        logger.error(f"Failed to connect to PGVector database: {str(e)}", exc_info=True)
        return None

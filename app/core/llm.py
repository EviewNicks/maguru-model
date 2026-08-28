"""LLM Provider with Multi-Model Fallback & Pool Failover."""
import os
import logging
from typing import List, Any
from langchain_openai import ChatOpenAI
from .config import settings

logger = logging.getLogger(__name__)

_llm_instance = None
_llm_pool_instances: List[ChatOpenAI] = []

def get_llm_pool() -> List[ChatOpenAI]:
    """Get list of instantiated ChatOpenAI models from configured pool."""
    global _llm_pool_instances
    if not _llm_pool_instances:
        _llm_pool_instances = _create_llm_pool()
    return _llm_pool_instances

def get_llm() -> Any:
    """Get shared LLM instance with automatic multi-model fallback."""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = _create_llm_with_pool_fallbacks()
    return _llm_instance

def _create_llm_pool() -> List[ChatOpenAI]:
    """Create ChatOpenAI instances for each model in settings.model_pool."""
    openrouter_key = settings.OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY", "")
    models = settings.model_pool
    pool = []

    for model_name in models:
        try:
            instance = ChatOpenAI(
                model=model_name,
                api_key=openrouter_key or "sk-placeholder",
                base_url=settings.OPENROUTER_BASE_URL,
                temperature=settings.OPENROUTER_TEMPERATURE,
                max_completion_tokens=settings.OPENROUTER_MAX_TOKENS
            )
            pool.append(instance)
            logger.info(f"Initialized model pool candidate: {model_name}")
        except Exception as e:
            logger.warning(f"Could not initialize model {model_name}: {str(e)}")

    # Fallback to standard if pool is somehow empty
    if not pool:
        pool.append(ChatOpenAI(
            model="openai/gpt-oss-20b:free",
            api_key=openrouter_key or "sk-placeholder",
            base_url=settings.OPENROUTER_BASE_URL,
            temperature=0.7,
            max_completion_tokens=1500
        ))

    return pool

def _create_llm_with_pool_fallbacks() -> Any:
    """Create primary LLM with automatic failover to fallback models."""
    pool = get_llm_pool()
    primary = pool[0]

    if len(pool) > 1:
        fallbacks = pool[1:]
        # Use LangChain native with_fallbacks for seamless 429/404/500 failover
        chained_llm = primary.with_fallbacks(fallbacks)
        logger.info(f"LLM initialized with primary '{primary.model_name}' and {len(fallbacks)} fallback models.")
        return chained_llm

    return primary

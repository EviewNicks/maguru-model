"""LLM Provider with Multi-Model Fallback & Pool Failover and Timeout Protection."""
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
    """Get shared LLM instance with automatic multi-model fallback and timeout protection."""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = _create_llm_with_pool_fallbacks()
    return _llm_instance

def _create_llm_pool() -> List[ChatOpenAI]:
    """Create ChatOpenAI instances with 12s timeout for each model in settings.model_pool."""
    openrouter_key = settings.OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY", "")
    models = settings.model_pool
    pool = []

    for idx, model_name in enumerate(models, start=1):
        try:
            instance = ChatOpenAI(
                model=model_name,
                api_key=openrouter_key or "sk-placeholder",
                base_url=settings.OPENROUTER_BASE_URL,
                temperature=settings.OPENROUTER_TEMPERATURE,
                max_completion_tokens=settings.OPENROUTER_MAX_TOKENS,
                request_timeout=12,
                max_retries=1
            )
            pool.append(instance)
            logger.info(f"[LLM_POOL] Initialized Candidate #{idx}: '{model_name}' (timeout=12s)")
        except Exception as e:
            logger.warning(f"[LLM_POOL] Could not initialize model '{model_name}': {str(e)}")

    if not pool:
        default_model = "cohere/north-mini-code:free"
        logger.warning(f"[LLM_POOL] Pool was empty, falling back to default: '{default_model}'")
        pool.append(ChatOpenAI(
            model=default_model,
            api_key=openrouter_key or "sk-placeholder",
            base_url=settings.OPENROUTER_BASE_URL,
            temperature=0.7,
            max_completion_tokens=1500,
            request_timeout=12,
            max_retries=1
        ))

    return pool

def _create_llm_with_pool_fallbacks() -> Any:
    """Create primary LLM with automatic failover to fallback models."""
    pool = get_llm_pool()
    primary = pool[0]

    if len(pool) > 1:
        fallbacks = pool[1:]
        chained_llm = primary.with_fallbacks(fallbacks)
        logger.info(f"[LLM_INIT] Primary LLM: '{primary.model_name}' with {len(fallbacks)} fallback models: {[m.model_name for m in fallbacks]}")
        return chained_llm

    logger.info(f"[LLM_INIT] Single Primary LLM initialized: '{primary.model_name}'")
    return primary
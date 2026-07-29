import os
import logging
from langchain_openai import ChatOpenAI
from .config import settings

logger = logging.getLogger(__name__)

_llm = None

def get_llm() -> ChatOpenAI:
    """Get or create shared LLM instance with fallback support."""
    global _llm
    if _llm is None:
        _llm = _create_llm_with_fallback()
    return _llm

def _create_llm_with_fallback() -> ChatOpenAI:
    """Create ChatOpenAI instance using OpenRouter with Z.AI fallback."""
    openrouter_key = settings.OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY", "")
    openrouter_model = settings.OPENROUTER_MODEL or os.getenv("OPENROUTER_MODEL", "google/gemma-7b-it:free")

    if openrouter_key and openrouter_key != "your_key_here":
        try:
            return ChatOpenAI(
                model=openrouter_model,
                api_key=openrouter_key,
                base_url=settings.OPENROUTER_BASE_URL,
                temperature=0.7,
                max_completion_tokens=1500
            )
        except Exception as e:
            logger.warning(f"OpenRouter LLM initialization warning: {str(e)}")

    # Fallback to Z.AI if specified in environment
    zai_key = os.getenv("ZAI_API_KEY", "")
    zai_model = os.getenv("ZAI_MODEL", "glm-4.7")

    if zai_key and zai_key != "your_key_here":
        return ChatOpenAI(
            model=zai_model,
            api_key=zai_key,
            base_url="https://api.z.ai/api/paas/v4/",
            temperature=0.7,
            max_completion_tokens=1500
        )

    # Return standard ChatOpenAI instance
    return ChatOpenAI(
        model=openrouter_model,
        api_key=openrouter_key or "sk-placeholder",
        base_url=settings.OPENROUTER_BASE_URL,
        temperature=0.7,
        max_completion_tokens=1500
    )

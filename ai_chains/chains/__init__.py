"""AI Chains for Maguru Learning Platform."""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Shared LLM instance with fallback support
_llm = None


def get_llm():
    """Get or create shared LLM instance with fallback.

    Priority:
    1. OpenRouter API (primary)
    2. Z.AI API (fallback if OpenRouter fails)

    Returns:
        ChatOpenAI instance
    """
    global _llm
    if _llm is None:
        _llm = _create_llm_with_fallback()
    return _llm


def _create_llm_with_fallback():
    """Create LLM with fallback to Z.AI if OpenRouter fails."""
    # Try OpenRouter first (primary)
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    openrouter_model = os.getenv("OPENROUTER_MODEL", "google/gemma-7b-it")

    if openrouter_key and openrouter_key != "your_key_here":
        try:
            llm = ChatOpenAI(model=openrouter_model,
                api_key=openrouter_key,
                base_url="https://openrouter.ai/api/v1",
                temperature=0.7,
                max_completion_tokens=1500
            )
            # Test connection
            llm.invoke("Hello")
            return llm
        except Exception:
            print("OpenRouter connection failed, trying Z.AI fallback...")

    # Fallback to Z.AI
    zai_key = os.getenv("ZAI_API_KEY")
    zai_model = os.getenv("ZAI_MODEL", "glm-4.7")

    if zai_key and zai_key != "your_key_here":
        return ChatOpenAI(model=zai_model,
            api_key=zai_key,
            base_url="https://api.z.ai/api/paas/v4/",
            temperature=0.7,
            max_completion_tokens=1500
        )

    # If no API keys available, return OpenRouter with default (will fail on invoke)
    return ChatOpenAI(model=openrouter_model,
        api_key=openrouter_key or "sk-placeholder",
        base_url="https://openrouter.ai/api/v1",
        temperature=0.7,
        max_completion_tokens=1500
    )

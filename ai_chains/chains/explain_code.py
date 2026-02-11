"""Code explanation chain using LCEL."""

from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from . import get_llm

# Lazy chain initialization
_chain = None

def _get_chain():
    """Get or create chain (lazy initialization)."""
    global _chain
    if _chain is None:
        _prompt = load_prompt("ai_chains/prompts/explain_code.yaml")
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain

def explain_code(code_snippet: str) -> str:
    """Explain Python code in Indonesian.

    Args:
        code_snippet: Python code to explain

    Returns:
        Explanation in Indonesian
    """
    try:
        return _get_chain().invoke({"code": code_snippet})
    except Exception as e:
        return f"Maaf, tutor AI sedang tidak tersedia. Error: {str(e)}"

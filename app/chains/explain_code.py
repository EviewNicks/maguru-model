"""Code explanation chain."""
import logging
from pathlib import Path
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from app.core.llm import get_llm

logger = logging.getLogger(__name__)

_chain = None

def _get_chain():
    """Get or create chain (lazy initialization)."""
    global _chain
    if _chain is None:
        prompt_path = Path(__file__).parent.parent / "prompts" / "explain_code.yaml"
        _prompt = load_prompt(str(prompt_path))
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain

def explain_code(code_snippet: str) -> str:
    """Explain Python code snippet in Indonesian."""
    try:
        return _get_chain().invoke({"code": code_snippet})
    except Exception as e:
        logger.error(f"Error in explain_code: {str(e)}", exc_info=True)
        return f"Maaf, saya tidak bisa menjelaskan kode ini sekarang. Error: {str(e)}"

def create_explain_code_chain():
    """Create LangServe-compatible chain."""
    def invoke(input_dict: dict) -> str:
        code = input_dict.get("code") or input_dict.get("code_snippet") or ""
        return explain_code(code_snippet=code)
    return RunnableLambda(invoke)

"""Code explanation chain."""
import logging
from typing import Any
from pathlib import Path
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from app.core.llm import get_llm
from app.schemas.chat import ExplainCodeInputSchema

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
    if not code_snippet or not code_snippet.strip():
        return "Silakan masukkan potongan kode pemrograman yang ingin Anda minta penjelasannya."
    try:
        return _get_chain().invoke({"code": code_snippet})
    except Exception as e:
        logger.error(f"Error in explain_code: {str(e)}", exc_info=True)
        return f"Maaf, saya tidak bisa menjelaskan kode ini sekarang. Error: {str(e)}"

def create_explain_code_chain():
    """Create LangServe-compatible chain with explicit input schema."""
    def invoke(input_data: Any) -> str:
        if isinstance(input_data, dict):
            code = input_data.get("code") or input_data.get("code_snippet") or ""
        else:
            code = getattr(input_data, "code", "")
        return explain_code(code_snippet=code)
    return RunnableLambda(invoke).with_types(input_type=ExplainCodeInputSchema)

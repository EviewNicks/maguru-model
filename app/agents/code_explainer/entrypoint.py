"""
Code Explainer Agent — Stateless LCEL chain.

Explains Python code snippets in Indonesian for students.
Migrated from: app/chains/explain_code.py
"""
import logging
from pathlib import Path
from typing import Any

from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from app.shared import get_llm
from app.schemas.chat import ExplainCodeInputSchema

logger = logging.getLogger(__name__)

_PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "explain_code.yaml"
_chain = None


def _get_chain():
    """Lazy-initialize the LCEL chain."""
    global _chain
    if _chain is None:
        _prompt = load_prompt(str(_PROMPT_PATH))
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain


def explain_code(code_snippet: str) -> str:
    """Explain a Python code snippet in Indonesian."""
    if not code_snippet or not code_snippet.strip():
        return "Silakan masukkan potongan kode pemrograman yang ingin Anda minta penjelasannya."
    try:
        return _get_chain().invoke({"code": code_snippet})
    except Exception as e:
        logger.error(f"[CodeExplainer][ERROR] {str(e)}", exc_info=True)
        return f"Maaf, saya tidak bisa menjelaskan kode ini sekarang. Error: {str(e)}"


def create_code_explainer_chain():
    """
    LangServe-compatible entrypoint for /explain-code route.
    Supports SSE streaming via LangServe add_routes.
    """
    def invoke(input_data: Any) -> str:
        if isinstance(input_data, dict):
            code = input_data.get("code") or input_data.get("code_snippet") or ""
        else:
            code = getattr(input_data, "code", "")
        return explain_code(code_snippet=code)

    return RunnableLambda(invoke).with_types(input_type=ExplainCodeInputSchema)

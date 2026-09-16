"""Hint generator chain."""
import logging
from typing import Any
from pathlib import Path
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from app.core.llm import get_llm
from app.schemas.chat import HintInputSchema

logger = logging.getLogger(__name__)

_chain = None

def _get_chain():
    """Get or create chain (lazy initialization)."""
    global _chain
    if _chain is None:
        prompt_path = Path(__file__).parent.parent / "prompts" / "hint_generator.yaml"
        _prompt = load_prompt(str(prompt_path))
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain

def generate_hint(task: str, student_attempt: str, level: int = 1) -> str:
    """Generate progressive hint in Indonesian."""
    level = max(1, min(3, level))
    try:
        return _get_chain().invoke({
            "task": task or "Selesaikan tugas logika pemrograman ini",
            "attempt": student_attempt or "Belum ada percobaan",
            "level": str(level)
        })
    except Exception as e:
        logger.error(f"Error in generate_hint: {str(e)}", exc_info=True)
        return f"Hint tidak tersedia sekarang. Error: {str(e)}"

def create_hint_generator_chain():
    """Create LangServe-compatible chain with explicit input schema."""
    def invoke(input_data: Any) -> str:
        if isinstance(input_data, dict):
            task = input_data.get("task", "")
            attempt = input_data.get("attempt") or input_data.get("student_attempt", "")
            level = input_data.get("level", 1)
        else:
            task = getattr(input_data, "task", "")
            attempt = getattr(input_data, "student_attempt", "")
            level = getattr(input_data, "level", 1)

        try:
            level = int(level)
        except (ValueError, TypeError):
            level = 1

        return generate_hint(
            task=task,
            student_attempt=attempt,
            level=level
        )
    return RunnableLambda(invoke).with_types(input_type=HintInputSchema)

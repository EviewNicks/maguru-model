"""Hint generator chain."""
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
        prompt_path = Path(__file__).parent.parent / "prompts" / "hint_generator.yaml"
        _prompt = load_prompt(str(prompt_path))
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain

def generate_hint(task: str, student_attempt: str, level: int = 1) -> str:
    """Generate progressive hint in Indonesian."""
    level = max(1, min(3, level))
    try:
        return _get_chain().invoke({
            "task": task,
            "attempt": student_attempt,
            "level": str(level)
        })
    except Exception as e:
        logger.error(f"Error in generate_hint: {str(e)}", exc_info=True)
        return f"Hint tidak tersedia sekarang. Error: {str(e)}"

def create_hint_generator_chain():
    """Create LangServe-compatible chain."""
    def invoke(input_dict: dict) -> str:
        level = input_dict.get("level", 1)
        try:
            level = int(level)
        except (ValueError, TypeError):
            level = 1
        return generate_hint(
            task=input_dict.get("task", ""),
            student_attempt=input_dict.get("attempt") or input_dict.get("student_attempt", ""),
            level=level
        )
    return RunnableLambda(invoke)

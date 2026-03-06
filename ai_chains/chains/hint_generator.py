"""Progressive hint generator chain."""

from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from . import get_llm

# Lazy chain initialization
_chain = None

def _get_chain():
    """Get or create chain (lazy initialization)."""
    global _chain
    if _chain is None:
        _prompt = load_prompt("ai_chains/prompts/hint_generator.yaml")
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain

def generate_hint(task: str, student_attempt: str, level: int) -> str:
    """Generate progressive hint.

    Args:
        task: Practice task description
        student_attempt: Student's current attempt
        level: Hint level (1=gentle, 2=conceptual, 3=direct)

    Returns:
        Hint in Indonesian
    """
    level_names = {1: "Halus", 2: "Konseptual", 3: "Langsung"}
    level_name = level_names.get(level, "Halus")

    try:
        return _get_chain().invoke({
            "task": task,
            "attempt": student_attempt,
            "level": level_name
        })
    except Exception as e:
        return f"Hint tidak tersedia. Error: {str(e)}"

def get_all_hints(task: str, student_attempt: str) -> list:
    """Generate all 3 hint levels.

    Returns list of hints for levels 1, 2, 3.
    """
    return [
        generate_hint(task, student_attempt, 1),
        generate_hint(task, student_attempt, 2),
        generate_hint(task, student_attempt, 3)
    ]

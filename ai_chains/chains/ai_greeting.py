"""AI greeting generation chain."""

from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from . import get_llm

# Lazy chain initialization
_chain = None

def _get_chain():
    """Get or create chain (lazy initialization)."""
    global _chain
    if _chain is None:
        _prompt = load_prompt("ai_chains/prompts/ai_greeting.yaml")
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain

def generate_greeting(student_name: str, course_metadata: dict) -> str:
    """Generate personalized course greeting.

    Args:
        student_name: Student's name
        course_metadata: Dict with title and learning_objectives

    Returns:
        Greeting in Indonesian
    """
    objectives = "\n".join([
        f"- {obj}" for obj in course_metadata.get("learning_objectives", [])
    ])

    try:
        return _get_chain().invoke({
            "student_name": student_name,
            "course_title": course_metadata.get("title", "Kursus Python"),
            "learning_objectives": objectives
        })
    except Exception as e:
        return f"Halo, {student_name}! Selamat datang di kursus Python. Mari kita mulai belajar!"

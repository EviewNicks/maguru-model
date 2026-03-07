"""AI greeting generation chain with personalized responses."""

from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from . import get_llm
import random

# Lazy chain initialization
_chain = None

def _get_chain():
    """Get or create chain (lazy initialization)."""
    global _chain
    if _chain is None:
        _prompt = load_prompt("ai_chains/prompts/ai_greeting.yaml")
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain

def _get_fallback_greeting(student_name: str, course_title: str) -> str:
    """Generate encouraging fallback greeting without LLM."""
    greetings = [
        f"Halo {student_name}! Selamat datang di {course_title}.",
        f"Hi {student_name}! Senang bertemu kamu di kelas {course_title}.",
        f"Selamat datang {student_name}! Siap belajar {course_title}?",
    ]
    encouragements = [
        "Mari kita mulai petualangan ini dengan semangat!",
        "Ayok kita mulai, pasti seru!",
        "Kita belajar bersama ya, {student_name}!",
    ]
    return f"{random.choice(greetings)} {random.choice(encouragements)}"

def generate_greeting(student_name: str, course_metadata: dict) -> str:
    """Generate personalized course greeting with variety.

    Args:
        student_name: Student's name
        course_metadata: Dict with title and learning_objectives

    Returns:
        Personalized greeting in Indonesian
    """
    # Format learning objectives for prompt
    objectives = course_metadata.get("learning_objectives", [])
    if objectives:
        obj_text = "\n".join([f"- {obj}" for obj in objectives[:3]])
    else:
        obj_text = "berbagai dasar pemrograman"

    course_title = course_metadata.get("title", "Kursus Python")

    try:
        result = _get_chain().invoke({
            "student_name": student_name,
            "course_title": course_title,
            "learning_objectives": obj_text
        })
        # Post-process to ensure quality
        if len(result) < 30 or result.startswith("Halo"):
            # Fallback if LLM response is too generic
            return _get_fallback_greeting(student_name, course_title)
        return result
    except Exception:
        return _get_fallback_greeting(student_name, course_title)

"""Student greeting chain."""
import logging
from pathlib import Path
from typing import Dict, Any, Union
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
        prompt_path = Path(__file__).parent.parent / "prompts" / "ai_greeting.yaml"
        _prompt = load_prompt(str(prompt_path))
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain

def generate_greeting(student_name: str, course_metadata: Union[dict, str]) -> str:
    """Generate personal course greeting for student."""
    if isinstance(course_metadata, str):
        title = course_metadata
        objectives = "Dasar-dasar pemrograman"
    else:
        title = course_metadata.get("title", "Pemrograman Python")
        objectives = course_metadata.get("learning_objectives", "Dasar-dasar pemrograman")

    try:
        return _get_chain().invoke({
            "student_name": student_name,
            "course_title": title,
            "learning_objectives": objectives
        })
    except Exception as e:
        logger.error(f"Error in generate_greeting: {str(e)}", exc_info=True)
        return f"Halo {student_name}! Selamat datang di kursus {title}!"

def create_greeting_chain():
    """Create LangServe-compatible chain."""
    def invoke(input_dict: dict) -> str:
        student_name = input_dict.get("student_name", "Siswa")
        course_meta = input_dict.get("course_metadata", {})
        return generate_greeting(student_name=student_name, course_metadata=course_meta)
    return RunnableLambda(invoke)

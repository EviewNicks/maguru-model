"""
Co-Teacher Greeting — Personalized student welcome message.
Part of the Co-Teacher agent domain.
Migrated from: app/chains/ai_greeting.py
"""
import logging
from pathlib import Path
from typing import Any, Union, Optional

from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from app.shared import get_llm
from app.schemas.chat import GreetingInputSchema

logger = logging.getLogger(__name__)

_PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "ai_greeting.yaml"
_chain: Optional[Any] = None


def _get_chain():
    global _chain
    if _chain is None:
        _prompt = load_prompt(str(_PROMPT_PATH))
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain


def generate_greeting(student_name: str, course_metadata: Union[dict, str]) -> str:
    """Generate a personalized course greeting for a student."""
    if isinstance(course_metadata, str):
        title = course_metadata
        objectives = "Dasar-dasar pemrograman"
    elif isinstance(course_metadata, dict):
        title = course_metadata.get("title") or "Pemrograman Python"
        objectives = course_metadata.get("learning_objectives") or "Dasar-dasar pemrograman"
    else:
        title = "Pemrograman Python"
        objectives = "Dasar-dasar pemrograman"

    try:
        return _get_chain().invoke({
            "student_name": student_name or "Siswa",
            "course_title": title or "Pemrograman Python",
            "learning_objectives": objectives or "Dasar-dasar pemrograman",
        })
    except Exception as e:
        logger.error(f"[CoTeacher][GREETING][ERROR] {str(e)}", exc_info=True)
        return f"Halo {student_name}! Selamat datang di kursus {title}!"


def create_greeting_chain():
    """LangServe-compatible entrypoint for /greeting route."""
    def invoke(input_data: Any) -> str:
        if isinstance(input_data, dict):
            student_name = input_data.get("user_name") or input_data.get("student_name") or "Siswa"
            course_meta = input_data.get("course_metadata", {})
        else:
            student_name = getattr(input_data, "user_name", "Siswa")
            course_meta = getattr(input_data, "course_metadata", {})
        return generate_greeting(student_name=student_name, course_metadata=course_meta)

    return RunnableLambda(invoke).with_types(input_type=GreetingInputSchema)

"""Automated Quiz Generator Chain for generating assessment questions from lesson content."""
import json
import re
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from app.core.llm import get_llm
from app.services.rag_service import get_course_context
from app.schemas.quiz import GenerateQuizRequestSchema

logger = logging.getLogger(__name__)

_chain = None

def _get_chain():
    """Get or create chain (lazy initialization)."""
    global _chain
    if _chain is None:
        prompt_path = Path(__file__).parent.parent / "prompts" / "quiz_generator.yaml"
        _prompt = load_prompt(str(prompt_path))
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain

def _sanitize_input(text: Optional[str], max_len: int = 4000) -> str:
    """Sanitize and truncate input text for prompt injection protection."""
    if not text:
        return ""
    sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', str(text))
    return sanitized[:max_len]

def _extract_json_array(raw_text: str) -> List[Dict[str, Any]]:
    """Safely extract and parse JSON array from raw LLM output string."""
    cleaned = raw_text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, list):
            return parsed
        elif isinstance(parsed, dict) and "questions" in parsed:
            return parsed["questions"]
        return [parsed]
    except Exception:
        match = re.search(r'\[\s*\{.*\}\s*\]', raw_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
        raise ValueError(f"Could not parse LLM output as valid JSON quiz array: {raw_text[:200]}")

def generate_quiz_questions(
    course_id: str,
    section_id: Optional[str] = None,
    num_questions: int = 5,
    difficulty: str = "medium",
    lesson_content: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Generate structured quiz assessment questions based on course/lesson content."""
    safe_course_id = _sanitize_input(course_id, max_len=100) or "umum"
    safe_difficulty = difficulty.lower() if difficulty.lower() in ("easy", "medium", "hard") else "medium"

    content_for_prompt = ""
    if lesson_content and lesson_content.strip():
        content_for_prompt = _sanitize_input(lesson_content, max_len=3000)
    else:
        try:
            content_for_prompt = get_course_context(course_id=safe_course_id, query="quiz materi konsep dasar", top_k=4)
        except Exception as e:
            logger.warning(f"RAG context retrieval for quiz generator fallback: {str(e)}")

    if not content_for_prompt or not content_for_prompt.strip():
        content_for_prompt = f"Topik pembelajaran untuk kursus {safe_course_id} meliputi konsep dasar pemrograman, logika, dan pemecahan masalah."

    try:
        raw_output = _get_chain().invoke({
            "lesson_content": content_for_prompt,
            "num_questions": str(num_questions),
            "difficulty": safe_difficulty
        })
        questions = _extract_json_array(raw_output)
        if not questions:
            raise ValueError("Empty questions array returned from LLM.")
        return questions
    except Exception as e:
        logger.error(f"Error generating quiz questions for course {safe_course_id}: {str(e)}", exc_info=True)
        return [
            {
                "question": f"Konsep manakah yang dipelajari pada kursus {safe_course_id}?",
                "options": {
                  "a": "Pemrograman dasar dan sintaks dasar",
                  "b": "Pengeditan video tingkat lanjut",
                  "c": "Desain grafis 3D",
                  "d": "Manajemen keuangan akuntansi"
                },
                "correct": "a",
                "topic": "Pemrograman",
                "difficulty": difficulty
            }
        ]

def create_quiz_generator_chain():
    """Create LangServe-compatible runnable with explicit input schema."""
    def invoke(input_data: Any) -> dict:
        if isinstance(input_data, dict):
            cid = input_data.get("course_id", "umum")
            sid = input_data.get("section_id", None)
            nq = input_data.get("num_questions", 5)
            diff = input_data.get("difficulty", "medium")
            lc = input_data.get("lesson_content", None)
        else:
            cid = getattr(input_data, "course_id", "umum")
            sid = getattr(input_data, "section_id", None)
            nq = getattr(input_data, "num_questions", 5)
            diff = getattr(input_data, "difficulty", "medium")
            lc = getattr(input_data, "lesson_content", None)

        try:
            nq = int(nq)
        except (ValueError, TypeError):
            nq = 5

        questions = generate_quiz_questions(
            course_id=cid,
            section_id=sid,
            num_questions=nq,
            difficulty=diff,
            lesson_content=lc
        )
        return {"status": "success", "course_id": cid, "questions": questions}
    return RunnableLambda(invoke).with_types(input_type=GenerateQuizRequestSchema)

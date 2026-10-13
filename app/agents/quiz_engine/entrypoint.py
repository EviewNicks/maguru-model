"""
Quiz Engine Agent — LangServe-compatible entrypoints.

Exposes:
  - create_quiz_engine_chain()   → /generate-quiz SSE route
  - create_quiz_feedback_chain() → /quiz-feedback SSE route
"""
import logging
from pathlib import Path
from typing import Any

from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from app.shared import get_llm
from app.schemas.chat import QuizFeedbackInputSchema
from app.schemas.quiz import GenerateQuizRequestSchema

logger = logging.getLogger(__name__)

_FEEDBACK_PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "quiz_feedback.yaml"

_feedback_chain = None


def _get_feedback_chain():
    """Lazy-initialize the quiz feedback LCEL chain."""
    global _feedback_chain
    if _feedback_chain is None:
        _prompt = load_prompt(str(_FEEDBACK_PROMPT_PATH))
        _feedback_chain = _prompt | get_llm() | StrOutputParser()
    return _feedback_chain


# ─── Quiz Feedback Chain ──────────────────────────────────────────────────────

def generate_feedback(
    question: str,
    student_answer: str,
    correct_answer: str,
    is_correct: bool,
) -> str:
    """Generate supportive quiz feedback in Indonesian."""
    status_str = "Benar" if is_correct else "Salah"
    try:
        return _get_feedback_chain().invoke({
            "question": question or "Soal kuis pemrograman",
            "student_answer": student_answer or "Tidak ada jawaban",
            "correct_answer": correct_answer or "Jawaban yang benar",
            "is_correct": status_str,
        })
    except Exception as e:
        logger.error(f"[QuizEngine][FEEDBACK][ERROR] {str(e)}", exc_info=True)
        return "Feedback tidak tersedia sekarang."


def create_quiz_feedback_chain():
    """LangServe-compatible chain for /quiz-feedback route."""
    def invoke(input_data: Any) -> str:
        if isinstance(input_data, dict):
            question = input_data.get("question", "")
            student_answer = input_data.get("student_answer", "")
            correct_answer = input_data.get("correct_answer", "")
            is_correct = input_data.get("is_correct", False)
        else:
            question = getattr(input_data, "question", "")
            student_answer = getattr(input_data, "student_answer", "")
            correct_answer = getattr(input_data, "correct_answer", "")
            is_correct = getattr(input_data, "is_correct", False)

        if isinstance(is_correct, str):
            is_correct = is_correct.lower() in ("true", "1", "yes", "benar")

        return generate_feedback(
            question=question,
            student_answer=student_answer,
            correct_answer=correct_answer,
            is_correct=bool(is_correct),
        )

    return RunnableLambda(invoke).with_types(input_type=QuizFeedbackInputSchema)


# ─── Quiz Generator Chain ─────────────────────────────────────────────────────

def create_quiz_engine_chain():
    """
    LangServe-compatible chain for /generate-quiz route.
    Delegates to the quiz graph for stateful generation.
    """
    from app.agents.quiz_engine.graph import generate_quiz_direct

    def invoke(input_data: Any) -> dict:
        if isinstance(input_data, dict):
            topic = input_data.get("topic", "")
            content = input_data.get("content", "")
            course_id = input_data.get("course_id", "")
            quiz_type = input_data.get("quiz_type", "section_quiz")
            num_questions = input_data.get("num_questions", 3)
            difficulty = input_data.get("difficulty", "medium")
            thread_id = input_data.get("thread_id", None)
        else:
            topic = getattr(input_data, "topic", "")
            content = getattr(input_data, "content", "")
            course_id = getattr(input_data, "course_id", "")
            quiz_type = getattr(input_data, "quiz_type", "section_quiz")
            num_questions = getattr(input_data, "num_questions", 3)
            difficulty = getattr(input_data, "difficulty", "medium")
            thread_id = getattr(input_data, "thread_id", None)

        return generate_quiz_direct(
            topic=topic,
            content=content,
            course_id=course_id,
            quiz_type=quiz_type,
            num_questions=num_questions,
            difficulty=difficulty,
            thread_id=thread_id,
        )

    return RunnableLambda(invoke).with_types(input_type=GenerateQuizRequestSchema)

"""Quiz feedback chain."""
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
        prompt_path = Path(__file__).parent.parent / "prompts" / "quiz_feedback.yaml"
        _prompt = load_prompt(str(prompt_path))
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain

def generate_feedback(question: str, student_answer: str, correct_answer: str, is_correct: bool) -> str:
    """Generate supportive feedback for quiz response."""
    status_str = "Benar" if is_correct else "Salah"
    try:
        return _get_chain().invoke({
            "question": question,
            "student_answer": student_answer,
            "correct_answer": correct_answer,
            "is_correct": status_str
        })
    except Exception as e:
        logger.error(f"Error in generate_feedback: {str(e)}", exc_info=True)
        return "Feedback tidak tersedia sekarang."

def create_quiz_feedback_chain():
    """Create LangServe-compatible chain."""
    def invoke(input_dict: dict) -> str:
        is_correct = input_dict.get("is_correct", False)
        if isinstance(is_correct, str):
            is_correct = is_correct.lower() in ("true", "1", "yes", "benar")
        return generate_feedback(
            question=input_dict.get("question", ""),
            student_answer=input_dict.get("student_answer", ""),
            correct_answer=input_dict.get("correct_answer", ""),
            is_correct=bool(is_correct)
        )
    return RunnableLambda(invoke)

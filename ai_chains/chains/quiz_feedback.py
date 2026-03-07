"""Quiz feedback generation chain."""

from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from . import get_llm

# Lazy chain initialization
_chain = None

def _get_chain():
    """Get or create chain (lazy initialization)."""
    global _chain
    if _chain is None:
        _prompt = load_prompt("ai_chains/prompts/quiz_feedback.yaml")
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain

def generate_feedback(question: str, student_answer: str,
                     correct_answer: str, is_correct: bool) -> str:
    """Generate quiz feedback.

    Args:
        question: Question text
        student_answer: Student's answer
        correct_answer: Correct answer
        is_correct: Whether answer was correct

    Returns:
        Feedback in Indonesian
    """
    status = "Benar" if is_correct else "Salah"

    try:
        return _get_chain().invoke({
            "question": question,
            "student_answer": str(student_answer),
            "correct_answer": str(correct_answer),
            "is_correct": status
        })
    except Exception:
        if is_correct:
            return "Benar! Bagus sekali!"
        return f"Salah. Jawaban yang benar adalah: {correct_answer}"

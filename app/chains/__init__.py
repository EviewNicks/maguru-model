"""
AI Chains Package — Backward-Compatibility Shims.

All symbols are now provided by app.agents.* modules.
These re-exports ensure existing tests and API endpoints continue to work.
"""
# Co-Teacher (stateful)
from app.agents.co_teacher.entrypoint import create_co_teacher_chain as create_qa_chatbot_chain, answer_question
from app.agents.co_teacher.greeting import create_greeting_chain, generate_greeting

# Code Explainer (stateless)
from app.agents.code_explainer.entrypoint import create_code_explainer_chain as create_explain_code_chain, explain_code

# Hint Generator (stateless)
from app.agents.hint_generator.entrypoint import create_hint_generator_chain, generate_hint

# Quiz Engine (stateful)
from app.agents.quiz_engine.entrypoint import create_quiz_feedback_chain, generate_feedback
from app.chains.quiz_generator import generate_quiz_questions, create_quiz_generator_chain

__all__ = [
    # Legacy names (used by existing tests)
    "answer_question", "create_qa_chatbot_chain",
    "explain_code", "create_explain_code_chain",
    "generate_hint", "create_hint_generator_chain",
    "generate_feedback", "create_quiz_feedback_chain",
    "generate_greeting", "create_greeting_chain",
    "generate_quiz_questions", "create_quiz_generator_chain",
]

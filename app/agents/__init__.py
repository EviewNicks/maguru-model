"""
Maguru AI Agents — Modular 4-Agent Architecture.

Each agent is a self-contained vertical slice:
  - co_teacher     : Stateful Q&A with multi-turn memory + RAG + Greeting (LangGraph)
  - code_explainer : Stateless code explanation (LCEL)
  - hint_generator : Stateless 3-level progressive hints (LCEL)
  - quiz_engine    : Stateful quiz generation + feedback (LangGraph)
"""
from app.agents.co_teacher import create_co_teacher_chain, create_greeting_chain
from app.agents.code_explainer import create_code_explainer_chain
from app.agents.hint_generator import create_hint_generator_chain
from app.agents.quiz_engine import create_quiz_feedback_chain, create_quiz_engine_chain

__all__ = [
    "create_co_teacher_chain",
    "create_greeting_chain",
    "create_code_explainer_chain",
    "create_hint_generator_chain",
    "create_quiz_feedback_chain",
    "create_quiz_engine_chain",
]

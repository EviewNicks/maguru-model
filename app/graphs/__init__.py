"""
LangGraph Stateful Workflows Package — Backward-Compatibility Shims.

Logic has been migrated to app.agents.co_teacher and app.agents.quiz_engine.
These re-exports keep existing import paths functional.
"""
from app.agents.co_teacher.graph import (
    QAState, create_qa_graph, get_qa_graph, run_qa_graph, astream_qa_graph,
)
from app.agents.quiz_engine.graph import (
    QuizState, create_quiz_graph, get_quiz_graph, generate_quiz_direct,
)

__all__ = [
    "QAState", "create_qa_graph", "get_qa_graph", "run_qa_graph", "astream_qa_graph",
    "QuizState", "create_quiz_graph", "get_quiz_graph", "generate_quiz_direct",
]

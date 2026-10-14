"""
Hint Generator Agent — LangGraph workflow for progressive programming hints.
Compatible with LangGraph CLI and LangGraph Studio.
"""
import logging
from typing import Dict, Any, Optional
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

from app.agents.hint_generator.entrypoint import generate_hint

logger = logging.getLogger(__name__)


class HintState(TypedDict):
    """State definition for Hint Generator workflow."""
    task: str
    attempt: str
    level: int
    hint: Optional[str]


def generate_hint_node(state: HintState) -> Dict[str, Any]:
    """Execute progressive hint generation node."""
    task = state.get("task", "")
    attempt = state.get("attempt", "")
    level = state.get("level", 1)
    hint = generate_hint(task=task, student_attempt=attempt, level=level)
    return {"hint": hint}


def create_hint_graph():
    """Create and compile Hint Generator LangGraph."""
    workflow = StateGraph(HintState)
    workflow.add_node("generate_hint", generate_hint_node)
    workflow.add_edge(START, "generate_hint")
    workflow.add_edge("generate_hint", END)
    return workflow.compile()


_hint_graph = None


def get_hint_graph():
    """Get singleton compiled Hint Generator graph."""
    global _hint_graph
    if _hint_graph is None:
        _hint_graph = create_hint_graph()
    return _hint_graph

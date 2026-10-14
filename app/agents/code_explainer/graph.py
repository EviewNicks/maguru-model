"""
Code Explainer Agent — LangGraph workflow for code explanation.
Compatible with LangGraph CLI and LangGraph Studio.
"""
import logging
from typing import Dict, Any, Optional
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

from app.agents.code_explainer.entrypoint import explain_code

logger = logging.getLogger(__name__)


class CodeExplainerState(TypedDict):
    """State definition for Code Explainer workflow."""
    code: str
    explanation: Optional[str]


def explain_code_node(state: CodeExplainerState) -> Dict[str, Any]:
    """Execute code explanation node."""
    code = state.get("code", "")
    explanation = explain_code(code)
    return {"explanation": explanation}


def create_explainer_graph():
    """Create and compile Code Explainer LangGraph."""
    workflow = StateGraph(CodeExplainerState)
    workflow.add_node("explain_code", explain_code_node)
    workflow.add_edge(START, "explain_code")
    workflow.add_edge("explain_code", END)
    return workflow.compile()


_explainer_graph = None


def get_explainer_graph():
    """Get singleton compiled Code Explainer graph."""
    global _explainer_graph
    if _explainer_graph is None:
        _explainer_graph = create_explainer_graph()
    return _explainer_graph

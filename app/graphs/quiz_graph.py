"""Stateful LangGraph Workflow for Automated Quiz Generation (Direct Flow)."""
import os
import uuid
import logging
from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from app.db.checkpointer import get_checkpointer
from app.chains.quiz_generator import generate_quiz_questions

logger = logging.getLogger(__name__)

class QuizState(TypedDict):
    """State definition for Quiz Generation workflow."""
    course_id: str
    topic: str
    content: str
    quiz_type: str
    num_questions: int
    difficulty: str
    questions: List[Dict[str, Any]]
    status: str

def generate_quiz_node(state: QuizState) -> Dict[str, Any]:
    """Generate quiz questions directly using LLM."""
    topic = state.get("topic", "")
    content = state.get("content", "")
    num_questions = state.get("num_questions", 3)
    difficulty = state.get("difficulty", "medium")

    questions = generate_quiz_questions(
        topic=topic,
        content=content,
        num_questions=num_questions,
        difficulty=difficulty
    )

    return {
        "questions": questions,
        "status": "generated"
    }

def create_quiz_graph():
    """Create and compile direct Quiz Generation LangGraph."""
    workflow = StateGraph(QuizState)
    workflow.add_node("generate_quiz", generate_quiz_node)

    workflow.add_edge(START, "generate_quiz")
    workflow.add_edge("generate_quiz", END)

    checkpointer = get_checkpointer()
    return workflow.compile(checkpointer=checkpointer)

_quiz_graph = None

def get_quiz_graph():
    """Get singleton compiled Quiz graph."""
    global _quiz_graph
    if _quiz_graph is None:
        _quiz_graph = create_quiz_graph()
    return _quiz_graph

def generate_quiz_direct(
    topic: str,
    content: str,
    course_id: str,
    quiz_type: str = "section_quiz",
    num_questions: int = 3,
    difficulty: str = "medium",
    thread_id: Optional[str] = None
) -> Dict[str, Any]:
    """Execute direct quiz generation graph with persistence."""
    graph = get_quiz_graph()
    thread_key = thread_id or f"quiz-{course_id}-{uuid.uuid4()}"
    config = {"configurable": {"thread_id": thread_key}}

    initial_state = {
        "course_id": course_id,
        "topic": topic,
        "content": content,
        "quiz_type": quiz_type,
        "num_questions": num_questions,
        "difficulty": difficulty,
        "questions": [],
        "status": "started"
    }

    result = graph.invoke(initial_state, config=config)
    return {
        "status": result.get("status", "success"),
        "course_id": course_id,
        "quiz_type": quiz_type,
        "thread_id": thread_key,
        "questions": result.get("questions", [])
    }

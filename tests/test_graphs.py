"""Unit tests for LangGraph Stateful Workflows (QA Graph & Quiz Graph)."""
import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage, AIMessage
from fastapi.testclient import TestClient

from app.main import app
from app.db.checkpointer import get_checkpointer
from app.graphs.qa_graph import create_qa_graph, run_qa_graph, retrieve_context_node, generate_answer_node
from app.graphs.quiz_graph import create_quiz_graph, generate_quiz_node, generate_quiz_direct

client = TestClient(app)

def test_checkpointer_singleton():
    """Verify checkpointer initialization and singleton behavior."""
    cp1 = get_checkpointer()
    cp2 = get_checkpointer()
    assert cp1 is not None
    assert cp1 == cp2

def test_qa_graph_creation():
    """Verify QA StateGraph compiles properly with expected nodes."""
    graph = create_qa_graph()
    assert graph is not None
    assert hasattr(graph, "invoke")
    assert hasattr(graph, "astream")

def test_qa_retrieve_context_node():
    """Test RAG context retrieval node in QA StateGraph."""
    state = {
        "messages": [HumanMessage(content="Apa itu variabel dalam Python?")],
        "course_id": "course-123",
        "session_title": "Variabel",
        "session_content": "Materi variabel",
        "rag_context": ""
    }
    with patch("app.graphs.qa_graph.get_course_context", return_value="Konteks variabel Python"):
        result = retrieve_context_node(state)
        assert "rag_context" in result
        assert result["rag_context"] == "Konteks variabel Python"

def test_qa_generate_answer_node():
    """Test answer generation node with mocked LLM."""
    state = {
        "messages": [HumanMessage(content="Halo")],
        "course_id": None,
        "session_title": "Dasar",
        "session_content": "Materi",
        "rag_context": "Konteks dasar"
    }
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = AIMessage(content="Halo! Ada yang bisa saya bantu?")
    
    with patch("app.graphs.qa_graph.get_llm", return_value=mock_llm):
        result = generate_answer_node(state)
        assert "messages" in result
        assert len(result["messages"]) == 1
        assert "Halo! Ada yang bisa saya bantu?" in result["messages"][0].content

def test_quiz_graph_creation():
    """Verify Quiz Generation StateGraph compiles with correct nodes."""
    graph = create_quiz_graph()
    assert graph is not None
    assert hasattr(graph, "invoke")

def test_quiz_generate_node():
    """Test generation node in direct Quiz graph."""
    state = {
        "course_id": "course-xyz",
        "topic": "Python Loop",
        "content": "for and while loops in python",
        "quiz_type": "section_quiz",
        "num_questions": 2,
        "difficulty": "easy",
        "questions": [],
        "status": "init"
    }

    mock_questions = [
        {
            "question": "Apa fungsi for loop?",
            "options": {"a": "Iterasi", "b": "Print", "c": "Delete", "d": "Exit"},
            "correct": "a",
            "topic": "Loop",
            "difficulty": "easy"
        }
    ]

    with patch("app.graphs.quiz_graph.generate_quiz_questions", return_value=mock_questions):
        res = generate_quiz_node(state)
        assert res["status"] == "generated"
        assert len(res["questions"]) == 1

def test_chat_streaming_sse_endpoint():
    """Test SSE token streaming endpoint /api/v1/chat/stream."""
    with patch("app.graphs.qa_graph.get_llm") as mock_get_llm:
        mock_llm = MagicMock()
        
        async def mock_astream(*args, **kwargs):
            for token in ["Halo", " ", "Siswa", "!"]:
                yield AIMessage(content=token)
                
        mock_llm.astream = mock_astream
        mock_get_llm.return_value = mock_llm

        response = client.post(
            "/api/v1/chat/stream",
            json={
                "question": "Halo AI",
                "session_title": "Pengenalan",
                "thread_id": "test-stream-thread-1"
            }
        )
        assert response.status_code == 200
        assert "text/event-stream" in response.headers.get("content-type", "")
        content = response.text
        assert "event: thread_id" in content
        assert "test-stream-thread-1" in content
        assert "event: data" in content

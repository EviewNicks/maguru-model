"""
MoSCoW Unit and Integration Tests for Maguru AI Modular 4-Agent Architecture.

Scope:
- Must-Have:
    * M1: Package and module exports across all 4 agents.
    * M2: Co-Teacher LangGraph nodes (message extraction & answer generation).
    * M3: Quiz Engine LangGraph execution with valid signatures.
    * M4: Backward-compatibility shims (app.chains & app.graphs).
- Should-Have:
    * S1: Stateless agent chains (Code Explainer & Hint Generator).
    * S2: Co-Teacher greeting personalization with diverse metadata formats.
    * S3: Quiz Feedback chain with boolean normalization.
"""
from unittest.mock import MagicMock, patch
import pytest
from langchain_core.messages import HumanMessage, AIMessage

# Must-Have Imports
from app.agents import (
    create_co_teacher_chain,
    create_greeting_chain,
    create_code_explainer_chain,
    create_hint_generator_chain,
    create_quiz_feedback_chain,
    create_quiz_engine_chain,
)
from app.agents.co_teacher import (
    create_qa_graph,
    run_qa_graph,
    generate_greeting,
    answer_question,
)
from app.agents.co_teacher.graph import retrieve_context_node, generate_answer_node
from app.agents.code_explainer import explain_code
from app.agents.code_explainer.graph import get_explainer_graph
from app.agents.hint_generator import generate_hint
from app.agents.hint_generator.graph import get_hint_graph
from app.agents.quiz_engine import (
    create_quiz_graph,
    generate_quiz_direct,
    generate_feedback,
)
from app.agents.quiz_engine.graph import generate_quiz_node


# ═══════════════════════════════════════════════════════════════════════════
# MUST-HAVE (M) TESTS
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.unit
def test_must_have_agents_package_exports():
    """M1: Verify app.agents exports all 6 chain factories and subpackage interfaces."""
    factories = [
        create_co_teacher_chain,
        create_greeting_chain,
        create_code_explainer_chain,
        create_hint_generator_chain,
        create_quiz_feedback_chain,
        create_quiz_engine_chain,
        create_qa_graph,
        run_qa_graph,
        answer_question,
        create_quiz_graph,
    ]
    for factory in factories:
        assert callable(factory), f"Factory {factory} must be callable"


@pytest.mark.unit
def test_must_have_co_teacher_context_node_polymorphism():
    """M2: Verify retrieve_context_node safely parses HumanMessage and dict messages."""
    # Case 1: HumanMessage
    state_msg = {
        "messages": [HumanMessage(content="Bagaimana cara kerja list di Python?")],
        "course_id": "python-101",
    }
    with patch("app.agents.co_teacher.graph.get_course_context", return_value="Materi list Python"):
        res = retrieve_context_node(state_msg)
        assert res["rag_context"] == "Materi list Python"

    # Case 2: Dict message format (student role)
    state_dict = {
        "messages": [{"role": "student", "content": "Apa itu dictionary?"}],
        "course_id": "python-101",
    }
    with patch("app.agents.co_teacher.graph.get_course_context", return_value="Materi dict Python"):
        res = retrieve_context_node(state_dict)
        assert res["rag_context"] == "Materi dict Python"


@pytest.mark.unit
def test_must_have_co_teacher_answer_node():
    """M2: Verify generate_answer_node invokes LLM and wraps response in AIMessage."""
    state = {
        "messages": [HumanMessage(content="Halo Maguru")],
        "session_title": "Dasar",
        "session_content": "Materi dasar",
        "rag_context": "Konteks dasar",
    }
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = AIMessage(content="Halo! Saya siap membantu belajarmu.")

    with patch("app.agents.co_teacher.graph.get_llm", return_value=mock_llm):
        res = generate_answer_node(state)
        assert "messages" in res
        assert len(res["messages"]) == 1
        assert "Halo! Saya siap membantu belajarmu." in res["messages"][0].content


@pytest.mark.unit
def test_must_have_quiz_engine_graph_node_signature():
    """M3: Verify generate_quiz_node passes correct parameters to generate_quiz_questions without error."""
    state = {
        "course_id": "course-python-101",
        "topic": "Looping",
        "content": "Pengulangan for dan while",
        "quiz_type": "section_quiz",
        "num_questions": 3,
        "difficulty": "medium",
        "questions": [],
        "status": "init",
    }

    mock_questions = [
        {"question": "Soal 1", "options": {"a": "1", "b": "2"}, "correct": "a"},
        {"question": "Soal 2", "options": {"a": "1", "b": "2"}, "correct": "b"},
        {"question": "Soal 3", "options": {"a": "1", "b": "2"}, "correct": "a"},
    ]

    with patch(
        "app.agents.quiz_engine.graph.generate_quiz_questions",
        return_value=mock_questions
    ) as mock_func:
        res = generate_quiz_node(state)

        # Assert correct keyword arguments were passed
        mock_func.assert_called_once_with(
            course_id="course-python-101",
            course_title="Looping",
            lesson_content="Pengulangan for dan while",
            num_questions=3,
            difficulty="medium",
        )
        assert res["status"] == "generated"
        assert len(res["questions"]) == 3


@pytest.mark.unit
def test_must_have_quiz_engine_direct_runner():
    """M3: Verify generate_quiz_direct compiles graph and returns expected response shape."""
    mock_questions = [{"question": "Soal Direct", "options": {"a": "A", "b": "B"}, "correct": "a"}]
    with patch(
        "app.agents.quiz_engine.graph.generate_quiz_questions",
        return_value=mock_questions
    ):
        result = generate_quiz_direct(
            topic="Functions",
            content="Definisi def di python",
            course_id="course-123",
            num_questions=1,
            difficulty="easy",
            thread_id="test-thread-direct",
        )
        assert result["status"] == "generated"
        assert result["course_id"] == "course-123"
        assert result["thread_id"] == "test-thread-direct"
        assert len(result["questions"]) == 1


@pytest.mark.unit
def test_must_have_backward_compatibility_shims():
    """M4: Verify legacy import paths in app.chains and app.graphs continue to resolve."""
    from app.chains import (
        create_qa_chatbot_chain,
        answer_question as shim_answer_question,
        create_explain_code_chain,
        explain_code as shim_explain_code,
        create_hint_generator_chain as shim_hint_chain,
        generate_hint as shim_generate_hint,
        create_quiz_feedback_chain as shim_feedback_chain,
        generate_feedback as shim_generate_feedback,
        create_greeting_chain as shim_greeting_chain,
        generate_greeting as shim_generate_greeting,
    )
    from app.graphs import (
        QAState,
        create_qa_graph as shim_create_qa_graph,
        run_qa_graph as shim_run_qa_graph,
        QuizState,
        create_quiz_graph as shim_create_quiz_graph,
        generate_quiz_direct as shim_generate_quiz_direct,
    )

    assert QAState is not None
    assert QuizState is not None
    assert callable(create_qa_chatbot_chain)
    assert callable(shim_answer_question)
    assert callable(create_explain_code_chain)
    assert callable(shim_explain_code)
    assert callable(shim_hint_chain)
    assert callable(shim_generate_hint)
    assert callable(shim_feedback_chain)
    assert callable(shim_generate_feedback)
    assert callable(shim_greeting_chain)
    assert callable(shim_generate_greeting)
    assert callable(shim_create_qa_graph)
    assert callable(shim_run_qa_graph)
    assert callable(shim_create_quiz_graph)
    assert callable(shim_generate_quiz_direct)


# ═══════════════════════════════════════════════════════════════════════════
# SHOULD-HAVE (S) TESTS
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.unit
def test_should_have_stateless_agent_chains():
    """S1: Verify Code Explainer and Hint Generator return graceful prompt responses."""
    # Empty inputs return immediate helpful guidance without hitting LLM
    expl = explain_code("")
    assert "Silakan masukkan potongan kode" in expl

    mock_llm = MagicMock()
    mock_llm.invoke.return_value = AIMessage(content="Petunjuk langkah pertama: cek tanda titik dua")
    with patch("app.agents.hint_generator.entrypoint.get_llm", return_value=mock_llm):
        hint = generate_hint(task="Buat loop", student_attempt="for i in range(5)", level=1)
        assert len(hint) > 0


@pytest.mark.unit
def test_should_have_co_teacher_greeting_metadata_variations():
    """S2: Verify greeting handles dict metadata, str metadata, and none gracefully."""
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = AIMessage(content="Halo Budi! Selamat datang di kursus.")

    with patch("app.agents.co_teacher.greeting.get_llm", return_value=mock_llm):
        # 1. Dict metadata
        greet_dict = generate_greeting("Budi", {"title": "Python Dasar", "learning_objectives": "Variabel"})
        assert len(greet_dict) > 0

        # 2. String metadata
        greet_str = generate_greeting("Siti", "Struktur Data")
        assert len(greet_str) > 0

        # 3. None / fallback
        greet_none = generate_greeting("", None)  # type: ignore[arg-type]
        assert len(greet_none) > 0


@pytest.mark.unit
def test_should_have_quiz_feedback_chain():
    """S3: Verify quiz feedback formatting."""
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = AIMessage(content="Jawaban Anda tepat sekali!")

    with patch("app.agents.quiz_engine.entrypoint.get_llm", return_value=mock_llm):
        fb = generate_feedback(
            question="Apa tipe data angka bulat?",
            student_answer="int",
            correct_answer="int",
            is_correct=True,
        )
        assert len(fb) > 0


@pytest.mark.unit
def test_should_have_code_explainer_and_hint_graphs():
    """S4: Verify Code Explainer and Hint Generator LangGraph graphs."""
    explainer_g = get_explainer_graph()
    hint_g = get_hint_graph()

    assert explainer_g is not None
    assert hint_g is not None

    with patch("app.agents.code_explainer.graph.explain_code", return_value="Penjelasan kode test"):
        res = explainer_g.invoke({"code": "x = 10", "explanation": None})
        assert res.get("explanation") == "Penjelasan kode test"

    with patch("app.agents.hint_generator.graph.generate_hint", return_value="Petunjuk langkah 1"):
        res_h = hint_g.invoke({"task": "Buat fungsi", "attempt": "def foo():", "level": 1, "hint": None})
        assert res_h.get("hint") == "Petunjuk langkah 1"

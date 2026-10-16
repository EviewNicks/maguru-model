"""
Co-Teacher Agent — Stateful LangGraph workflow with multi-turn memory, RAG retrieval,
and multi-model LLM failover streaming.

Migrated from: app/graphs/qa_graph.py
"""
import uuid
import logging
import operator
from typing import List, Dict, Any, Optional, AsyncIterator, Annotated
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

from app.shared import (
    get_llm,
    get_llm_pool,
    get_checkpointer,
    get_store,
    get_student_profile,
    get_course_context,
)

logger = logging.getLogger(__name__)


class QAState(TypedDict):
    """State definition for Co-Teacher LangGraph with multi-turn memory and long-term student store."""
    messages: Annotated[List[BaseMessage], operator.add]
    course_id: Optional[str]
    session_title: Optional[str]
    session_content: Optional[str]
    rag_context: Optional[str]
    student_id: Optional[str]


# ─── Graph Nodes ─────────────────────────────────────────────────────────────

def retrieve_context_node(state: QAState) -> Dict[str, Any]:
    """Retrieve relevant RAG context from vector store based on the latest question."""
    course_id = state.get("course_id")
    messages = state.get("messages", [])

    query = ""
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            query = str(msg.content)
            break
        elif isinstance(msg, dict) and msg.get("role") in ("user", "student"):
            query = str(msg.get("content", ""))
            break

    rag_context = ""
    if course_id and query:
        try:
            rag_context = get_course_context(course_id=course_id, query=query)
        except Exception as e:
            logger.warning(f"[CoTeacher][RAG] Retrieval warning: {str(e)}")

    if not rag_context:
        rag_context = "Gunakan pengetahuan dasar pemrograman secara umum."

    return {"rag_context": rag_context}


def _read_profile_dict(student_id: str, store: Any = None) -> Dict[str, Any]:
    """Read student profile dictionary from store or fallback helper."""
    if store is not None:
        try:
            item = store.get(("students", student_id), "profile")
            if item and hasattr(item, "value") and isinstance(item.value, dict):
                return item.value
        except Exception as e:
            logger.warning(f"[CoTeacher][Store] Could not read from store: {str(e)}")
    return get_student_profile(student_id)


def _format_student_profile(student_id: Optional[str], store: Any = None) -> str:
    """Format student long-term profile into concise system prompt context."""
    if not student_id:
        return ""
    data = _read_profile_dict(student_id, store)
    if not data:
        return ""

    parts = [
        f"Materi yang sedang dipelajari/perlu bimbingan: {data.get('weaknesses') or data.get('struggles')}"
        if (data.get("weaknesses") or data.get("struggles")) else "",
        f"Materi yang sudah dikuasai: {data.get('mastered')}" if data.get("mastered") else "",
        f"Preferensi gaya belajar: {data.get('learning_style')}" if data.get("learning_style") else "",
    ]
    valid_parts = [p for p in parts if p]
    if not valid_parts:
        return ""
    return "\nProfil Siswa (Memori Jangka Panjang):\n- " + "\n- ".join(valid_parts)


def _build_conversation_messages(system_instruction: str, messages: List[Any]) -> List[BaseMessage]:
    """Convert polymorphic state messages into standard langchain BaseMessages."""
    conversation: List[BaseMessage] = [SystemMessage(content=system_instruction)]
    for msg in messages:
        if isinstance(msg, (HumanMessage, AIMessage, SystemMessage)):
            conversation.append(msg)
        elif isinstance(msg, dict):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role in ("user", "student"):
                conversation.append(HumanMessage(content=content))
            else:
                conversation.append(AIMessage(content=content))
    return conversation


def generate_answer_node(state: QAState, *, store=None) -> Dict[str, Any]:
    """Generate assistant response using LLM with context, conversation history, and student profile."""
    llm = get_llm()
    messages = state.get("messages", [])
    session_title = state.get("session_title") or "Umum"
    session_content = (state.get("session_content") or "")[:1000]
    rag_context = state.get("rag_context") or ""
    student_id = state.get("student_id") or ""

    student_profile = _format_student_profile(student_id, store)
    system_instruction = (
        f"Anda adalah Maguru AI Co-Teacher. Jawab pertanyaan siswa dengan ramah dan ringkas dalam Bahasa Indonesia.\n"
        f"Topik Sesi: {session_title}\n"
        f"Materi Singkat: {session_content}\n"
        f"Konteks Materi Kursus (RAG): {rag_context}\n"
        f"{student_profile}\n"
    )

    conversation = _build_conversation_messages(system_instruction, messages)

    try:
        response = llm.invoke(conversation)
        ai_content = response.content if hasattr(response, "content") else str(response)
        return {"messages": [AIMessage(content=ai_content)]}
    except Exception as e:
        logger.error(f"[CoTeacher][LLM] Error invoking LLM: {str(e)}", exc_info=True)
        return {"messages": [AIMessage(content=f"Maaf, terjadi kendala saat memproses jawaban: {str(e)}")]}


# ─── Graph Factory ────────────────────────────────────────────────────────────

def create_qa_graph():
    """Create and compile Co-Teacher LangGraph with checkpointer persistence and long-term Store."""
    workflow = StateGraph(QAState)
    workflow.add_node("retrieve_context", retrieve_context_node)
    workflow.add_node("generate_answer", generate_answer_node)

    workflow.add_edge(START, "retrieve_context")
    workflow.add_edge("retrieve_context", "generate_answer")
    workflow.add_edge("generate_answer", END)

    checkpointer = get_checkpointer()
    store = get_store()
    return workflow.compile(checkpointer=checkpointer, store=store)


_qa_graph = None


def get_qa_graph():
    """Get singleton compiled Co-Teacher graph."""
    global _qa_graph
    if _qa_graph is None:
        _qa_graph = create_qa_graph()
    return _qa_graph


# ─── Public Runners ───────────────────────────────────────────────────────────

def run_qa_graph(
    question: str,
    course_id: Optional[str] = None,
    session_title: Optional[str] = None,
    session_content: Optional[str] = None,
    thread_id: Optional[str] = None,
    student_id: Optional[str] = None,
) -> str:
    """Execute Co-Teacher graph synchronously with thread-based state persistence and store."""
    graph = get_qa_graph()
    thread_key = thread_id or f"session-{course_id or 'global'}-{uuid.uuid4()}"
    config = {
        "configurable": {
            "thread_id": thread_key,
            "user_id": student_id or "default",
        }
    }

    initial_state = {
        "messages": [HumanMessage(content=question)],
        "course_id": course_id,
        "session_title": session_title,
        "session_content": session_content,
        "rag_context": "",
        "student_id": student_id,
    }

    result = graph.invoke(initial_state, config=config)
    messages = result.get("messages", [])
    if messages:
        last_msg = messages[-1]
        return last_msg.content if hasattr(last_msg, "content") else str(last_msg)
    return "Tidak ada respons."


def _build_rag_context(course_id: Optional[str], question: str) -> str:
    """Retrieve RAG context safely without raising exceptions."""
    if not course_id:
        return ""
    try:
        return get_course_context(course_id=course_id, query=question)
    except Exception:
        return ""


def _persist_stream_result(
    thread_key: str,
    question: str,
    full_response: str,
    course_id: Optional[str],
    session_title: Optional[str],
    session_content: Optional[str],
    rag_context: str,
    student_id: Optional[str] = None,
) -> None:
    """Safely persist conversation turn into LangGraph checkpointer."""
    try:
        graph = get_qa_graph()
        config = {
            "configurable": {
                "thread_id": thread_key,
                "user_id": student_id or "default",
            }
        }
        graph.update_state(
            config,
            {
                "messages": [HumanMessage(content=question), AIMessage(content=full_response)],
                "course_id": course_id,
                "session_title": session_title,
                "session_content": session_content,
                "rag_context": rag_context,
                "student_id": student_id,
            },
        )
    except Exception as e:
        logger.warning(f"[CoTeacher][PERSIST] Could not update graph state: {str(e)}")


async def astream_qa_graph(
    question: str,
    course_id: Optional[str] = None,
    session_title: Optional[str] = None,
    session_content: Optional[str] = None,
    thread_id: Optional[str] = None,
    student_id: Optional[str] = None,
) -> AsyncIterator[str]:
    """Stream token-by-token async response with multi-model failover and student profile."""
    thread_key = thread_id or f"session-{course_id or 'global'}-{uuid.uuid4()}"
    rag_context = _build_rag_context(course_id, question)

    student_profile_text = _format_student_profile(student_id)

    system_instruction = (
        f"Anda adalah Maguru AI Co-Teacher. Jawab pertanyaan siswa dengan ramah dan ringkas dalam Bahasa Indonesia.\n"
        f"Topik Sesi: {session_title or 'Umum'}\n"
        f"Materi Singkat: {(session_content or '')[:1000]}\n"
        f"Konteks Materi Kursus (RAG): {rag_context or 'Pengetahuan umum'}\n"
        f"{student_profile_text}\n"
    )

    messages = [
        SystemMessage(content=system_instruction),
        HumanMessage(content=question),
    ]

    llm_pool = get_llm_pool()
    full_response = ""
    stream_successful = False

    for candidate_llm in llm_pool:
        try:
            async for chunk in candidate_llm.astream(messages):
                token = str(chunk.content) if hasattr(chunk, "content") else str(chunk)
                full_response += token
                yield token
            stream_successful = True
            break
        except Exception as e:
            model_name = getattr(candidate_llm, "model_name", "unknown")
            logger.warning(
                f"[CoTeacher][STREAM] Model '{model_name}' failed ({str(e)}). Trying next..."
            )

    if not stream_successful:
        err = "\n[Maaf, seluruh model di pool sedang sibuk atau mengalami kendala koneksi.]"
        full_response += err
        yield err

    _persist_stream_result(
        thread_key=thread_key,
        question=question,
        full_response=full_response,
        course_id=course_id,
        session_title=session_title,
        session_content=session_content,
        rag_context=rag_context,
        student_id=student_id,
    )

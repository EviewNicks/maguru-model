"""
Co-Teacher Agent — LangServe-compatible entrypoint.

Exposes:
  - create_co_teacher_chain()  → LangServe LCEL runnable (SSE streaming)
  - answer_question()          → sync helper used by REST API endpoints
"""
import time
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from app.shared import get_llm, get_course_context
from app.schemas.chat import ChatInputSchema
from app.agents.co_teacher.graph import run_qa_graph

logger = logging.getLogger(__name__)

_PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "qa_chatbot.yaml"


def _format_history(messages: list) -> str:
    """Format last 5 chat messages for prompt injection."""
    if not messages:
        return "Belum ada riwayat chat."
    formatted = []
    for msg in messages[-5:]:
        if isinstance(msg, dict):
            role = "Siswa" if msg.get("role") in ("student", "user") else "AI"
            formatted.append(f"{role}: {msg.get('content', '')}")
        else:
            role = "Siswa" if getattr(msg, "role", "") in ("student", "user") else "AI"
            formatted.append(f"{role}: {getattr(msg, 'content', '')}")
    return "\n".join(formatted)


def _prepare_inputs(input_data: Any) -> Dict[str, str]:
    """Preprocess inputs: extract fields, enrich with RAG context."""
    t_start = time.time()

    if isinstance(input_data, dict):
        q = input_data.get("question", "")
        st = input_data.get("session_title", "")
        sc = input_data.get("session_content", "")
        ch = input_data.get("chat_history", [])
        cid = input_data.get("course_id", None)
        tid = input_data.get("thread_id", None)
    else:
        q = getattr(input_data, "question", "")
        st = getattr(input_data, "session_title", "")
        sc = getattr(input_data, "session_content", "")
        ch = getattr(input_data, "chat_history", [])
        cid = getattr(input_data, "course_id", None)
        tid = getattr(input_data, "thread_id", None)

    logger.info(
        f"[CoTeacher][INPUT] ThreadID='{tid}' Course='{cid}' Session='{st}' Q='{q[:60]}...'"
    )

    rag_context = ""
    if cid and q:
        try:
            rag_context = get_course_context(course_id=cid, query=q)
            logger.info(f"[CoTeacher][RAG] {len(rag_context)} chars retrieved for course='{cid}'")
        except Exception as e:
            logger.warning(f"[CoTeacher][RAG] Skipped: {str(e)}")

    if not rag_context:
        rag_context = "Gunakan pengetahuan dasar pemrograman dan materi yang relevan."

    logger.info(
        f"[CoTeacher][READY] Preprocessing done in {(time.time() - t_start) * 1000:.1f}ms"
    )

    return {
        "question": q or "Halo",
        "session_title": st or "Dasar",
        "session_content": (sc or "")[:1000],
        "chat_history": _format_history(ch or []),
        "rag_context": rag_context,
    }


def create_co_teacher_chain():
    """
    Create LangServe-compatible LCEL chain for the Co-Teacher agent.
    Supports SSE token-by-token streaming via /chatbot/stream.
    """
    _prompt = load_prompt(str(_PROMPT_PATH))
    chain = RunnableLambda(_prepare_inputs) | _prompt | get_llm() | StrOutputParser()
    return chain.with_types(input_type=ChatInputSchema)


def answer_question(
    question: str,
    session_title: Optional[str] = "",
    session_content: Optional[str] = "",
    chat_history: Optional[List[Dict[str, Any]]] = None,
    course_id: Optional[str] = None,
    thread_id: Optional[str] = None,
) -> str:
    """
    Answer student question using LangGraph (with memory) with LCEL fallback.
    Used by REST API endpoints that don't need streaming.
    """
    if not question or not question.strip():
        return "Halo! Saya adalah Maguru AI Co-Teacher. Silakan ajukan pertanyaan Anda!"

    try:
        return run_qa_graph(
            question=question,
            course_id=course_id,
            session_title=session_title,
            session_content=session_content,
            thread_id=thread_id,
        )
    except Exception as e:
        logger.warning(f"[CoTeacher] LangGraph fallback to LCEL: {str(e)}")

    try:
        chain = create_co_teacher_chain()
        return chain.invoke({
            "question": question,
            "session_title": session_title,
            "session_content": session_content,
            "chat_history": chat_history,
            "course_id": course_id,
            "thread_id": thread_id,
        })
    except Exception as e:
        logger.error(f"[CoTeacher][ERROR] {str(e)}", exc_info=True)
        return f"Maaf, saya tidak bisa menjawab sekarang. Error: {str(e)}"

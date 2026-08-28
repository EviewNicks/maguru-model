"""Q&A Chatbot Chain with LangGraph State Persistence and RAG context awareness."""
import os
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from app.core.llm import get_llm
from app.services.rag_service import get_course_context
from app.graphs.qa_graph import run_qa_graph
from app.schemas.chat import ChatInputSchema

logger = logging.getLogger(__name__)

_chain = None

def _get_chain():
    """Get or create LCEL chain (lazy initialization)."""
    global _chain
    if _chain is None:
        prompt_path = Path(__file__).parent.parent / "prompts" / "qa_chatbot.yaml"
        if not prompt_path.exists():
            prompt_path = Path(__file__).parent.parent.parent / "ai_chains" / "prompts" / "qa_chatbot.yaml"
        _prompt = load_prompt(str(prompt_path))
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain

def answer_question(
    question: str,
    session_title: Optional[str] = "",
    session_content: Optional[str] = "",
    chat_history: Optional[List[Dict[str, Any]]] = None,
    course_id: Optional[str] = None,
    thread_id: Optional[str] = None
) -> str:
    """Answer student question using LangGraph state persistence and RAG course context."""
    if not question or not question.strip():
        return "Halo! Saya adalah Maguru AI Co-Teacher. Silakan ajukan pertanyaan atau materi pemrograman yang ingin Anda pelajari!"

    # Attempt execution with LangGraph state persistence
    try:
        return run_qa_graph(
            question=question,
            course_id=course_id,
            session_title=session_title,
            session_content=session_content,
            thread_id=thread_id
        )
    except Exception as e:
        logger.warning(f"LangGraph execution fallback to LCEL chain: {str(e)}")

    # Fallback to direct LCEL chain execution
    history_text = _format_history(chat_history or [])
    rag_context = ""
    if course_id:
        try:
            rag_context = get_course_context(course_id=course_id, query=question)
        except Exception:
            pass

    if not rag_context:
        rag_context = "Tidak ada materi terpisah. Gunakan pengetahuan dasar."

    try:
        return _get_chain().invoke({
            "question": question,
            "session_title": session_title or "Dasar",
            "session_content": (session_content or "")[:1000],
            "chat_history": history_text,
            "rag_context": rag_context
        })
    except Exception as e:
        logger.error(f"Error in qa_chatbot answer_question fallback: {str(e)}", exc_info=True)
        return f"Maaf, saya tidak bisa menjawab pertanyaan ini sekarang. Error: {str(e)}"

def _format_history(messages: list) -> str:
    """Format chat messages for prompt."""
    if not messages:
        return "Belum ada riwayat chat."

    formatted = []
    for msg in messages[-5:]:
        role = "Siswa" if msg.get("role") in ("student", "user") else "AI"
        formatted.append(f"{role}: {msg.get('content', '')}")

    return "\n".join(formatted)

def create_qa_chatbot_chain():
    """Create LangServe-compatible runnable with explicit input schema."""
    def invoke(input_data: Any) -> str:
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

        return answer_question(
            question=q,
            session_title=st,
            session_content=sc,
            chat_history=ch,
            course_id=cid,
            thread_id=tid
        )
    return RunnableLambda(invoke).with_types(input_type=ChatInputSchema)

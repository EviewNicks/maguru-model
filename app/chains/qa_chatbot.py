"""Q&A Chatbot Chain with RAG and session context awareness."""
import os
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from app.core.llm import get_llm
from app.services.rag_service import get_course_context

logger = logging.getLogger(__name__)

_chain = None

def _get_chain():
    """Get or create chain (lazy initialization)."""
    global _chain
    if _chain is None:
        prompt_path = Path(__file__).parent.parent / "prompts" / "qa_chatbot.yaml"
        if not prompt_path.exists():
            # Fallback path check
            prompt_path = Path(__file__).parent.parent.parent / "ai_chains" / "prompts" / "qa_chatbot.yaml"
        _prompt = load_prompt(str(prompt_path))
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain

def answer_question(
    question: str,
    session_title: Optional[str] = "",
    session_content: Optional[str] = "",
    chat_history: Optional[List[Dict[str, Any]]] = None,
    course_id: Optional[str] = None
) -> str:
    """Answer student question using RAG course context and session context.

    Args:
        question: Student's question
        session_title: Current session title
        session_content: Session content snippet
        chat_history: List of recent messages
        course_id: Optional course ID to filter RAG vector store

    Returns:
        AI Co-Teacher response in Indonesian
    """
    history_text = _format_history(chat_history or [])
    
    # Retrieve RAG context from Supabase pgvector if course_id is provided
    rag_context = ""
    if course_id:
        rag_context = get_course_context(course_id=course_id, query=question)
    
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
        logger.error(f"Error in qa_chatbot answer_question: {str(e)}", exc_info=True)
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
    """Create LangServe-compatible runnable lambda."""
    def invoke(input_dict: dict) -> str:
        return answer_question(
            question=input_dict.get("question", ""),
            session_title=input_dict.get("session_title", ""),
            session_content=input_dict.get("session_content", ""),
            chat_history=input_dict.get("chat_history", []),
            course_id=input_dict.get("course_id", None)
        )
    return RunnableLambda(invoke)

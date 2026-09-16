"""Q&A Chatbot Chain with LangGraph State Persistence, LCEL Real-Time Streaming, RAG Context, and End-to-End Tracing."""
import os
import time
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

def _format_history(messages: list) -> str:
    """Format chat messages for prompt."""
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
    """Prepare inputs for LCEL prompt pipeline with RAG enrichment and structured debug logging."""
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

    logger.info(f"[BACKEND_QA][INPUT_RECEIVED] ThreadID: '{tid}' | Course: '{cid}' | Session: '{st}' | Question: '{q[:60]}...'")

    # RAG Context Retrieval
    rag_context = ""
    if cid and q:
        try:
            rag_context = get_course_context(course_id=cid, query=q)
            logger.info(f"[BACKEND_QA][RAG_LOOKUP] Retrieved {len(rag_context)} chars of context for course '{cid}'")
        except Exception as e:
            logger.warning(f"[BACKEND_QA][RAG_WARNING] Retrieval skipped/failed: {str(e)}")

    if not rag_context:
        rag_context = "Gunakan pengetahuan dasar pemrograman dan materi yang relevan."

    history_text = _format_history(ch or [])
    logger.info(f"[BACKEND_QA][PIPELINE_READY] Preprocessing completed in {(time.time() - t_start)*1000:.1f}ms. Dispatching to LLM Stream...")

    return {
        "question": q or "Halo",
        "session_title": st or "Dasar",
        "session_content": (sc or "")[:1000],
        "chat_history": history_text,
        "rag_context": rag_context
    }

def create_qa_chatbot_chain():
    """Create LangServe-compatible LCEL runnable with token-by-token streaming support."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "qa_chatbot.yaml"
    if not prompt_path.exists():
        prompt_path = Path(__file__).parent.parent.parent / "ai_chains" / "prompts" / "qa_chatbot.yaml"

    _prompt = load_prompt(str(prompt_path))
    
    # Native LCEL pipeline: Preprocess -> Prompt -> LLM with Fallbacks & Timeout -> String Output Parser
    chain = RunnableLambda(_prepare_inputs) | _prompt | get_llm() | StrOutputParser()
    return chain.with_types(input_type=ChatInputSchema)

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

    try:
        return run_qa_graph(
            question=question,
            course_id=course_id,
            session_title=session_title,
            session_content=session_content,
            thread_id=thread_id
        )
    except Exception as e:
        logger.warning(f"[BACKEND_QA] LangGraph execution fallback to LCEL chain: {str(e)}")

    try:
        chain = create_qa_chatbot_chain()
        return chain.invoke({
            "question": question,
            "session_title": session_title,
            "session_content": session_content,
            "chat_history": chat_history,
            "course_id": course_id,
            "thread_id": thread_id
        })
    except Exception as e:
        logger.error(f"[BACKEND_QA][ERROR] in answer_question fallback: {str(e)}", exc_info=True)
        return f"Maaf, saya tidak bisa menjawab pertanyaan ini sekarang. Error: {str(e)}"
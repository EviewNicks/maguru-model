"""Stateful LangGraph Workflow for Q&A Chatbot with Memory & RAG Retrieval."""
import os
import uuid
import logging
import operator
from pathlib import Path
from typing import List, Dict, Any, Optional, AsyncIterator, Annotated
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import load_prompt
from langgraph.graph import StateGraph, START, END

from app.core.llm import get_llm, get_llm_pool
from app.db.checkpointer import get_checkpointer
from app.services.rag_service import get_course_context

logger = logging.getLogger(__name__)

class QAState(TypedDict):
    """State definition for LangGraph QA Assistant with memory."""
    messages: Annotated[List[BaseMessage], operator.add]
    course_id: Optional[str]
    session_title: Optional[str]
    session_content: Optional[str]
    rag_context: Optional[str]

def retrieve_context_node(state: QAState) -> Dict[str, Any]:
    """Retrieve relevant RAG context from vector store based on the latest question."""
    course_id = state.get("course_id")
    messages = state.get("messages", [])
    
    query = ""
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage) or (isinstance(msg, dict) and msg.get("role") in ("user", "student")):
            query = msg.content if hasattr(msg, "content") else msg.get("content", "")
            break
            
    rag_context = ""
    if course_id and query:
        try:
            rag_context = get_course_context(course_id=course_id, query=query)
        except Exception as e:
            logger.warning(f"RAG retrieval in qa_graph warning: {str(e)}")
            
    if not rag_context:
        rag_context = "Gunakan pengetahuan dasar pemrograman secara umum."
        
    return {"rag_context": rag_context}

def generate_answer_node(state: QAState) -> Dict[str, Any]:
    """Generate assistant response using LLM with context awareness and fallbacks."""
    llm = get_llm()
    messages = state.get("messages", [])
    session_title = state.get("session_title") or "Umum"
    session_content = (state.get("session_content") or "")[:1000]
    rag_context = state.get("rag_context") or ""

    system_instruction = (
        f"Anda adalah Maguru AI Co-Teacher. Jawab pertanyaan siswa dengan ramah dan ringkas dalam Bahasa Indonesia.\n"
        f"Topik Sesi: {session_title}\n"
        f"Materi Singkat: {session_content}\n"
        f"Konteks Materi Kursus (RAG): {rag_context}\n"
    )

    conversation_messages = [SystemMessage(content=system_instruction)]
    for msg in messages:
        if isinstance(msg, (HumanMessage, AIMessage, SystemMessage)):
            conversation_messages.append(msg)
        elif isinstance(msg, dict):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role in ("user", "student"):
                conversation_messages.append(HumanMessage(content=content))
            else:
                conversation_messages.append(AIMessage(content=content))

    try:
        response = llm.invoke(conversation_messages)
        ai_content = response.content if hasattr(response, "content") else str(response)
        return {"messages": [AIMessage(content=ai_content)]}
    except Exception as e:
        logger.error(f"Error invoking LLM in qa_graph: {str(e)}", exc_info=True)
        return {"messages": [AIMessage(content=f"Maaf, terjadi kendala saat memproses jawaban: {str(e)}")]}

def create_qa_graph():
    """Create and compile LangGraph QA StateGraph with checkpointer persistence."""
    workflow = StateGraph(QAState)
    workflow.add_node("retrieve_context", retrieve_context_node)
    workflow.add_node("generate_answer", generate_answer_node)

    workflow.add_edge(START, "retrieve_context")
    workflow.add_edge("retrieve_context", "generate_answer")
    workflow.add_edge("generate_answer", END)

    checkpointer = get_checkpointer()
    return workflow.compile(checkpointer=checkpointer)

_qa_graph = None

def get_qa_graph():
    """Get singleton compiled QA graph."""
    global _qa_graph
    if _qa_graph is None:
        _qa_graph = create_qa_graph()
    return _qa_graph

def run_qa_graph(
    question: str,
    course_id: Optional[str] = None,
    session_title: Optional[str] = None,
    session_content: Optional[str] = None,
    thread_id: Optional[str] = None
) -> str:
    """Execute QA graph synchronously with thread-based state persistence."""
    graph = get_qa_graph()
    thread_key = thread_id or f"session-{course_id or 'global'}-{uuid.uuid4()}"
    config = {"configurable": {"thread_id": thread_key}}

    initial_state = {
        "messages": [HumanMessage(content=question)],
        "course_id": course_id,
        "session_title": session_title,
        "session_content": session_content,
        "rag_context": ""
    }

    result = graph.invoke(initial_state, config=config)
    messages = result.get("messages", [])
    if messages:
        last_msg = messages[-1]
        return last_msg.content if hasattr(last_msg, "content") else str(last_msg)
    return "Tidak ada respons."

async def astream_qa_graph(
    question: str,
    course_id: Optional[str] = None,
    session_title: Optional[str] = None,
    session_content: Optional[str] = None,
    thread_id: Optional[str] = None
) -> AsyncIterator[str]:
    """Stream token-by-token response asynchronously with multi-model fallback failover."""
    thread_key = thread_id or f"session-{course_id or 'global'}-{uuid.uuid4()}"
    
    # Retrieve RAG context
    rag_context = ""
    if course_id:
        try:
            rag_context = get_course_context(course_id=course_id, query=question)
        except Exception:
            pass

    system_instruction = (
        f"Anda adalah Maguru AI Co-Teacher. Jawab pertanyaan siswa dengan ramah dan ringkas dalam Bahasa Indonesia.\n"
        f"Topik Sesi: {session_title or 'Umum'}\n"
        f"Materi Singkat: {(session_content or '')[:1000]}\n"
        f"Konteks Materi Kursus (RAG): {rag_context or 'Pengetahuan umum'}\n"
    )

    messages = [
        SystemMessage(content=system_instruction),
        HumanMessage(content=question)
    ]

    llm_pool = get_llm_pool()
    full_response = ""
    stream_successful = False

    # Try models in pool in sequence until stream succeeds
    for candidate_llm in llm_pool:
        try:
            async for chunk in candidate_llm.astream(messages):
                token = chunk.content if hasattr(chunk, "content") else str(chunk)
                full_response += token
                yield token
            stream_successful = True
            break
        except Exception as e:
            logger.warning(f"Streaming failed with model '{candidate_llm.model_name}' ({str(e)}). Switching to next model...")

    if not stream_successful:
        err = "\n[Maaf, seluruh model di pool sedang sibuk atau mengalami kendala koneksi.]"
        full_response += err
        yield err

    # Persist state into checkpointer
    try:
        graph = get_qa_graph()
        config = {"configurable": {"thread_id": thread_key}}
        graph.update_state(
            config,
            {
                "messages": [HumanMessage(content=question), AIMessage(content=full_response)],
                "course_id": course_id,
                "session_title": session_title,
                "session_content": session_content,
                "rag_context": rag_context
            }
        )
    except Exception as e:
        logger.warning(f"Could not update graph state after stream: {str(e)}")

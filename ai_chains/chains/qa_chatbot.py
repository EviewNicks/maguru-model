"""Q&A chatbot chain with context awareness."""

from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from . import get_llm

# Lazy chain initialization
_chain = None

def _get_chain():
    """Get or create chain (lazy initialization)."""
    global _chain
    if _chain is None:
        _prompt = load_prompt("ai_chains/prompts/qa_chatbot.yaml")
        _chain = _prompt | get_llm() | StrOutputParser()
    return _chain

def answer_question(question: str, session_title: str,
                   session_content: str, chat_history: list) -> str:
    """Answer student question with session context.

    Args:
        question: Student's question
        session_title: Current session title
        session_content: Session markdown content
        chat_history: List of recent messages (max 10)

    Returns:
        Answer in Indonesian
    """
    # Format chat history for prompt
    history_text = _format_history(chat_history)

    try:
        return _get_chain().invoke({
            "question": question,
            "session_title": session_title,
            "session_content": session_content[:1000],  # Limit content
            "chat_history": history_text
        })
    except Exception as e:
        return f"Maaf, saya tidak bisa menjawab sekarang. Error: {str(e)}"

def _format_history(messages: list) -> str:
    """Format chat messages for prompt."""
    if not messages:
        return "Belum ada riwayat chat."

    formatted = []
    for msg in messages[-5:]:  # Last 5 messages
        role = "Siswa" if msg.get("role") == "student" else "AI"
        formatted.append(f"{role}: {msg.get('content', '')}")

    return "\n".join(formatted)

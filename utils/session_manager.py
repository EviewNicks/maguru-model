"""Session state management for Maguru MVP.

This module provides functions to manage Streamlit session state,
including progress tracking, quiz scores, and chat history.
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional


def init_session() -> None:
    """Initialize session state with default values.

    Creates session state keys:
    - initialized: bool = True
    - current_course: str = ""
    - current_module: str = ""
    - current_session: str = ""
    - completed_sessions: List[str] = []
    - quiz_scores: Dict[str, Dict] = {}
    - chat_history: List[Dict] = []
    - student_name: str = ""
    """
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.current_course = ""
        st.session_state.current_module = ""
        st.session_state.current_session = ""
        st.session_state.completed_sessions = []
        st.session_state.quiz_scores = {}
        st.session_state.chat_history = []
        st.session_state.student_name = ""


def update_progress(course_id: str, module_id: str, session_id: str) -> None:
    """Mark a session as completed.

    Args:
        course_id: Course identifier
        module_id: Module identifier
        session_id: Session identifier

    Side effects:
        Adds session_id to completed_sessions list if not already present
    """
    init_session()
    session_key = f"{course_id}/{module_id}/{session_id}"

    if session_key not in st.session_state.completed_sessions:
        st.session_state.completed_sessions.append(session_key)


def get_current_session() -> Dict[str, str]:
    """Retrieve current learning session.

    Returns:
        Dict with keys: course, module, session
    """
    init_session()
    return {
        "course": st.session_state.current_course,
        "module": st.session_state.current_module,
        "session": st.session_state.current_session,
    }


def save_quiz_score(quiz_id: str, score: int, total: int, passed: bool) -> None:
    """Store quiz results.

    Args:
        quiz_id: Quiz identifier
        score: Points earned
        total: Total possible points
        passed: Whether score >= 70%

    Side effects:
        Adds entry to quiz_scores dict with timestamp
    """
    init_session()

    # Track attempt number
    if quiz_id in st.session_state.quiz_scores:
        attempt = st.session_state.quiz_scores[quiz_id].get("attempt", 0) + 1
    else:
        attempt = 1

    st.session_state.quiz_scores[quiz_id] = {
        "score": score,
        "total": total,
        "passed": passed,
        "timestamp": datetime.now().isoformat(),
        "attempt": attempt,
    }


def get_chat_history() -> List[Dict[str, str]]:
    """Get recent chat messages (max 10).

    Returns:
        List of dicts with keys: role, content, timestamp
    """
    init_session()
    return st.session_state.chat_history


def add_chat_message(role: str, content: str) -> None:
    """Add message to chat history.

    Args:
        role: "student" or "ai"
        content: Message text

    Side effects:
        Appends to chat_history, maintains max 10 messages (FIFO)
    """
    init_session()

    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(),
    }

    st.session_state.chat_history.append(message)

    # Maintain max 10 messages (FIFO - remove oldest)
    if len(st.session_state.chat_history) > 10:
        st.session_state.chat_history = st.session_state.chat_history[-10:]


def is_session_completed(session_id: str) -> bool:
    """Check if session is completed.

    Args:
        session_id: Session identifier

    Returns:
        True if session_id in completed_sessions
    """
    init_session()
    return session_id in st.session_state.completed_sessions

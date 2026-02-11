"""Chatbot component for Maguru - AI Q&A assistant."""

import streamlit as st
from utils.session_manager import get_chat_history, add_chat_message
from utils.content_loader import load_session_content
from ai_chains import qa_chatbot, hint_generator


def show() -> None:
    """Display chatbot interface."""
    st.markdown("### 🤖 Asisten AI")

    # Chat container
    chat_container = st.container()

    with chat_container:
        # Display message history
        messages = get_chat_history()

        if not messages:
            st.info("💡 Tanyakan apa saja tentang materi yang sedang Anda pelajari!")
        else:
            for msg in messages:
                _render_message(msg['role'], msg['content'])

        # Auto-scroll to latest (using st.markdown with anchor)
        if messages:
            st.markdown("<div id='chat-end'></div>", unsafe_allow_html=True)

    # Input area
    st.markdown("---")

    # Question input
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])

        with col1:
            user_input = st.text_input(
                "Pertanyaan Anda",
                placeholder="Ketik pertanyaan...",
                label_visibility="collapsed"
            )

        with col2:
            submitted = st.form_submit_button("Kirim 📤", use_container_width=True)

        if submitted and user_input.strip():
            _handle_user_message(user_input.strip())

    # Hint button
    _render_hint_button()


def _render_message(role: str, content: str) -> None:
    """Render a single message with role-based styling.

    Args:
        role: Message role ('student' or 'ai')
        content: Message content
    """
    if role == "student":
        st.markdown(f"""
        <div style='background-color: #E3F2FD; padding: 10px; border-radius: 10px; margin: 5px 0;'>
        <strong>👤 Anda:</strong> {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background-color: #E8F5E9; padding: 10px; border-radius: 10px; margin: 5px 0;'>
        <strong>🤖 AI:</strong> {content}
        </div>
        """, unsafe_allow_html=True)


def _handle_user_message(question: str) -> None:
    """Process user input and get AI response.

    Args:
        question: User's question
    """
    # Add student message
    add_chat_message("student", question)

    # Get session context
    course_id = st.session_state.get('current_course', '')
    module_id = st.session_state.get('current_module', '')
    session_id = st.session_state.get('current_session', '')

    content = load_session_content(course_id, module_id, session_id) or ""
    chat_history = get_chat_history()

    # Get AI response
    try:
        response = qa_chatbot.answer_question(
            question,
            f"Session {session_id}",
            content,
            chat_history
        )

        # Add AI response
        add_chat_message("ai", response)

        # Rerun to show messages
        st.rerun()

    except Exception as e:
        error_msg = f"Maaf, terjadi kesalahan: {str(e)}"
        add_chat_message("ai", error_msg)
        st.rerun()


def _render_hint_button() -> None:
    """Render 3-level hint button."""
    st.markdown("---")

    with st.expander("💡 Dapatkan Hint", expanded=False):
        st.markdown("Klik untuk mendapatkan bantuan bertahap:")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Hint 1", key="hint1", use_container_width=True):
                _get_hint(1)

        with col2:
            if st.button("Hint 2", key="hint2", use_container_width=True):
                _get_hint(2)

        with col3:
            if st.button("Hint 3", key="hint3", use_container_width=True):
                _get_hint(3)


def _get_hint(level: int) -> None:
    """Get hint at specified level.

    Args:
        level: Hint level (1-3)
    """
    course_id = st.session_state.get('current_course', '')
    module_id = st.session_state.get('current_module', '')
    session_id = st.session_state.get('current_session', '')

    content = load_session_content(course_id, module_id, session_id) or ""

    try:
        hint = hint_generator.generate_hint(
            level,
            content,
            f"Session {session_id}"
        )

        st.info(f"💡 **Hint Level {level}:**\n\n{hint}")

        # Also add to chat history
        add_chat_message("ai", f"Hint Level {level}: {hint}")
        st.rerun()

    except Exception as e:
        st.error(f"Gagal mendapatkan hint: {str(e)}")

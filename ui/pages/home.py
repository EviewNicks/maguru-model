"""Home page for Maguru - Course selection."""

import streamlit as st
from utils.session_manager import (
    init_session, get_current_session,
    update_progress, add_chat_message, get_chat_history
)
from utils.content_loader import load_course_metadata
from ai_chains import ai_greeting
import os


def show() -> None:
    """Display home page with course list."""
    init_session()

    st.title("🐍 Maguru - Belajar Coding dengan AI")
    st.markdown("---")

    # Student name input (if not set)
    if not st.session_state.student_name:
        with st.form("student_form"):
            st.subheader("Selamat Datang! 👋")
            st.markdown("Silakan masukkan nama Anda untuk memulai belajar.")
            name = st.text_input("Nama Anda", placeholder="Masukkan nama...")
            submitted = st.form_submit_button("Mulai Belajar")

            if submitted and name.strip():
                st.session_state.student_name = name.strip()
                st.rerun()
            elif submitted:
                st.warning("Nama tidak boleh kosong!")
        return

    # Greeting message
    st.markdown(f"### Halo, {st.session_state.student_name}! 👋")
    st.markdown("Pilih kursus untuk memulai:")

    # Display courses
    _render_course_list()


def _render_course_list() -> None:
    """Load and display all available courses."""
    courses_dir = "data/courses"

    # Get all course directories
    if not os.path.exists(courses_dir):
        st.warning("Belum ada kursus tersedia.")
        return

    course_dirs = [
        d for d in os.listdir(courses_dir)
        if os.path.isdir(os.path.join(courses_dir, d))
    ]

    if not course_dirs:
        st.warning("Belum ada kursus tersedia.")
        return

    # Display courses in a grid
    cols = st.columns(min(len(course_dirs), 3))

    for idx, course_id in enumerate(course_dirs):
        col = cols[idx % len(cols)]
        with col:
            _render_course_card(course_id)


def _render_course_card(course_id: str) -> None:
    """Display a single course card.

    Args:
        course_id: Course identifier
    """
    metadata = load_course_metadata(course_id)

    if metadata is None:
        st.error(f"Kursus '{course_id}' tidak dapat dimuat.")
        return

    # Card container
    with st.container():
        # Title
        st.markdown(f"### {metadata.get('title', course_id)}")

        # Description
        description = metadata.get('description', '')
        if description:
            st.caption(description)

        # Metadata row
        col1, col2 = st.columns(2)
        with col1:
            difficulty = metadata.get('difficulty', 'unknown')
            difficulty_emoji = {
                'beginner': '🟢',
                'intermediate': '🟡',
                'advanced': '🔴'
            }.get(difficulty, '⚪')
            st.markdown(f"{difficulty_emoji} {difficulty.title()}")

        with col2:
            duration = metadata.get('duration_hours', 0)
            if duration:
                st.markdown(f"⏱️ {duration} jam")

        # Start button
        if st.button(
            f"Mulai Belajar - {metadata.get('title', course_id)}",
            key=f"start_{course_id}",
            type="primary",
            use_container_width=True
        ):
            _handle_course_selection(course_id, metadata)


def _handle_course_selection(course_id: str, metadata: dict) -> None:
    """Store course selection and show AI greeting.

    Args:
        course_id: Selected course ID
        metadata: Course metadata dict
    """
    # Store selection
    st.session_state.current_course = course_id

    # Get first module and session
    modules = metadata.get('modules', [])
    if modules:
        st.session_state.current_module = modules[0]

    # Trigger AI greeting
    try:
        greeting = ai_greeting.generate_greeting(
            st.session_state.student_name,
            metadata
        )
        st.success(greeting)
    except Exception as e:
        st.info(f"Selamat datang di {metadata.get('title', course_id)}!")

    # Add greeting to chat history
    add_chat_message("ai", f"Selamat datang di {metadata.get('title', course_id)}!")

    st.rerun()

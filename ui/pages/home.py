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

    # Check if course was just selected (show greeting message)
    if st.session_state.get("course_selected", False):
        greeting_msg = st.session_state.get("ai_greeting_message", "")
        if greeting_msg:
            st.success(greeting_msg)
            # Add greeting to chat history too
            init_session()
            add_chat_message("ai", greeting_msg)
        # Reset flag
        st.session_state.course_selected = None

    # Student name input (if not set)
    if not st.session_state.student_name:
        _render_student_form()
        return

    # If a course is selected, show course overview
    if st.session_state.get("current_course"):
        _render_course_overview()
        return

    # Show course list for selection
    st.markdown(f"### Halo, {st.session_state.student_name}! 👋")
    st.markdown("Pilih kursus untuk memulai:")

    _render_course_list()


def _render_student_form() -> None:
    """Render student name input form."""
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


def _render_course_overview() -> None:
    """Display course overview after selection."""
    course_id = st.session_state.current_course

    # Load course metadata
    metadata = load_course_metadata(course_id)

    if metadata is None:
        st.error(f"Kursus '{course_id}' tidak dapat dimuat.")
        return

    # Overview container with background
    st.markdown("""
    <style>
    .course-overview {
        background-color: #F8F9FA;
        border: 2px solid #E1E5A7;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .overview-title {
        color: #FF6B6B;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .overview-description {
        color: #333;
        margin-bottom: 15px;
    }
    .module-list {
        background-color: #FFF;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Overview content
    with st.container():
        st.markdown(f"### {metadata.get('title', course_id)}")
        st.markdown(f"**Overview:**")
        description = metadata.get('description', '')
        if description:
            st.markdown(description)

        # Display modules
        modules = metadata.get('modules', [])
        if modules:
            st.markdown("**Modul Pembelajaran:**")

            for module_id in modules:
                module_path = f"data/courses/{course_id}/modules/{module_id}/module.yaml"
                try:
                    import yaml
                    with open(module_path, 'r', encoding='utf-8') as f:
                        module_data = yaml.safe_load(f)
                    module_title = module_data.get('title', module_id)
                    st.markdown(f"- 📂 {module_title}")

                    # Show sessions
                    sessions = module_data.get('sessions', [])
                    for session_id in sessions:
                        st.markdown(f"  - 📄 {session_id.replace('_', ' ').title()}")

                except Exception:
                    pass

        # Learning objectives
        objectives = metadata.get('learning_objectives', [])
        if objectives:
            st.markdown("**Tujuan Pembelajaran:**")
            for obj in objectives:
                st.markdown(f"- {obj}")

        # Enter session button
        st.markdown("---")

        if st.button(
            "🚀 Masuk ke Sesi Pertama",
            key="enter_first_session",
            type="primary",
            use_container_width=True,
            help="Klik untuk memulai sesi pertama"
        ):
            st.session_state.current_page = "Learn"
            # Initialize first session
            modules = metadata.get('modules', [])
            if modules:
                st.session_state.current_module = modules[0]
                st.session_state.current_session = "session_1_1"

            st.rerun()


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
            f"Pilih - {metadata.get('title', course_id)}",
            key=f"select_{course_id}",
            type="primary",
            use_container_width=True
        ):
            _handle_course_selection(course_id, metadata)


def _handle_course_selection(course_id: str, metadata: dict) -> None:
    """Handle course selection - show greeting message, not navigate immediately.

    Args:
        course_id: Selected course ID
        metadata: Course metadata dict
    """
    # Store selection
    st.session_state.current_course = course_id
    st.session_state.course_selected = True  # Set flag for overview display

    # Get first module and session
    modules = metadata.get('modules', [])
    if modules:
        st.session_state.current_module = modules[0]

    # Trigger AI greeting and store in session
    try:
        greeting = ai_greeting.generate_greeting(
            st.session_state.student_name,
            metadata
        )
        st.session_state.ai_greeting_message = greeting
        st.success(greeting)
    except Exception as e:
        greeting = f"Selamat datang di {metadata.get('title', course_id)}!"
        st.session_state.ai_greeting_message = greeting
        st.info(greeting)

    # Add greeting to chat history
    init_session()
    add_chat_message("ai", st.session_state.ai_greeting_message)

    # Trigger rerun to show course overview
    st.rerun()

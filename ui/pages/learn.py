"""Learn page for Maguru - Content display with chatbot."""

import streamlit as st
from utils.session_manager import (
    init_session, get_current_session, update_progress,
    is_session_completed, add_chat_message, get_chat_history
)
from utils.content_loader import (
    load_course_metadata, load_module_list,
    load_session_content, get_next_session
)
from ai_chains import qa_chatbot


def show() -> None:
    """Display learn page with session content and chatbot."""
    init_session()

    # Check if course is selected
    if not st.session_state.current_course:
        st.warning("Silakan pilih kursus terlebih dahulu di halaman Home.")
        if st.button("Ke Halaman Home", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()
        return

    # Page header
    st.title(f"📚 Belajar: {_get_course_title()}")

    # Initialize current session if needed
    if not st.session_state.current_session:
        _initialize_first_session()

    # Layout: Content (left) + Chatbot (right)
    col1, col2 = st.columns([2, 1])

    with col1:
        _render_session_content()

    with col2:
        from ui.components.chatbot import show as show_chatbot
        show_chatbot()

    # Home button at bottom (less prominent exit)
    st.markdown("---")
    if st.button("🏠 Kembali ke Halaman Utama", use_container_width=True):
        st.session_state.current_page = "Home"
        st.rerun()


def _get_course_title() -> str:
    """Get current course title.

    Returns:
        Course title or fallback string
    """
    metadata = load_course_metadata(st.session_state.current_course)
    if metadata:
        return metadata.get('title', st.session_state.current_course)
    return st.session_state.current_course


def _initialize_first_session() -> None:
    """Set first session of first module as current session."""
    modules = load_module_list(st.session_state.current_course)
    if modules:
        st.session_state.current_module = modules[0]
        st.session_state.current_session = "session_1_1"  # Default first session


def _render_session_content() -> None:
    """Display current session content with progress and navigation."""
    course_id = st.session_state.current_course
    module_id = st.session_state.current_module
    session_id = st.session_state.current_session

    # Progress bar
    _render_progress_bar()

    st.markdown("---")

    # Load and display content
    content = load_session_content(course_id, module_id, session_id)

    if content is None:
        st.error(f"Konten untuk {session_id} tidak ditemukan.")
        return

    # Session header
    st.markdown(f"### 📖 Sesi: {session_id.replace('_', ' ').title()}")

    # Render markdown content
    st.markdown(content)

    # Navigation buttons
    st.markdown("---")
    _render_navigation()


def _render_progress_bar() -> None:
    """Display completion progress for current module."""
    course_id = st.session_state.current_course
    module_id = st.session_state.current_module

    metadata = load_course_metadata(course_id)
    if not metadata:
        return

    modules = metadata.get('modules', [])
    if module_id not in modules:
        return

    module_path = f"data/courses/{course_id}/modules/{module_id}/module.yaml"
    import yaml
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            module_data = yaml.safe_load(f)
            sessions = module_data.get('sessions', [])

        # Count completed sessions in this module
        completed = sum(
            1 for s in sessions
            if is_session_completed(f"{course_id}/{module_id}/{s}")
        )

        total = len(sessions)
        progress_pct = (completed / total * 100) if total > 0 else 0

        st.markdown(f"**Progress Module {module_id}:**")
        st.progress(progress_pct / 100)
        st.caption(f"{completed}/{total} sesi selesai")

    except Exception:
        pass


def _render_navigation() -> None:
    """Display navigation buttons for session control."""
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅️ Sebelumnya", use_container_width=True):
            _navigate_previous()

    with col2:
        # Mark complete button
        session_key = f"{st.session_state.current_course}/{st.session_state.current_module}/{st.session_state.current_session}"
        is_completed = is_session_completed(session_key)

        if is_completed:
            st.success("✅ Sesi Selesai")
        else:
            if st.button("✅ Tandai Selesai", use_container_width=True):
                update_progress(
                    st.session_state.current_course,
                    st.session_state.current_module,
                    st.session_state.current_session
                )
                st.rerun()

    with col3:
        if st.button("Selanjutnya ➡️", use_container_width=True):
            _navigate_next()


def _navigate_previous() -> None:
    """Navigate to previous session."""
    # Simple implementation - go to module quiz
    st.info("Navigasi sebelumnya akan diimplementasikan segera.")


def _navigate_next() -> None:
    """Navigate to next session or quiz."""
    next_session = get_next_session(
        st.session_state.current_course,
        st.session_state.current_module,
        st.session_state.current_session
    )

    if next_session:
        st.session_state.current_session = next_session
        st.rerun()
    else:
        st.info("Sesi ini adalah sesi terakhir. Silakan coba Kuis!")
        if st.button("Ke Kuis", use_container_width=True):
            st.session_state.current_page = "Quiz"
            st.rerun()

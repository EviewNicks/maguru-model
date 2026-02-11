"""Progress page for Maguru - Track learning progress."""

import streamlit as st
from utils.session_manager import (
    init_session, is_session_completed, get_chat_history
)
from utils.content_loader import (
    load_course_metadata, load_module_list,
    load_session_content
)
from datetime import datetime
import yaml


def show() -> None:
    """Display progress page."""
    init_session()

    st.title("📊 Progres Belajar")

    # Check if course is selected
    if not st.session_state.current_course:
        st.warning("Silakan pilih kursus terlebih dahulu di halaman Home.")
        if st.button("Ke Halaman Home", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()
        return

    # Overall progress
    _render_overall_progress()

    st.markdown("---")

    # Module progress
    _render_module_progress()

    st.markdown("---")

    # Quiz history
    _render_quiz_history()

    st.markdown("---")

    # Recommendations
    _render_recommendations()


def _render_overall_progress() -> None:
    """Display course completion percentage."""
    course_id = st.session_state.current_course
    metadata = load_course_metadata(course_id)

    if not metadata:
        return

    modules = metadata.get('modules', [])

    # Count total sessions and completed sessions
    total_sessions = 0
    completed_sessions = 0

    for module_id in modules:
        module_path = f"data/courses/{course_id}/modules/{module_id}/module.yaml"
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                module_data = yaml.safe_load(f)
                sessions = module_data.get('sessions', [])

                total_sessions += len(sessions)

                for session_id in sessions:
                    session_key = f"{course_id}/{module_id}/{session_id}"
                    if is_session_completed(session_key):
                        completed_sessions += 1
        except Exception:
            continue

    # Calculate progress
    progress_pct = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0

    st.markdown(f"### 🎯 Progres Keseluruhan")

    col1, col2 = st.columns(2)

    with col1:
        st.progress(progress_pct / 100)
        st.markdown(f"**{progress_pct:.1f}% Selesai**")

    with col2:
        st.metric(
            "Sesi Selesai",
            f"{completed_sessions}/{total_sessions}"
        )


def _render_module_progress() -> None:
    """Display module-by-module status."""
    st.markdown("### 📚 Progres per Modul")

    course_id = st.session_state.current_course
    metadata = load_course_metadata(course_id)

    if not metadata:
        return

    modules = metadata.get('modules', [])

    for module_id in modules:
        # Load module data
        module_path = f"data/courses/{course_id}/modules/{module_id}/module.yaml"
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                module_data = yaml.safe_load(f)

            module_title = module_data.get('title', module_id)
            sessions = module_data.get('sessions', [])

            # Count completed sessions
            completed = 0
            for session_id in sessions:
                session_key = f"{course_id}/{module_id}/{session_id}"
                if is_session_completed(session_key):
                    completed += 1

            # Display
            total = len(sessions)
            status_icon = "✅" if completed == total else "🔄"

            with st.expander(f"{status_icon} {module_title} ({completed}/{total} sesi)"):
                for session_id in sessions:
                    session_key = f"{course_id}/{module_id}/{session_id}"
                    is_done = is_session_completed(session_key)
                    icon = "✓" if is_done else "○"
                    st.markdown(f"{icon} {session_id.replace('_', ' ').title()}")

        except Exception as e:
            st.error(f"Gagal memuat modul {module_id}: {str(e)}")


def _render_quiz_history() -> None:
    """Display past quiz scores with timestamps."""
    st.markdown("### 📝 Riwayat Kuis")

    quiz_scores = st.session_state.get('quiz_scores', {})

    if not quiz_scores:
        st.info("Belum ada riwayat kuis.")
        return

    # Create table data
    table_data = []

    for quiz_id, result in quiz_scores.items():
        # Parse quiz_id (format: course_module)
        parts = quiz_id.replace('_', '/').split('/')
        name = quiz_id.replace(f'{st.session_state.current_course}_', '').replace('_', ' ').title()

        table_data.append({
            'Kuis': name,
            'Skor': f"{result['score']}/{result['total']}",
            'Hasil': 'Lulus ✅' if result['passed'] else 'Belum ❌',
            'Waktu': _format_timestamp(result['timestamp']),
            'Percobaan': result.get('attempt', 1)
        })

    # Display table
    if table_data:
        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )


def _render_recommendations() -> None:
    """Display next session to study."""
    st.markdown("### 💡 Rekomendasi")

    course_id = st.session_state.current_course
    modules = load_module_list(course_id)

    if not modules:
        return

    # Find next incomplete session
    next_session = None
    next_module = None

    for module_id in modules:
        module_path = f"data/courses/{course_id}/modules/{module_id}/module.yaml"
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                module_data = yaml.safe_load(f)
                sessions = module_data.get('sessions', [])

                for session_id in sessions:
                    session_key = f"{course_id}/{module_id}/{session_id}"
                    if not is_session_completed(session_key):
                        next_session = session_id
                        next_module = module_id
                        break

                if next_session:
                    break

        except Exception:
            continue

    if next_session:
        st.info(f"""
        📖 **Selanjutnya:** {next_session.replace('_', ' ').title()}

        Lanjutkan belajar di modul {next_module} untuk memperdalam pemahaman Anda.
        """)

        if st.button("Lanjut Belajar →", use_container_width=True):
            st.session_state.current_module = next_module
            st.session_state.current_session = next_session
            st.session_state.current_page = "Learn"
            st.rerun()
    else:
        st.success("🎉 Selamat! Anda telah menyelesaikan semua sesi di kursus ini.")


def _format_timestamp(timestamp: str) -> str:
    """Format ISO timestamp to readable format.

    Args:
        timestamp: ISO datetime string

    Returns:
        Formatted date/time string
    """
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return timestamp

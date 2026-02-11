"""Quiz page for Maguru - Assessment and feedback."""

import streamlit as st
from utils.session_manager import (
    init_session, save_quiz_score, get_chat_history
)
from utils.content_loader import load_quiz_definition, load_course_metadata
from utils.quiz_validator import (
    validate_answer, calculate_score,
    get_passed_status, identify_weak_areas
)
from ai_chains import quiz_feedback
from datetime import datetime
import yaml


# Session state keys for quiz
QUIZ_ANSWERS_KEY = "quiz_answers"
QUIZ_SUBMITTED_KEY = "quiz_submitted"
QUIZ_RESULTS_KEY = "quiz_results"


def show() -> None:
    """Display quiz page."""
    init_session()

    # Check if course is selected
    if not st.session_state.current_course:
        st.warning("Silakan pilih kursus terlebih dahulu di halaman Home.")
        if st.button("Ke Halaman Home", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()
        return

    st.title(f"📝 Kuis: {_get_module_title()}")

    # Load quiz definition
    course_id = st.session_state.current_course
    module_id = st.session_state.current_module

    quiz = load_quiz_definition(course_id, module_id, "")

    if quiz is None:
        st.error("Kuis tidak ditemukan untuk modul ini.")
        return

    # Check if quiz was already submitted
    if st.session_state.get(QUIZ_SUBMITTED_KEY, False):
        _render_results(quiz)
    else:
        _render_quiz_intro(quiz)
        _render_questions(quiz)
        _render_submit_button(quiz)


def _get_module_title() -> str:
    """Get current module title.

    Returns:
        Module title or fallback string
    """
    course_id = st.session_state.current_course
    module_id = st.session_state.current_module

    module_path = f"data/courses/{course_id}/modules/{module_id}/module.yaml"
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            module_data = yaml.safe_load(f)
            return module_data.get('title', module_id)
    except Exception:
        return module_id


def _render_quiz_intro(quiz: dict) -> None:
    """Display quiz introduction and instructions.

    Args:
        quiz: Quiz definition dict
    """
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🎯 Nilai Lulus", f"{quiz.get('passing_score', 70)}%")

    with col2:
        st.metric("⏱️ Waktu", f"{quiz.get('time_limit_minutes', 15)} menit")

    with col3:
        total_points = sum(q.get('points', 0) for q in quiz.get('questions', []))
        st.metric("📊 Total Poin", total_points)

    st.markdown("---")
    st.markdown("""
    ### 📋 Petunjuk:
    - Jawab semua pertanyaan dengan teliti
    - Untuk pilihan ganda, pilih satu jawaban yang benar
    - Untuk lengkapi kode, ketik jawaban yang tepat
    - Klik "Kirim Jawaban" setelah selesai
    """)


def _render_questions(quiz: dict) -> None:
    """Display all quiz questions.

    Args:
        quiz: Quiz definition dict
    """
    questions = quiz.get('questions', [])

    # Initialize answers storage if needed
    if QUIZ_ANSWERS_KEY not in st.session_state:
        st.session_state[QUIZ_ANSWERS_KEY] = {}

    for idx, question in enumerate(questions):
        question_id = question.get('id', f'q{idx}')

        st.markdown(f"### Soal {idx + 1}")

        # Question text
        st.markdown(question.get('question', ''))

        # Render based on type
        q_type = question.get('type', 'multiple_choice')

        if q_type == 'multiple_choice':
            _render_multiple_choice(question, question_id)
        elif q_type == 'code_completion':
            _render_code_completion(question, question_id)

        st.markdown("---")


def _render_multiple_choice(question: dict, question_id: str) -> None:
    """Render multiple choice question with radio buttons.

    Args:
        question: Question dict with options
        question_id: Question identifier
    """
    options = question.get('options', [])

    # Get current answer
    current_answers = st.session_state.get(QUIZ_ANSWERS_KEY, {})
    current = current_answers.get(question_id)

    # Render radio buttons
    answer = st.radio(
        "Pilih jawaban:",
        options=options,
        index=None,
        key=f"mc_{question_id}"
    )

    # Store selection
    if answer is not None:
        # Find index of selected option
        try:
            answer_index = options.index(answer)
            st.session_state[QUIZ_ANSWERS_KEY][question_id] = answer_index
        except ValueError:
            pass


def _render_code_completion(question: dict, question_id: str) -> None:
    """Render code completion question with text input.

    Args:
        question: Question dict with template
        question_id: Question identifier
    """
    template = question.get('template', '')
    current_answers = st.session_state.get(QUIZ_ANSWERS_KEY, {})

    # Show template
    st.code(template, language='python')

    # Get current answer
    current = current_answers.get(question_id, '')

    # Text input
    answer = st.text_input(
        "Isi bagian yang kosong:",
        value=current,
        key=f"cc_{question_id}",
        placeholder="Ketik jawaban..."
    )

    # Store answer
    if answer != current:
        st.session_state[QUIZ_ANSWERS_KEY][question_id] = answer


def _render_submit_button(quiz: dict) -> None:
    """Render submit button and handle answer submission.

    Args:
        quiz: Quiz definition dict
    """
    st.markdown("---")

    if st.button("📤 Kirim Jawaban", type="primary", use_container_width=True):
        _handle_answer_submission(quiz)


def _handle_answer_submission(quiz: dict) -> None:
    """Process and validate quiz answers.

    Args:
        quiz: Quiz definition dict
    """
    student_answers = st.session_state.get(QUIZ_ANSWERS_KEY, {})

    # Calculate score
    score = calculate_score(quiz, student_answers)
    total_points = sum(q.get('points', 0) for q in quiz.get('questions', []))

    # Check pass/fail
    passed = get_passed_status(score, total_points)

    # Identify incorrect answers for feedback
    incorrect = []
    for question in quiz.get('questions', []):
        q_id = question.get('id')
        if q_id in student_answers:
            if not validate_answer(question, student_answers[q_id]):
                incorrect.append(q_id)

    weak_areas = identify_weak_areas(quiz, incorrect)

    # Save results
    st.session_state[QUIZ_SUBMITTED_KEY] = True
    st.session_state[QUIZ_RESULTS_KEY] = {
        'score': score,
        'total': total_points,
        'passed': passed,
        'percentage': (score / total_points * 100) if total_points > 0 else 0,
        'incorrect': incorrect,
        'weak_areas': weak_areas
    }

    # Save to session manager
    quiz_id = f"{st.session_state.current_course}_{st.session_state.current_module}"
    save_quiz_score(quiz_id, score, total_points, passed)

    st.rerun()


def _render_results(quiz: dict) -> None:
    """Display quiz results with feedback and retry option.

    Args:
        quiz: Quiz definition dict
    """
    results = st.session_state.get(QUIZ_RESULTS_KEY, {})

    passed = results.get('passed', False)
    score = results.get('score', 0)
    total = results.get('total', 0)
    percentage = results.get('percentage', 0)

    st.markdown("---")

    # Score display
    if passed:
        st.success(f"🎉 Selamat! Anda LULUS!")
        st.balloons()
    else:
        st.error(f"😅 Nilai Anda belum mencapai kelulusan.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Skor", f"{score}/{total}")

    with col2:
        st.metric("Persentase", f"{percentage:.1f}%")

    with col3:
        status = "LULUS ✅" if passed else "BELUM LULUS ❌"
        st.metric("Status", status)

    st.markdown("---")

    # Detailed feedback per question
    st.markdown("### 📊 Detail Jawaban")

    questions = quiz.get('questions', [])
    student_answers = st.session_state.get(QUIZ_ANSWERS_KEY, {})

    for idx, question in enumerate(questions):
        q_id = question.get('id', f'q{idx}')
        is_correct = validate_answer(question, student_answers.get(q_id))

        if is_correct:
            st.markdown(f"✅ **Soal {idx + 1}:** Benar")
        else:
            st.markdown(f"❌ **Soal {idx + 1}:** Salah")
            explanation = question.get('explanation', '')
            if explanation:
                st.caption(f"💡 Penjelasan: {explanation}")

    # Weak areas
    weak_areas = results.get('weak_areas', [])
    if weak_areas and not passed:
        st.markdown("---")
        st.markdown("### 📚 Topik yang Perlu Ditinjau:")
        for area in weak_areas:
            st.markdown(f"- {area}")

    # Retry button
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Coba Lagi", use_container_width=True):
            st.session_state[QUIZ_SUBMITTED_KEY] = False
            st.session_state[QUIZ_ANSWERS_KEY] = {}
            st.rerun()

    with col2:
        if passed:
            if st.button("Lanjut ke Module Berikutnya ➡️", use_container_width=True):
                # Navigate to next module (implementation needed)
                st.info("Fitur navigasi module akan diimplementasikan segera.")

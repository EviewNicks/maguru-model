"""Quiz validator for Maguru MVP.

This module provides functions to validate quiz answers, calculate scores,
determine pass/fail status, and identify weak areas for review.
"""

from typing import Dict, List, Any, Optional


def validate_answer(question: Dict, student_answer: Any) -> bool:
    """Validate a student's answer against the correct answer.

    Args:
        question: Question dict with keys: type, correct (and options for multiple_choice)
        student_answer: Student's answer (int for multiple_choice, str for code_completion)

    Returns:
        True if answer is correct, False otherwise
    """
    if question is None or student_answer is None:
        return False

    question_type = question.get("type", "")

    if question_type == "multiple_choice":
        correct_index = question.get("correct")
        if correct_index is None or not isinstance(student_answer, int):
            return False
        return student_answer == correct_index

    elif question_type == "code_completion":
        correct_answer = question.get("answer")
        if correct_answer is None or not isinstance(student_answer, str):
            return False
        # Whitespace normalization + case-insensitive comparison
        normalized_student = " ".join(student_answer.split())
        normalized_correct = " ".join(correct_answer.split())
        return normalized_student.lower() == normalized_correct.lower()

    return False


def calculate_score(quiz_definition: Dict, student_answers: Dict[str, Any]) -> int:
    """Calculate total score from student answers.

    Args:
        quiz_definition: Quiz dict with questions list
        student_answers: Dict mapping question_id -> student_answer

    Returns:
        Total points earned (int)
    """
    if quiz_definition is None or student_answers is None:
        return 0

    questions = quiz_definition.get("questions", [])
    if not isinstance(questions, list):
        return 0

    total_score = 0

    for question in questions:
        question_id = question.get("id")
        if question_id is None:
            continue

        if question_id not in student_answers:
            continue

        if validate_answer(question, student_answers[question_id]):
            points = question.get("points", 0)
            if isinstance(points, int):
                total_score += points

    return total_score


def get_passed_status(score: int, total_points: int) -> bool:
    """Check if student passed the quiz (score >= 70%).

    Args:
        score: Points earned
        total_points: Total possible points

    Returns:
        True if score >= 70%, False otherwise
    """
    if total_points <= 0:
        return False

    percentage = (score / total_points) * 100
    return percentage >= 70


def identify_weak_areas(quiz_definition: Dict, incorrect_answers: List[str]) -> List[str]:
    """Identify weak areas based on incorrect answers.

    Args:
        quiz_definition: Quiz dict with questions list
        incorrect_answers: List of question IDs that were answered incorrectly

    Returns:
        List of topic names to review
    """
    if quiz_definition is None or not incorrect_answers:
        return []

    questions = quiz_definition.get("questions", [])
    if not isinstance(questions, list):
        return []

    questions_by_id = {q.get("id"): q for q in questions if q.get("id")}

    weak_areas = []

    for question_id in incorrect_answers:
        question = questions_by_id.get(question_id)
        if question is None:
            continue

        topic = question.get("topic")
        if topic and isinstance(topic, str) and topic not in weak_areas:
            weak_areas.append(topic)
        else:
            area = f"Question {question_id}"
            if area not in weak_areas:
                weak_areas.append(area)

    return weak_areas

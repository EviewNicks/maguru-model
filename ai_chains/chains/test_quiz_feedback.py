# -*- coding: utf-8 -*-
"""Test suite for quiz_feedback chain."""

import pytest
from ai_chains.chains.quiz_feedback import generate_feedback


class TestQuizFeedbackChain:
    """Test cases for quiz feedback chain."""

    def test_feedback_correct_answer_returns_string(self):
        """Test feedback for correct answer returns string."""
        result = generate_feedback(
            "Apa output 2+2?",
            "4",
            "4",
            True
        )
        assert isinstance(result, str)

    def test_feedback_incorrect_answer_returns_string(self):
        """Test feedback for incorrect answer returns string."""
        result = generate_feedback(
            "Apa output 2+2?",
            "5",
            "4",
            False
        )
        assert isinstance(result, str)

    def test_feedback_correct_not_empty(self):
        """Test feedback for correct answer is not empty."""
        result = generate_feedback("Test Q", "A", "A", True)
        assert len(result) > 0

    def test_feedback_incorrect_not_empty(self):
        """Test feedback for incorrect answer is not empty."""
        result = generate_feedback("Test Q", "Wrong", "Correct", False)
        assert len(result) > 0

    def test_feedback_contains_indonesian(self):
        """Test feedback contains Indonesian or fallback message."""
        result = generate_feedback("Apa itu variabel?", "wadah", "variabel", True)
        # Should have Indonesian words OR fallback message
        assert any(keyword in result.lower() for keyword in
                   ["benar", "salah", "bagus", "maaf", "error"])

    def test_feedback_math_question_correct(self):
        """Test feedback for math question with correct answer."""
        result = generate_feedback(
            "Berapa hasil 10 + 5?",
            "15",
            "15",
            True
        )
        assert isinstance(result, str)

    def test_feedback_math_question_incorrect(self):
        """Test feedback for math question with incorrect answer."""
        result = generate_feedback(
            "Berapa hasil 10 + 5?",
            "20",
            "15",
            False
        )
        assert isinstance(result, str)

    def test_feedback_code_question_correct(self):
        """Test feedback for code question with correct answer."""
        result = generate_feedback(
            "Bagaimana membuat variabel di Python?",
            "nama = 'value'",
            "nama = 'value'",
            True
        )
        assert isinstance(result, str)

    def test_feedback_multiple_choice_correct(self):
        """Test feedback for multiple choice correct answer."""
        result = generate_feedback(
            "Pilih jawaban yang benar",
            "B",
            "B",
            True
        )
        assert isinstance(result, str)

    def test_feedback_multiple_choice_incorrect(self):
        """Test feedback for multiple choice incorrect answer."""
        result = generate_feedback(
            "Pilih jawaban yang benar",
            "A",
            "C",
            False
        )
        assert isinstance(result, str)

    def test_feedback_with_long_question(self):
        """Test feedback with long question text."""
        long_q = "Apa" * 50 + "?"
        result = generate_feedback(long_q, "Answer", "Correct", True)
        assert isinstance(result, str)

    def test_feedback_with_special_characters(self):
        """Test feedback with special characters in question."""
        result = generate_feedback(
            "Apa output dari print(f'Halo {nama}')?",
            "Halo Budi",
            "Halo Budi",
            True
        )
        assert isinstance(result, str)

    @pytest.mark.parametrize("question,student,correct,is_correct", [
        ("2+2=?", "4", "4", True),
        ("2+2=?", "5", "4", False),
        ("Capital of Indonesia?", "Jakarta", "Jakarta", True),
        ("Capital of Indonesia?", "Bandung", "Jakarta", False),
    ])
    def test_feedback_various_scenarios(self, question, student, correct, is_correct):
        """Test feedback with various question scenarios."""
        result = generate_feedback(question, student, correct, is_correct)
        assert isinstance(result, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

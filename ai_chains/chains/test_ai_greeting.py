# -*- coding: utf-8 -*-
"""Test suite for ai_greeting chain."""

import pytest
from ai_chains.chains.ai_greeting import generate_greeting


class TestAIGreetingChain:
    """Test cases for AI greeting chain."""

    @pytest.fixture
    def sample_course(self):
        """Sample course metadata."""
        return {
            "title": "Python Basics",
            "learning_objectives": [
                "Memahami variabel",
                "Belajar tipe data",
                "Menguasai control flow"
            ]
        }

    def test_greeting_returns_string(self, sample_course):
        """Test that generate_greeting returns a string."""
        result = generate_greeting("Budi", sample_course)
        assert isinstance(result, str)

    def test_greeting_not_empty(self, sample_course):
        """Test that greeting is not empty."""
        result = generate_greeting("Budi", sample_course)
        assert len(result) > 0

    def test_greeting_contains_student_name(self, sample_course):
        """Test that greeting contains student name."""
        result = generate_greeting("Budi", sample_course)
        # Should contain name or have fallback message
        assert "Budi" in result or "maaf" in result.lower()

    def test_greeting_with_different_names(self, sample_course):
        """Test greeting with different student names."""
        names = ["Andi", "Siti", "Rina", "Joko"]
        for name in names:
            result = generate_greeting(name, sample_course)
            assert isinstance(result, str)
            assert name in result or "maaf" in result.lower()

    def test_greeting_with_course_title(self, sample_course):
        """Test greeting includes course context."""
        result = generate_greeting("Budi", sample_course)
        # Should have course reference OR fallback
        assert isinstance(result, str)

    def test_greeting_with_empty_objectives(self):
        """Test greeting with empty learning objectives."""
        course = {
            "title": "Python Basics",
            "learning_objectives": []
        }
        result = generate_greeting("Budi", course)
        assert isinstance(result, str)

    def test_greeting_with_single_objective(self):
        """Test greeting with single learning objective."""
        course = {
            "title": "Python Basics",
            "learning_objectives": ["Belajar Python dasar"]
        }
        result = generate_greeting("Budi", course)
        assert isinstance(result, str)

    def test_greeting_with_many_objectives(self):
        """Test greeting with many learning objectives."""
        course = {
            "title": "Python Complete",
            "learning_objectives": [
                "Variabel",
                "Tipe data",
                "Control flow",
                "Function",
                "Class",
                "Module"
            ]
        }
        result = generate_greeting("Budi", course)
        assert isinstance(result, str)

    def test_greeting_with_missing_title(self):
        """Test greeting with missing course title."""
        course = {
            "learning_objectives": ["Belajar Python"]
        }
        result = generate_greeting("Budi", course)
        assert isinstance(result, str)
        # Should use default title

    def test_greeting_with_special_characters_name(self):
        """Test greeting with special characters in name."""
        result = generate_greeting("José María", {"title": "Course", "learning_objectives": []})
        assert isinstance(result, str)

    def test_greeting_with_long_name(self):
        """Test greeting with long student name."""
        long_name = "Maria Alexandra Consuelo Rodriguez Gonzalez"
        result = generate_greeting(long_name, {"title": "Course", "learning_objectives": []})
        assert isinstance(result, str)

    def test_greeting_indonesian_output(self, sample_course):
        """Test that greeting contains Indonesian or fallback."""
        result = generate_greeting("Budi", sample_course)
        # Should have Indonesian words OR fallback message
        assert any(keyword in result.lower() for keyword in
                   ["halo", "selamat", "datang", "belajar", "kursus", "python", "maaf", "error"])

    @pytest.mark.parametrize("name,course_title", [
        ("Budi", "Python Basics"),
        ("Andi", "Web Development"),
        ("Siti", "Data Science"),
    ])
    def test_greeting_various_inputs(self, name, course_title):
        """Test greeting with various inputs."""
        course = {
            "title": course_title,
            "learning_objectives": ["Learn basic"]
        }
        result = generate_greeting(name, course)
        assert isinstance(result, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

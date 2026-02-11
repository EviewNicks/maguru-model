# -*- coding: utf-8 -*-
"""Test suite for qa_chatbot chain."""

import pytest
from ai_chains.chains.qa_chatbot import answer_question


class TestQAChatbotChain:
    """Test cases for Q&A chatbot chain."""

    def test_answer_question_returns_string(self):
        """Test that answer_question returns a string."""
        result = answer_question(
            "Apa itu variabel?",
            "Pengenalan Variabel",
            "Variabel adalah wadah untuk menyimpan data.",
            []
        )
        assert isinstance(result, str)

    def test_answer_question_not_empty(self):
        """Test that answer_question returns non-empty output."""
        result = answer_question(
            "Apa itu variabel?",
            "Pengenalan Variabel",
            "Variabel adalah wadah untuk menyimpan data.",
            []
        )
        assert len(result) > 0

    def test_answer_with_session_title(self):
        """Test answering with session title context."""
        result = answer_question(
            "Apa itu variabel?",
            "Session 1: Variabel Python",
            "Variabel adalah wadah data.",
            []
        )
        assert isinstance(result, str)

    def test_answer_with_session_content(self):
        """Test answering with session content context."""
        content = "Variabel menyimpan data seperti teks, angka, dan boolean."
        result = answer_question(
            "Contoh variabel?",
            "Variabel",
            content,
            []
        )
        assert isinstance(result, str)

    def test_answer_with_chat_history(self):
        """Test answering with chat history context."""
        history = [
            {"role": "student", "content": "Apa itu variabel?"},
            {"role": "ai", "content": "Variabel adalah wadah data."}
        ]
        result = answer_question(
            "Bisa beri contoh?",
            "Variabel",
            "Variabel adalah wadah data.",
            history
        )
        assert isinstance(result, str)

    def test_answer_with_long_chat_history(self):
        """Test answering with long chat history (more than 5 messages)."""
        history = [
            {"role": "student", "content": f"Pertanyaan {i}"} for i in range(10)
        ]
        result = answer_question(
            "Pertanyaan terakhir?",
            "Session",
            "Content here.",
            history
        )
        assert isinstance(result, str)

    def test_answer_with_empty_history(self):
        """Test answering with empty chat history."""
        result = answer_question(
            "Apa itu variabel?",
            "Session",
            "Content here.",
            []
        )
        assert isinstance(result, str)

    def test_answer_with_none_history(self):
        """Test answering with None chat history."""
        result = answer_question(
            "Apa itu variabel?",
            "Session",
            "Content here.",
            None
        )
        assert isinstance(result, str)

    def test_answer_code_question(self):
        """Test answering code-related question."""
        result = answer_question(
            "Bagaimana membuat variabel?",
            "Variabel Python",
            "nama = 'value' membuat variabel.",
            []
        )
        assert isinstance(result, str)

    def test_answer_concept_question(self):
        """Test answering concept question."""
        result = answer_question(
            "Apa perbedaan int dan float?",
            "Tipe Data",
            "Int untuk bilangan bulat, float untuk desimal.",
            []
        )
        assert isinstance(result, str)

    def test_answer_with_indonesian_query(self):
        """Test answering Indonesian language query."""
        result = answer_question(
            "Jelaskan tentang variabel",
            "Variabel",
            "Variabel menyimpan data.",
            []
        )
        assert isinstance(result, str)

    def test_answer_with_empty_session_content(self):
        """Test answering with empty session content."""
        result = answer_question(
            "Apa itu variabel?",
            "Session",
            "",
            []
        )
        assert isinstance(result, str)

    @pytest.mark.parametrize("question,session_title", [
        ("Apa itu variabel?", "Variabel"),
        ("Bagaimana print?", "Input Output"),
        ("Apa itu string?", "Tipe Data"),
    ])
    def test_answer_various_questions(self, question, session_title):
        """Test answering various types of questions."""
        result = answer_question(
            question,
            session_title,
            "Session content here.",
            []
        )
        assert isinstance(result, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# -*- coding: utf-8 -*-
"""Unit tests with mocks for automated quiz generator chain."""

import sys
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, '.')

from app.chains.quiz_generator import generate_quiz_questions, _extract_json_array, _sanitize_input
from app.schemas.quiz import GenerateQuizRequestSchema, GenerateQuizResponseSchema

def test_sanitize_input():
    """Test input sanitization and truncation."""
    raw = "Hello\x00 World!\x1f" + "a" * 5000
    cleaned = _sanitize_input(raw, max_len=100)
    assert "\x00" not in cleaned
    assert len(cleaned) == 100

def test_extract_json_array_valid():
    """Test parsing clean JSON array string."""
    raw = '[{"question": "Q1", "options": {"a":"1","b":"2","c":"3","d":"4"}, "correct":"a", "topic":"T1", "difficulty":"easy"}]'
    res = _extract_json_array(raw)
    assert len(res) == 1
    assert res[0]["question"] == "Q1"

def test_extract_json_array_markdown_wrapped():
    """Test parsing markdown wrapped JSON."""
    raw = '```json\n[{"question": "Q2", "options": {"a":"1","b":"2","c":"3","d":"4"}, "correct":"b", "topic":"T2", "difficulty":"medium"}]\n```'
    res = _extract_json_array(raw)
    assert len(res) == 1
    assert res[0]["question"] == "Q2"

@patch("app.chains.quiz_generator._get_chain")
def test_generate_quiz_questions_success(mock_get_chain):
    """Test quiz generation with mocked chain response."""
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = '[{"question": "Apa itu Python?", "options": {"a":"Bahasa","b":"Ular","c":"Mobil","d":"Game"}, "correct":"a", "topic":"Basics", "difficulty":"easy"}]'
    mock_get_chain.return_value = mock_chain

    questions = generate_quiz_questions(course_id="c123", lesson_content="Python dasar")
    assert len(questions) == 1
    assert questions[0]["correct"] == "a"
    assert questions[0]["question"] == "Apa itu Python?"

@patch("app.chains.quiz_generator._get_chain")
def test_generate_quiz_questions_fallback_on_error(mock_get_chain):
    """Test fallback quiz generation when LLM throws exception."""
    mock_chain = MagicMock()
    mock_chain.invoke.side_effect = Exception("LLM connection timeout")
    mock_get_chain.return_value = mock_chain

    questions = generate_quiz_questions(course_id="course-err", difficulty="hard")
    assert len(questions) == 1
    assert "course-err" in questions[0]["question"]
    assert questions[0]["difficulty"] == "hard"

if __name__ == "__main__":
    pytest.main(["-v", __file__])

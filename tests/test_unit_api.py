# -*- coding: utf-8 -*-
"""Unit tests for FastAPI endpoints using TestClient and mocks."""

import sys
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

sys.path.insert(0, '.')

from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test GET /health root endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data

def test_root_endpoint():
    """Test GET / root metadata endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "endpoints" in data

@patch("app.api.v1.endpoints.quiz.generate_quiz_questions")
def test_generate_quiz_endpoint(mock_gen):
    """Test POST /api/v1/generate-quiz endpoint."""
    mock_gen.return_value = [
        {
            "question": "Q Test",
            "options": {"a": "1", "b": "2", "c": "3", "d": "4"},
            "correct": "a",
            "topic": "Test Topic",
            "difficulty": "medium"
        }
    ]
    response = client.post(
        "/api/v1/generate-quiz",
        json={
            "course_id": "c123",
            "num_questions": 1,
            "difficulty": "medium"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["course_id"] == "c123"
    assert len(data["questions"]) == 1

@patch("app.api.v1.endpoints.ingest.ingest_text_content")
def test_ingest_text_endpoint(mock_ingest):
    """Test POST /api/v1/ingest endpoint."""
    mock_ingest.return_value = 3
    response = client.post(
        "/api/v1/ingest",
        json={
            "course_id": "c123",
            "content": "Materi teks lesson baru"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["chunks_processed"] == 3

if __name__ == "__main__":
    pytest.main(["-v", __file__])

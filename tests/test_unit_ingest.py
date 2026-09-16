# -*- coding: utf-8 -*-
"""Unit tests for Milestone 3 Auto-Ingestion & Knowledge Sync Endpoints."""

import sys
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

sys.path.insert(0, '.')

from app.main import app

client = TestClient(app)

@patch("app.api.v1.endpoints.ingest.ingest_text_content")
def test_ingest_single_lesson(mock_ingest):
    """Test POST /api/v1/ingest for single lesson with title and metadata."""
    mock_ingest.return_value = 2
    response = client.post(
        "/api/v1/ingest",
        json={
            "course_id": "course-python-101",
            "section_id": "sec-1",
            "lesson_id": "les-1",
            "title": "Pengenalan Variabel",
            "course_slug": "belajar-python",
            "content": "Variabel dalam Python tidak memerlukan deklarasi tipe secara eksplisit."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["chunks_processed"] == 2
    mock_ingest.assert_called_once_with(
        content="Variabel dalam Python tidak memerlukan deklarasi tipe secara eksplisit.",
        course_id="course-python-101",
        section_id="sec-1",
        lesson_id="les-1",
        title="Pengenalan Variabel",
        course_slug="belajar-python"
    )

@patch("app.api.v1.endpoints.ingest.bulk_ingest_course_lessons")
def test_bulk_ingest_lessons(mock_bulk):
    """Test POST /api/v1/ingest/bulk for full course synchronization."""
    mock_bulk.return_value = {"total_lessons": 3, "total_chunks": 8}
    payload = {
        "course_id": "course-python-101",
        "course_slug": "belajar-python",
        "lessons": [
            {"lesson_id": "l1", "section_id": "s1", "title": "Bab 1", "content": "Konten Bab 1"},
            {"lesson_id": "l2", "section_id": "s1", "title": "Bab 2", "content": "Konten Bab 2"},
            {"lesson_id": "l3", "section_id": "s2", "title": "Bab 3", "content": "Konten Bab 3"}
        ]
    }
    response = client.post("/api/v1/ingest/bulk", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["total_lessons"] == 3
    assert data["total_chunks"] == 8

@patch("app.api.v1.endpoints.ingest.delete_lesson_chunks")
def test_delete_lesson_chunks(mock_delete):
    """Test DELETE /api/v1/ingest for lesson cascade deletion."""
    mock_delete.return_value = True
    response = client.request(
        "DELETE",
        "/api/v1/ingest",
        json={"course_id": "course-python-101", "lesson_id": "les-1"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["lesson_id"] == "les-1"
    mock_delete.assert_called_once_with(course_id="course-python-101", lesson_id="les-1")

@patch("app.api.v1.endpoints.ingest.get_course_knowledge_status")
def test_get_knowledge_status(mock_status):
    """Test GET /api/v1/ingest/status for knowledge indicator badge."""
    mock_status.return_value = {
        "status": "success",
        "course_id": "course-python-101",
        "total_chunks": 12,
        "is_synced": True,
        "last_synced_at": None,
        "message": "12 knowledge chunks indexed"
    }
    response = client.get("/api/v1/ingest/status?course_id=course-python-101")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["total_chunks"] == 12
    assert data["is_synced"] is True

if __name__ == "__main__":
    pytest.main(["-v", __file__])

"""
API Test Suite for StudyMate AI
Validates FastAPI endpoints and core models.
"""

from fastapi.testclient import TestClient
from backend.main import app, SUPPORTED_LANGUAGES, create_fallback_quiz

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert data["version"] == "2.0.0"
    assert "AI Chat" in data["features"]


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["documents"] == 0
    assert data["languages"] == len(SUPPORTED_LANGUAGES)
    assert len(SUPPORTED_LANGUAGES) == 15


def test_documents_list_empty():
    response = client.get("/api/documents")
    assert response.status_code == 200
    assert response.json() == {"documents": []}


def test_document_delete_not_found():
    response = client.delete("/api/documents/nonexistent.pdf")
    assert response.status_code == 404


def test_quiz_fallback_generation():
    questions = create_fallback_quiz(num=3, context="Machine Learning is a subset of AI.", difficulty="easy")
    assert len(questions) == 3
    for q in questions:
        assert "question" in q
        assert "options" in q
        assert "correct" in q
        assert "explanation" in q


def test_export_chat():
    messages = [
        {"role": "user", "content": "What is RAG?"},
        {"role": "assistant", "content": "Retrieval-Augmented Generation."}
    ]
    response = client.post("/api/export-chat", json=messages)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "chat_history"
    assert data["total_messages"] == 2


def test_export_quiz():
    payload = {
        "timestamp": 1234567890,
        "quiz": [],
        "answers": {},
        "score": 4,
        "total": 5,
        "difficulty": "medium",
        "language": "English"
    }
    response = client.post("/api/export-quiz", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["percentage"] == 80.0
    assert data["score"] == 4

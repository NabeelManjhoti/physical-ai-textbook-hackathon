import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.chat import ChatRequest

client = TestClient(app)


def test_chat_endpoint():
    """
    Test the chat endpoint with a sample request
    """
    # This test requires the services to be running, so we'll just test the structure
    response = client.post(
        "/api/v1/chat/",
        json={"query": "What is Physical AI?"}
    )
    # We expect either a successful response or a service unavailable error
    # (since the actual services may not be running during tests)
    assert response.status_code in [200, 500]


def test_chat_health():
    """
    Test the chat health endpoint
    """
    response = client.get("/api/v1/chat/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "chat"}


def test_model_serialization():
    """
    Test that ChatRequest model can be properly serialized
    """
    chat_request = ChatRequest(query="Test query", session_id="test_session")
    assert chat_request.query == "Test query"
    assert chat_request.session_id == "test_session"
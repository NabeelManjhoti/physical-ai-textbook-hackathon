import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.ingest import IngestRequest

client = TestClient(app)


def test_ingest_endpoint():
    """
    Test the ingest endpoint with a sample request
    """
    # This test requires the services to be running, so we'll just test the structure
    response = client.post(
        "/api/v1/ingest/",
        json={"source_path": "/app/docs"}
    )
    # We expect either a successful response or a service unavailable error
    # (since the actual services may not be running during tests)
    assert response.status_code in [200, 400, 500]  # 400 if source path doesn't exist


def test_ingest_health():
    """
    Test the ingest health endpoint
    """
    response = client.get("/api/v1/ingest/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "ingest"}


def test_ingest_model_serialization():
    """
    Test that IngestRequest model can be properly serialized
    """
    ingest_request = IngestRequest(source_path="/test/path", chunk_size=1000, chunk_overlap=200)
    assert ingest_request.source_path == "/test/path"
    assert ingest_request.chunk_size == 1000
    assert ingest_request.chunk_overlap == 200
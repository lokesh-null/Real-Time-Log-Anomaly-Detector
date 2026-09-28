import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "log-anomaly-backend"
    assert "websocket_clients" in data

def test_websocket_manager():
    with client.websocket_connect("/ws") as websocket:
        # Check if the connection is registered
        response = client.get("/health")
        assert response.json()["websocket_clients"] == 1
    
    # Check if the connection is dropped
    response = client.get("/health")
    assert response.json()["websocket_clients"] == 0

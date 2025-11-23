from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint returns HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Weather Watcher" in response.text

def test_health_check():
    """Test health endpoint returns correct status"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0"

def test_api_info():
    """Test info endpoint returns project details"""
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "Weather Watcher"

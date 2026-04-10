from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_simulate():
    response = client.get("/simulate")
    assert response.status_code == 200
    data = response.json()
    assert "player_hp" in data
    assert "enemy_hp" in data

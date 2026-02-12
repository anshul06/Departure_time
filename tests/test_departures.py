from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_departures_endpoint():
    response = client.get("/departures?lat=51.5&lon=-0.1")
    assert response.status_code == 200
    assert "stations" in response.json()

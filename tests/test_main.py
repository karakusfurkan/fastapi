from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_basic_chat():
    response = client.post("/chat", json={"message": "Merhaba"})
    assert response.status_code == 200
    assert "Merhaba" in response.json()["reply"]

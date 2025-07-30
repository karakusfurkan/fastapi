import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def test_message():
    return {"message": "Test mesajı"}

def test_save_message(test_message):
    response = client.post("/chat/save", json=test_message)
    assert response.status_code == 200
    assert "inserted_id" in response.json()

def test_list_messages():
    response = client.get("/chat/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

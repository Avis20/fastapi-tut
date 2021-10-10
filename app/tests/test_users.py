from app.main import app
from fastapi.testclient import TestClient


def test_create(test_db):
    request_data = {
        "email": "test@test.com",
        "name": "test",
        "password": "test"
    }
    with TestClient(app) as client:
        response = client.post("/user/create", json=request_data)
        assert response.status_code == 200

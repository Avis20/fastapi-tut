import asyncio
import pytest

from fastapi.testclient import TestClient

from app.schemas.users import UserCreate
from app.utils.users import create_user
from app.main import app

request_data = {
    "email": "test@test.com",
    "username": "test@test.com",
    "name": "test",
    "password": "test",
}


def test_create(test_db):
    with TestClient(app) as client:
        response = client.post("/user/create", json=request_data)
        data = response.json()
        assert response.status_code == 200
        assert data.get("user_id") == 1
        assert data.get("email") == request_data.get("email")
        assert data.get("name") == request_data.get("name")
        assert data.get("password") == request_data.get("password")
        assert data.get("token").get("access_token") is not None
        assert data.get("token").get("ts_expires") is not None


def test_login(test_db):
    with TestClient(app) as client:
        response = client.post("/user/login", data=request_data)
        data = response.json()
        assert response.status_code == 200
        assert data.get("access_token") is not None
        assert data.get("ts_expires") is not None


def test_login_with_wrong_email(test_db):
    request_wrong_data = {"username": "1test@test.com", "password": "test"}
    with TestClient(app) as client:
        response = client.post("/user/login", data=request_wrong_data)
        data = response.json()
        assert response.status_code == 400


def test_user_info(test_db):
    with TestClient(app) as client:
        response = client.post("/user/login", data=request_data).json()
        response = client.get(
            "/user/info",
            headers={"Authorization": f"Bearer {response.get('access_token')}"},
        )
        data = response.json()
        assert response.status_code == 200
        assert data.get("user_id") == 1
        assert data.get("email") == request_data.get("email")
        assert data.get("name") == request_data.get("name")


def test_user_info_forbidden(test_db):
    with TestClient(app) as client:
        response = client.get("/user/info")
        assert response.status_code == 401


@pytest.mark.freeze_time("2015-01-01")
def test_expire_token(test_db, freezer):
    user = UserCreate(
        email="test2@mail.com",
        name="test2",
        password="test2",
    )
    with TestClient(app) as client:
        loop = asyncio.get_event_loop()
        user_db = loop.run_until_complete(create_user(user))
        freezer.move_to("'2000-01-01'")
        print("\n\n")
        print(user_db)
        print("\n\n")
        response = client.get(
            "/user/info",
            headers={"Authorization": f"Bearer {user_db.get('token').get('token')}"},
        )
        assert response.status_code == 401

import pytest
from fastapi.testclient import TestClient

from app_05_cookies_and_headers import app


@pytest.fixture
def client():
    return TestClient(app)              # a new client has an empty cookie jar


def test_cookie_parameter(client):
    response = client.get("/me", headers={"Cookie": "session_id=abc"})
    assert response.json() == {"session_id": "abc"}


def test_cookie_absent(client):
    assert client.get("/me").json() == {"session_id": None}


def test_set_cookie_flags(client):
    response = client.get("/set-cookie")
    header = response.headers["set-cookie"].lower()
    assert response.cookies["session_id"] == "abc123"
    assert "httponly" in header
    assert "samesite=lax" in header
    assert "max-age=3600" in header


def test_cookie_round_trip(client):
    client.get("/set-cookie")
    assert client.get("/me").json() == {"session_id": "abc123"}     # the client sent it back by itself


def test_delete_cookie(client):
    response = client.get("/delete-cookie")
    assert "max-age=0" in response.headers["set-cookie"].lower()


def test_header_underscore_conversion(client):
    response = client.get("/token", headers={"X-Token": "t1"})
    assert response.json() == {"x_token": "t1"}


def test_required_header_missing(client):
    response = client.get("/token")
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["type"] == "missing"
    assert error["loc"][0] == "header"
    assert error["loc"][1] in ("x_token", "x-token")


def test_header_sent_twice_is_a_list(client):
    response = client.get("/tokens", headers=[("X-Token", "a"), ("X-Token", "b")])
    assert response.json() == {"x_token": ["a", "b"]}


def test_response_header(client):
    response = client.get("/custom-header")
    assert response.headers["x-process-time"] == "0.01"
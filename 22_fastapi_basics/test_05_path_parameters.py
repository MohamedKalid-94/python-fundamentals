import pytest
from fastapi.testclient import TestClient

from app_05_path_parameters import app

client = TestClient(app)


def test_fixed_path_before_variable():
    assert client.get("/users/me").json() == {"user": "the current user"}


def test_int_path_parameter():
    assert client.get("/users/5").json() == {"user_id": 5}


def test_invalid_int_is_422():
    for bad in ("abc", "1.5"):
        assert client.get(f"/users/{bad}").status_code == 422
    error = client.get("/users/abc").json()["detail"][0]
    assert error["type"] == "int_parsing"
    assert error["loc"] == ["path", "user_id"]


def test_path_with_slashes():
    response = client.get("/files/home/ann/notes.txt")
    assert response.json() == {"file_path": "home/ann/notes.txt"}


@pytest.mark.parametrize("kind, unit", [("temperature", "C"), ("humidity", "%")])
def test_enum_values(kind, unit):
    assert client.get(f"/sensors/{kind}").json() == {"kind": kind, "unit": unit}


def test_enum_invalid_value():
    response = client.get("/sensors/light")
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "enum"
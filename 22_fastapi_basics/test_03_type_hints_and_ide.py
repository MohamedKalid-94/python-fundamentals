from typing import get_type_hints

from fastapi.testclient import TestClient

from app_03_type_hints_and_ide import app, double

client = TestClient(app)


def test_double():
    assert client.get("/double/21").json() == {"result": 42}


def test_double_not_a_number():
    response = client.get("/double/abc")
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["type"] == "int_parsing"
    assert error["loc"] == ["path", "number"]


def test_greet_default():
    assert client.get("/greet", params={"name": "Ann"}).json() == {"message": "Hello Ann"}


def test_greet_excited():
    response = client.get("/greet", params={"name": "Ann", "excited": "true"})
    assert response.json() == {"message": "Hello Ann!"}


def test_greet_missing_name():
    response = client.get("/greet")
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["type"] == "missing"
    assert error["loc"] == ["query", "name"]


def test_fastapi_reads_these_hints():
    assert get_type_hints(double) == {"number": int, "return": dict[str, int]}
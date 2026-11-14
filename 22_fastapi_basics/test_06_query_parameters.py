import pytest
from fastapi.testclient import TestClient

from app_06_query_parameters import app

client = TestClient(app)


def test_defaults():
    names = [item["name"] for item in client.get("/items").json()]
    assert names == ["pen", "ink", "cap", "ruler", "tape"]


def test_skip_and_limit():
    response = client.get("/items", params={"skip": 1, "limit": 2})
    assert response.json() == [{"name": "ink"}, {"name": "cap"}]


def test_invalid_limit():
    response = client.get("/items", params={"limit": "abc"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "limit"]


def test_required_query_missing():
    response = client.get("/search")
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["type"] == "missing"
    assert error["loc"] == ["query", "q"]


def test_search_substring():
    assert client.get("/search", params={"q": "p"}).json() == {
        "query": "p", "exact": False, "found": ["pen", "cap", "tape"],
    }


def test_search_exact():
    response = client.get("/search", params={"q": "pen", "exact": "true"})
    assert response.json() == {"query": "pen", "exact": True, "found": ["pen"]}


@pytest.mark.parametrize("text, expected", [
    ("true", True), ("1", True), ("yes", True), ("on", True),
    ("false", False), ("0", False), ("no", False), ("off", False),
])
def test_bool_conversion(text, expected):
    response = client.get("/search", params={"q": "pen", "exact": text})
    assert response.json()["exact"] is expected


def test_path_and_query_defaults():
    assert client.get("/users/7/orders").json() == {"user_id": 7, "status": None, "page": 1}


def test_path_and_query_values():
    response = client.get("/users/7/orders", params={"status": "open", "page": 2})
    assert response.json() == {"user_id": 7, "status": "open", "page": 2}
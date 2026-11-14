from fastapi.testclient import TestClient

from app_07_parameter_validation import app

client = TestClient(app)


def first_error(response):
    assert response.status_code == 422
    return response.json()["detail"][0]


def test_valid_request():
    assert client.get("/items/5").json() == {"item_id": 5, "q": None, "size": 10}


def test_path_too_small():
    error = first_error(client.get("/items/0"))
    assert error["type"] == "greater_than_equal"
    assert error["loc"] == ["path", "item_id"]
    assert "greater than or equal to 1" in error["msg"]


def test_path_too_large():
    assert first_error(client.get("/items/1001"))["type"] == "less_than_equal"


def test_query_too_short():
    error = first_error(client.get("/items/5", params={"q": "ab"}))
    assert error["type"] == "string_too_short"
    assert error["loc"] == ["query", "q"]


def test_query_too_long():
    error = first_error(client.get("/items/5", params={"q": "x" * 21}))
    assert error["type"] == "string_too_long"


def test_size_too_large():
    assert first_error(client.get("/items/5", params={"size": 101}))["type"] == "less_than_equal"


def test_pattern_matches():
    assert client.get("/codes", params={"code": "ABC-123"}).json() == {"code": "ABC-123"}


def test_pattern_does_not_match():
    error = first_error(client.get("/codes", params={"code": "abc-123"}))
    assert error["type"] == "string_pattern_mismatch"


def test_multiple_values():
    response = client.get("/multi", params=[("tag", "a"), ("tag", "b")])
    assert response.json() == {"tags": ["a", "b"]}


def test_multiple_values_absent():
    assert client.get("/multi").json() == {"tags": []}


def test_alias():
    assert client.get("/aliased", params={"item-query": "x"}).json() == {"item_query": "x"}
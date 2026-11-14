from fastapi.testclient import TestClient

from app_09_request_body import app

client = TestClient(app)


def test_create_item():
    response = client.post("/items", json={"name": "pen", "price": 10})
    assert response.status_code == 201
    assert response.json() == {
        "name": "pen", "price": 10.0, "tags": [], "description": None, "price_with_tax": 11.8,
    }


def test_price_must_be_positive():
    response = client.post("/items", json={"name": "pen", "price": 0})
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["type"] == "greater_than"
    assert error["loc"] == ["body", "price"]


def test_missing_field():
    response = client.post("/items", json={"price": 5})
    error = response.json()["detail"][0]
    assert error["type"] == "missing"
    assert error["loc"] == ["body", "name"]


def test_wrong_type():
    response = client.post("/items", json={"name": "pen", "price": "abc"})
    assert response.json()["detail"][0]["type"] == "float_parsing"


def test_invalid_json():
    response = client.post("/items", content="not json", headers={"Content-Type": "application/json"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "json_invalid"


def test_update_mixes_path_query_and_body():
    response = client.put("/items/5", params={"notify": "true"}, json={"name": "pen", "price": 10})
    assert response.json() == {
        "item_id": 5, "notify": True, "name": "pen", "price": 10.0, "tags": [], "description": None,
    }


def test_two_bodies():
    payload = {"item": {"name": "pen", "price": 1}, "user": {"username": "ann"}}
    assert client.post("/orders", json=payload).json() == {"item": "pen", "user": "ann"}


def test_extra_fields_are_ignored():
    response = client.post("/items", json={"name": "pen", "price": 1, "colour": "red"})
    assert response.status_code == 201
    assert "colour" not in response.json()


def test_single_body_value():
    assert client.post("/importance", json=3).json() == {"importance": 3}


def test_embedded_body_ok():
    assert client.post("/rating", json={"score": 4}).json() == {"score": 4}


def test_embedded_body_invalid():
    response = client.post("/rating", json={"score": 9})
    error = response.json()["detail"][0]
    assert response.status_code == 422
    assert error["type"] == "less_than_equal"
    assert error["loc"] == ["body", "score"]
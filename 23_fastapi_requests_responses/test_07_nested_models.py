from fastapi.testclient import TestClient

from app_07_nested_models import app

client = TestClient(app)


def test_nested_item_body():
    payload = {
        "name": "cam", "price": 9.5, "tags": ["a", "b"],
        "images": [{"url": "https://example.com/a.png", "name": "front"}],
    }
    assert client.post("/items", json=payload).json() == {
        "name": "cam", "tag_count": 2, "image_names": ["front"],
    }


def test_set_removes_duplicates():
    response = client.post("/items", json={"name": "x", "price": 1, "tags": ["a", "a", "b"]})
    assert response.json()["tag_count"] == 2


def test_invalid_url():
    payload = {"name": "x", "price": 1, "images": [{"url": "not a url", "name": "n"}]}
    response = client.post("/items", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "url_parsing"


def test_list_of_models():
    payload = {"name": "bundle", "items": [{"name": "a", "price": 1.5}, {"name": "b", "price": 2.5}]}
    assert client.post("/offers", json=payload).json() == {"name": "bundle", "total": 4.0, "items": 2}


def test_error_location_shows_the_exact_path():
    payload = {"name": "bundle", "items": [{"name": "a", "price": 1}, {"name": "b", "price": "x"}]}
    error = client.post("/offers", json=payload).json()["detail"][0]
    assert error["loc"] == ["body", "items", 1, "price"]
    assert error["type"] == "float_parsing"


def test_dict_with_int_keys():
    response = client.post("/weights", json={"1": 2.5, "2": 1.5})
    assert response.json() == {"total": 4.0, "keys": [1, 2]}


def test_dict_with_a_bad_key():
    assert client.post("/weights", json={"a": 1.0}).status_code == 422


def test_nested_response_model():
    assert client.get("/sample").json() == {
        "name": "sample",
        "items": [{"name": "x", "price": 2.0, "tags": ["t"], "images": None}],
    }
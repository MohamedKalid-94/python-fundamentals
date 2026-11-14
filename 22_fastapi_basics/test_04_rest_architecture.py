import pytest
from fastapi.testclient import TestClient

from app_04_rest_architecture import app, reset

client = TestClient(app)


@pytest.fixture(autouse=True)
def fresh_data():
    reset()                         # every test starts with the same two items


def test_list():
    assert client.get("/items").json() == [{"id": 1, "name": "pen"}, {"id": 2, "name": "ink"}]


def test_get_one():
    assert client.get("/items/2").json() == {"id": 2, "name": "ink"}


def test_get_missing_is_404():
    response = client.get("/items/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_returns_201():
    response = client.post("/items", params={"name": "cap"})
    assert response.status_code == 201
    assert response.json() == {"id": 3, "name": "cap"}
    assert client.get("/items/3").json() == {"id": 3, "name": "cap"}


def test_replace():
    response = client.put("/items/1", params={"name": "pencil"})
    assert response.status_code == 200
    assert client.get("/items/1").json()["name"] == "pencil"


def test_delete_returns_204():
    response = client.delete("/items/1")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/items/1").status_code == 404


def test_delete_missing_is_404():
    assert client.delete("/items/99").status_code == 404
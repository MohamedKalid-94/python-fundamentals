import pytest
from fastapi.testclient import TestClient

from app_01_crud import app, reset

client = TestClient(app)


@pytest.fixture(autouse=True)
def fresh_data():
    reset()


def make(name="temp", **extra):
    return client.post("/sensors", json={"name": name, **extra})


def names(response):
    return [sensor["name"] for sensor in response.json()]


def test_create_returns_201():
    response = make()
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "temp", "unit": "C", "location": None}


def test_duplicate_name_is_409():
    make()
    response = make()
    assert response.status_code == 409
    assert response.json() == {"detail": "A sensor with this name already exists"}


def test_create_validation():
    response = client.post("/sensors", json={"name": ""})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "string_too_short"


def test_list_filter_and_pagination():
    make("a", unit="C")
    make("b", unit="%")
    make("c", unit="C")
    assert names(client.get("/sensors")) == ["a", "b", "c"]
    assert names(client.get("/sensors", params={"unit": "C"})) == ["a", "c"]
    assert names(client.get("/sensors", params={"skip": 1, "limit": 1})) == ["b"]


def test_read_one_and_404():
    make()
    assert client.get("/sensors/1").json()["name"] == "temp"
    assert client.get("/sensors/99").status_code == 404


def test_put_replaces_everything():
    make(location="lab", unit="%")
    response = client.put("/sensors/1", json={"name": "temp2"})
    assert response.json() == {"id": 1, "name": "temp2", "unit": "C", "location": None}


def test_patch_changes_only_the_sent_fields():
    make(location="lab")
    response = client.patch("/sensors/1", json={"location": "roof"})
    assert response.json() == {"id": 1, "name": "temp", "unit": "C", "location": "roof"}


def test_patch_to_an_existing_name_is_409():
    make("a")
    make("b")
    assert client.patch("/sensors/2", json={"name": "a"}).status_code == 409


def test_delete_then_404():
    make()
    assert client.delete("/sensors/1").status_code == 204
    assert client.get("/sensors/1").status_code == 404


def test_changing_a_missing_sensor_is_404():
    assert client.put("/sensors/9", json={"name": "x"}).status_code == 404
    assert client.patch("/sensors/9", json={"unit": "F"}).status_code == 404
    assert client.delete("/sensors/9").status_code == 404
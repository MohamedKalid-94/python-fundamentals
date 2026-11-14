import pytest
from fastapi.testclient import TestClient

from app_03_mongodb import InMemoryNoteStore, app, get_store


@pytest.fixture
def client():
    store = InMemoryNoteStore()                             # a fresh fake database for every test
    app.dependency_overrides[get_store] = lambda: store
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_and_read(client):
    created = client.post("/notes", json={"title": "first", "body": "hello"})
    assert created.status_code == 201
    assert created.json() == {"id": "1", "title": "first", "body": "hello"}
    assert client.get("/notes/1").json() == created.json()


def test_unknown_id_is_404(client):
    response = client.get("/notes/nope")
    assert response.status_code == 404
    assert response.json() == {"detail": "Note not found"}


def test_list_with_limit(client):
    for index in range(3):
        client.post("/notes", json={"title": f"n{index}"})
    titles = [note["title"] for note in client.get("/notes", params={"limit": 2}).json()]
    assert titles == ["n0", "n1"]


def test_delete(client):
    client.post("/notes", json={"title": "x"})
    assert client.delete("/notes/1").status_code == 204
    assert client.get("/notes/1").status_code == 404
    assert client.delete("/notes/1").status_code == 404


def test_empty_title_is_422(client):
    response = client.post("/notes", json={"title": ""})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "string_too_short"
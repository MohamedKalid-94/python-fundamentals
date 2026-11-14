import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app_02_sql_database import Base, app, get_db, make_engine


@pytest.fixture
def client():
    engine = make_engine("sqlite://")                       # a new empty in-memory database per test
    Base.metadata.create_all(engine)
    test_session = sessionmaker(engine, expire_on_commit=False)

    def override_get_db():
        with test_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)                                   # no "with": the real lifespan is not run
    app.dependency_overrides.clear()
    engine.dispose()


def add(client, name, **extra):
    return client.post("/devices", json={"name": name, **extra})


def test_create_device(client):
    response = add(client, "gw-1")
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "gw-1", "firmware": "1.0.0", "online": False}


def test_duplicate_name_is_409(client):
    add(client, "gw-1")
    assert add(client, "gw-1").status_code == 409
    assert add(client, "gw-2").status_code == 201           # the session recovered after the rollback


def test_validation_error(client):
    assert client.post("/devices", json={"firmware": "2.0"}).status_code == 422


def test_read_and_404(client):
    add(client, "gw-1", firmware="2.1.0")
    assert client.get("/devices/1").json()["firmware"] == "2.1.0"
    assert client.get("/devices/99").status_code == 404


def test_list_filter_and_pagination(client):
    for name in ("a", "b", "c"):
        add(client, name)
    client.patch("/devices/1/online", json={"online": True})
    client.patch("/devices/3/online", json={"online": True})
    names = lambda response: [d["name"] for d in response.json()]
    assert names(client.get("/devices", params={"online": "true"})) == ["a", "c"]
    assert names(client.get("/devices", params={"online": "false"})) == ["b"]
    assert names(client.get("/devices", params={"skip": 1, "limit": 1})) == ["b"]


def test_set_online_is_stored(client):
    add(client, "gw-1")
    assert client.patch("/devices/1/online", json={"online": True}).json()["online"] is True
    assert client.get("/devices/1").json()["online"] is True


def test_delete(client):
    add(client, "gw-1")
    assert client.delete("/devices/1").status_code == 204
    assert client.get("/devices/1").status_code == 404
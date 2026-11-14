import pytest
from fastapi.testclient import TestClient

from app_06_response_model import app, reset

client = TestClient(app)


@pytest.fixture(autouse=True)
def fresh_data():
    reset()


def test_password_is_filtered_out():
    response = client.post("/users", json={"username": "ann", "password": "secret"})
    assert response.status_code == 201
    assert response.json() == {"username": "ann", "full_name": None, "id": 1}
    assert "password" not in response.text


def test_list_response_model():
    client.post("/users", json={"username": "ann", "password": "p1"})
    client.post("/users", json={"username": "bo", "password": "p2", "full_name": "Bo B"})
    assert client.get("/users").json() == [
        {"username": "ann", "full_name": None, "id": 1},
        {"username": "bo", "full_name": "Bo B", "id": 2},
    ]


def test_input_is_still_validated():
    response = client.post("/users", json={"username": "ann"})
    error = response.json()["detail"][0]
    assert response.status_code == 422
    assert error["type"] == "missing"
    assert error["loc"] == ["body", "password"]


def test_exclude_unset_leaves_out_defaults():
    assert client.get("/items/foo").json() == {"name": "Foo", "price": 50.2}


def test_exclude_unset_keeps_values_that_were_set():
    assert client.get("/items/bar").json() == {
        "name": "Bar", "description": "The bartenders", "price": 62.0, "tax": 20.2,
    }


def test_bad_output_is_a_500():
    safe_client = TestClient(app, raise_server_exceptions=False)
    assert safe_client.get("/broken").status_code == 500


def test_openapi_documents_the_output_model():
    schema = client.get("/openapi.json").json()
    reference = schema["paths"]["/users"]["post"]["responses"]["201"]["content"]["application/json"]["schema"]["$ref"]
    assert "UserOut" in reference
    user_out = next(v for k, v in schema["components"]["schemas"].items() if k.startswith("UserOut"))
    assert "password" not in user_out["properties"]
    assert "id" in user_out["properties"]
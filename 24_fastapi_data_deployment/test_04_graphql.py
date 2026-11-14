import pytest
from fastapi.testclient import TestClient

from app_04_graphql import SENSORS, app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_sensors():
    del SENSORS[2:]


def gql(query, variables=None):
    return client.post("/graphql", json={"query": query, "variables": variables}).json()


def test_hello():
    assert gql("{ hello }") == {"data": {"hello": "Hello from GraphQL"}}


def test_client_chooses_the_fields():
    assert gql("{ sensors { name unit } }") == {
        "data": {"sensors": [{"name": "temp", "unit": "C"}, {"name": "humidity", "unit": "%"}]},
    }


def test_variables_and_a_missing_item():
    query = "query($id: Int!) { sensor(id: $id) { name } }"
    assert gql(query, {"id": 2}) == {"data": {"sensor": {"name": "humidity"}}}
    assert gql(query, {"id": 99}) == {"data": {"sensor": None}}


def test_mutation():
    result = gql('mutation { addSensor(name: "pressure", unit: "hPa") { id name unit } }')
    assert result == {"data": {"addSensor": {"id": 3, "name": "pressure", "unit": "hPa"}}}
    assert len(SENSORS) == 3


def test_unknown_field_gives_errors():
    result = gql("{ doesNotExist }")
    assert "errors" in result


def test_rest_route_next_to_graphql():
    assert client.get("/health").json() == {"status": "ok"}
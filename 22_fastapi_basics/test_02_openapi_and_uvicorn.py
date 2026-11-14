from fastapi.testclient import TestClient

from app_02_openapi_and_uvicorn import app, private_app

client = TestClient(app)


def test_openapi_schema_describes_the_code():
    schema = client.get("/openapi.json").json()
    assert schema["openapi"].startswith("3.")
    assert schema["info"]["title"] == "Sensor API"
    assert schema["info"]["version"] == "1.0.0"
    operation = schema["paths"]["/sensors"]["get"]
    assert operation["summary"] == "List sensors"
    assert operation["tags"] == ["sensors"]
    assert operation["description"].startswith("Return all sensors")      # from the docstring


def test_docs_pages_exist():
    docs = client.get("/docs")
    assert docs.status_code == 200
    assert "text/html" in docs.headers["content-type"]
    assert client.get("/redoc").status_code == 200


def test_docs_can_be_switched_off():
    private = TestClient(private_app)
    assert private.get("/docs").status_code == 404
    assert private.get("/openapi.json").status_code == 404
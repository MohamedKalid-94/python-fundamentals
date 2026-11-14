from fastapi.testclient import TestClient

from app_09_mounting_flask import app

client = TestClient(app)


def test_flask_root():
    response = client.get("/flask/")
    assert response.status_code == 200
    assert response.text == "Hello from Flask"


def test_path_without_the_trailing_slash_is_redirected():
    response = client.get("/flask")
    assert response.status_code == 200
    assert response.text == "Hello from Flask"


def test_flask_route_with_a_parameter_and_escaping():
    assert client.get("/flask/hello/Ann").text == "Hello Ann from Flask"
    assert "&lt;b&gt;" in client.get("/flask/hello/<b>").text


def test_flask_query_parameters_and_json():
    response = client.get("/flask/add", params={"a": 2, "b": 3})
    assert response.json() == {"sum": 5}


def test_fastapi_routes_still_work_and_unknown_flask_routes_are_404():
    assert client.get("/fastapi").json() == {"framework": "fastapi"}
    assert client.get("/flask/nope").status_code == 404


def test_flask_routes_are_not_in_the_fastapi_documentation():
    paths = client.get("/openapi.json").json()["paths"]
    assert "/fastapi" in paths
    assert not any(path.startswith("/flask") for path in paths)
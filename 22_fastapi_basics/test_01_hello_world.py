from fastapi.testclient import TestClient

from app_01_hello_world import app

client = TestClient(app)        # calls the app directly: no server, no port


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
    assert response.headers["content-type"] == "application/json"


def test_unknown_path_is_404():
    response = client.get("/nothing")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_wrong_method_is_405():
    response = client.post("/")
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}
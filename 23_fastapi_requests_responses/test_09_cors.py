from fastapi.testclient import TestClient

from app_09_cors import app, dev_app

client = TestClient(app)
ALLOWED = "http://localhost:3000"


def preflight(origin=ALLOWED, method="POST", headers="Content-Type"):
    return client.options("/data", headers={
        "Origin": origin,
        "Access-Control-Request-Method": method,
        "Access-Control-Request-Headers": headers,
    })


def test_allowed_origin_gets_cors_headers():
    response = client.get("/data", headers={"Origin": ALLOWED})
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED
    assert response.headers["access-control-allow-credentials"] == "true"


def test_other_origin_still_gets_its_answer_but_no_cors_header():
    response = client.get("/data", headers={"Origin": "http://evil.example.com"})
    assert response.status_code == 200                              # the server answers; the BROWSER blocks it
    assert response.json() == {"value": 42}
    assert "access-control-allow-origin" not in response.headers


def test_request_without_origin_has_no_cors_headers():
    response = client.get("/data")
    assert "access-control-allow-origin" not in response.headers


def test_preflight_is_accepted():
    response = preflight()
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED
    assert "POST" in response.headers["access-control-allow-methods"]
    assert "DELETE" not in response.headers["access-control-allow-methods"]
    assert "Content-Type" in response.headers["access-control-allow-headers"]
    assert response.headers["access-control-max-age"] == "600"


def test_preflight_with_a_disallowed_method():
    assert preflight(method="DELETE").status_code == 400


def test_preflight_with_a_disallowed_header():
    assert preflight(headers="X-Custom").status_code == 400


def test_preflight_from_a_disallowed_origin():
    assert preflight(origin="http://evil.example.com").status_code == 400


def test_wildcard_app():
    dev_client = TestClient(dev_app)
    response = dev_client.get("/data", headers={"Origin": "http://anything.example"})
    assert response.headers["access-control-allow-origin"] == "*"
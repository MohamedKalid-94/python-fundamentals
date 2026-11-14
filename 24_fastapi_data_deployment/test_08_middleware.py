from fastapi.testclient import TestClient

from app_08_middleware import app

client = TestClient(app)


def test_process_time_header():
    response = client.get("/")
    assert float(response.headers["x-process-time"]) >= 0


def test_request_id_is_generated():
    response = client.get("/")
    request_id = response.headers["x-request-id"]
    assert len(request_id) == 32
    assert response.json() == {"request_id": request_id}        # the endpoint saw the same id


def test_request_id_from_the_client_is_kept():
    response = client.get("/", headers={"X-Request-ID": "abc-123"})
    assert response.headers["x-request-id"] == "abc-123"
    assert response.json() == {"request_id": "abc-123"}


def test_big_responses_are_gzipped():
    response = client.get("/big", headers={"Accept-Encoding": "gzip"})
    assert response.headers["content-encoding"] == "gzip"
    assert response.json() == {"data": "x" * 2000}              # the client library unpacked it


def test_small_responses_are_not_gzipped():
    assert "content-encoding" not in client.get("/").headers


def test_middleware_can_answer_by_itself():
    response = client.get("/blocked")
    assert response.status_code == 403
    assert response.json() == {"detail": "blocked by middleware"}


def test_untrusted_host_is_rejected():
    response = client.get("/", headers={"Host": "evil.example.com"})
    assert response.status_code == 400
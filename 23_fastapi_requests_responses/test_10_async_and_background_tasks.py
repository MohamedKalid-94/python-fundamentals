import pytest
from fastapi.testclient import TestClient

from app_10_async_and_background_tasks import app, log

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_log():
    log.clear()


def test_sync_and_async_endpoints_both_work():
    assert client.get("/sync").json() == {"mode": "sync"}
    assert client.get("/async").json() == {"mode": "async"}


def test_def_endpoint_runs_off_the_event_loop():
    assert client.get("/where-sync").json() == {"on_event_loop": False}


def test_async_def_endpoint_runs_on_the_event_loop():
    assert client.get("/where-async").json() == {"on_event_loop": True}


def test_gather():
    assert client.get("/gather").json() == {"results": [2, 4, 6]}


def test_blocking_call_moved_to_a_thread():
    assert client.get("/to-thread/41").json() == {"result": 42}


def test_background_tasks_run_after_the_response():
    response = client.post("/notify/ann")
    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}
    assert log == ["notified ann", "async notified ann"]
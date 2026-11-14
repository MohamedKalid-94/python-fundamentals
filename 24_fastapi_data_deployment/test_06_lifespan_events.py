import pytest
from fastapi.testclient import TestClient

from app_06_lifespan_events import app, events, failing_app, legacy_app


@pytest.fixture(autouse=True)
def clear_events():
    events.clear()


def test_lifespan_runs_inside_the_with_block():
    with TestClient(app) as client:
        assert events == ["startup"]
        assert client.get("/predict/hello").json() == {"model": "fake-model", "length": 5}
    assert events == ["startup", "shutdown"]


def test_without_the_with_block_there_is_no_start_up():
    client = TestClient(app)
    assert events == []
    with pytest.raises(AttributeError):                 # app.state.model was never created
        client.get("/predict/x")


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_the_older_event_handlers_still_work():
    with TestClient(legacy_app):
        assert events == ["legacy startup"]
    assert events == ["legacy startup", "legacy shutdown"]


def test_a_start_up_error_stops_the_application():
    with pytest.raises(RuntimeError, match="database not reachable"):
        with TestClient(failing_app):
            pass
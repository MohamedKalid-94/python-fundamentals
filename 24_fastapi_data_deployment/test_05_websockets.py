import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app_05_websockets import app, manager


def test_echo():
    client = TestClient(app)
    with client.websocket_connect("/ws/echo") as websocket:
        websocket.send_text("hello")
        assert websocket.receive_text() == "echo: hello"
        websocket.send_text("again")
        assert websocket.receive_text() == "echo: again"


def test_json_messages():
    client = TestClient(app)
    with client.websocket_connect("/ws/json") as websocket:
        websocket.send_json({"a": 2, "b": 3})
        assert websocket.receive_json() == {"sum": 5}


def test_chat_room_broadcast_and_cleanup():
    with TestClient(app) as client:                     # one shared event loop for both connections
        with client.websocket_connect("/ws/chat/ann") as ann:
            assert ann.receive_text() == "ann joined"
            with client.websocket_connect("/ws/chat/bo") as bo:
                assert bo.receive_text() == "bo joined"
                assert ann.receive_text() == "bo joined"
                bo.send_text("hi")
                assert ann.receive_text() == "bo: hi"
                assert bo.receive_text() == "bo: hi"
            assert ann.receive_text() == "bo left"
    assert manager.active == []


def test_connection_without_a_valid_token_is_refused():
    client = TestClient(app)
    with pytest.raises(WebSocketDisconnect) as info:
        with client.websocket_connect("/ws/secure?token=wrong"):
            pass
    assert info.value.code == 1008


def test_connection_with_a_valid_token_is_accepted():
    client = TestClient(app)
    with client.websocket_connect("/ws/secure?token=s3cret") as websocket:
        assert websocket.receive_text() == "welcome"
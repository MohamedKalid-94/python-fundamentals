import json

from fastapi.testclient import TestClient

from app_10_streaming import app, sse

client = TestClient(app)


def test_plain_text_stream():
    assert client.get("/stream/text").text == "Hello world, this is streamed"


def test_sse_lines():
    with client.stream("GET", "/stream/sse") as response:
        assert response.headers["content-type"].startswith("text/event-stream")
        lines = [line for line in response.iter_lines() if line]
    assert lines == [
        'data: {"token": "Hello"}',
        'data: {"token": " world"}',
        'data: {"token": ", this"}',
        'data: {"token": " is"}',
        'data: {"token": " streamed"}',
        "event: done",
        "data: [DONE]",
    ]


def test_sse_tokens_can_be_put_back_together():
    with client.stream("GET", "/stream/sse") as response:
        lines = [line for line in response.iter_lines() if line]
    tokens = [json.loads(line[len("data: "):])["token"] for line in lines if line.startswith("data: {")]
    assert "".join(tokens) == "Hello world, this is streamed"


def test_sse_headers_for_proxies_and_browsers():
    with client.stream("GET", "/stream/sse") as response:
        assert response.headers["cache-control"] == "no-cache"
        assert response.headers["x-accel-buffering"] == "no"


def test_sync_generator_stream():
    assert client.get("/stream/numbers", params={"count": 3}).text == "0\n1\n2\n"


def test_ndjson_stream():
    response = client.get("/stream/ndjson", params={"count": 2})
    assert [json.loads(line) for line in response.text.splitlines()] == [{"i": 0}, {"i": 1}]


def test_sse_helper_format():
    assert sse("x") == "data: x\n\n"
    assert sse("x", event="done") == "event: done\ndata: x\n\n"
import asyncio
import json
from collections.abc import AsyncIterator, Iterator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

# STREAMING: send the answer IN PIECES while it is still being produced.
# Essential for LLM chat: the user sees words appear instead of waiting for the whole answer.
#   StreamingResponse(generator, media_type=...)
#     async generator (async def with yield)   runs on the event loop: use await inside
#     sync generator (def with yield)          runs in the thread pool
#   The status code and headers are sent FIRST. After that you cannot change them: report a
#   mid-stream failure as a final message in the stream itself.
#
# SERVER-SENT EVENTS (SSE): a simple text format for one-way streams (server to browser).
#     data: first message\n\n          every message ends with a BLANK LINE
#     event: done\n data: [DONE]\n\n   an optional event name
#     : ping\n\n                       a comment line, used as a keep-alive
#   media_type="text/event-stream", and Cache-Control: no-cache.
#   Behind nginx add  X-Accel-Buffering: no  or the pieces are held back.
#   Browser: new EventSource("/stream/sse")  (GET only). For POST requests use fetch() and read response.body.
# NDJSON: one JSON object per line (application/x-ndjson): easy to parse piece by piece.
# WebSocket (lesson 05) is for two-way traffic; SSE is simpler when only the server talks.

app = FastAPI()

TOKENS = ["Hello", " world", ", this", " is", " streamed"]


async def fake_llm_tokens(delay: float = 0.0) -> AsyncIterator[str]:
    for token in TOKENS:
        await asyncio.sleep(delay)                      # a real model would take time here
        yield token


def sse(data: str, event: str | None = None) -> str:
    prefix = f"event: {event}\n" if event else ""
    return f"{prefix}data: {data}\n\n"


@app.get("/stream/text")
async def stream_text():
    return StreamingResponse(fake_llm_tokens(), media_type="text/plain")


@app.get("/stream/sse")
async def stream_sse():
    async def events():
        async for token in fake_llm_tokens():
            yield sse(json.dumps({"token": token}))
        yield sse("[DONE]", event="done")

    headers = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    return StreamingResponse(events(), media_type="text/event-stream", headers=headers)


@app.get("/stream/numbers")
def stream_numbers(count: int = 3):
    def generate() -> Iterator[str]:
        for index in range(count):
            yield f"{index}\n"

    return StreamingResponse(generate(), media_type="text/plain")


@app.get("/stream/ndjson")
def stream_ndjson(count: int = 2):
    def generate() -> Iterator[str]:
        for index in range(count):
            yield json.dumps({"i": index}) + "\n"

    return StreamingResponse(generate(), media_type="application/x-ndjson")
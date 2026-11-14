from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# A WEBSOCKET is a connection that STAYS OPEN: both sides can send messages at any time.
#   HTTP        the client asks, the server answers, the connection ends
#   WebSocket   one handshake (an HTTP upgrade), then messages flow both ways until someone closes it
# Use it for: chat, live sensor dashboards, collaborative editing, notifications.
# For one-way streams (an LLM answer token by token) Server-Sent Events are simpler (lesson 10).
#
#   @app.websocket("/ws")        the route; path and query parameters work as usual
#   await websocket.accept()     complete the handshake (or close() first to REFUSE the connection)
#   receive_text() / receive_json() / receive_bytes()      send_text() / send_json() / send_bytes()
#   WebSocketDisconnect          raised by receive_* when the client goes away: clean up in "except"
#   close codes: 1000 normal, 1008 policy violation (for example a bad token)
#
# SCALING WARNING: the ConnectionManager below lives in ONE process. With several workers or servers
# you need a shared channel (Redis pub/sub, a message broker) to reach every client.
# EMBEDDED ANALOGY: a persistent UART or TCP link where either side may talk at any time.

app = FastAPI()


@app.websocket("/ws/echo")
async def echo(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            text = await websocket.receive_text()
            await websocket.send_text(f"echo: {text}")
    except WebSocketDisconnect:
        pass


@app.websocket("/ws/json")
async def add_numbers(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            await websocket.send_json({"sum": data["a"] + data["b"]})
    except WebSocketDisconnect:
        pass


class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active:
            self.active.remove(websocket)

    async def broadcast(self, message: str):
        for connection in list(self.active):            # a copy: the list may change while we send
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/chat/{name}")
async def chat(websocket: WebSocket, name: str):
    await manager.connect(websocket)
    await manager.broadcast(f"{name} joined")
    try:
        while True:
            text = await websocket.receive_text()
            await manager.broadcast(f"{name}: {text}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{name} left")


@app.websocket("/ws/secure")
async def secure(websocket: WebSocket, token: str | None = None):
    if token != "s3cret":                               # simple demo check; use a real token in practice
        await websocket.close(code=1008)                # refuse BEFORE accept()
        return
    await websocket.accept()
    await websocket.send_text("welcome")
    await websocket.close()
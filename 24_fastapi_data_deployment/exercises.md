Write the questions as # comments and your solutions as code, with a test_*.py using TestClient for each.

Build a full CRUD API for /books (title, author, year) with Create, Update and Read models, PUT, PATCH, DELETE, paging, a filter by author and a duplicate check (409). Write at least 12 tests.
Add a /books/search?q= endpoint that matches the title ignoring case, and a sort Enum query parameter (title, year). Test the sorting in both directions.
Put the books API from exercise 1 on SQLite with SQLAlchemy. Add a year >= 1450 check and a unique constraint on title plus author. Test with an in-memory database and dependency_overrides.
Add a second table reviews (book id, rating 1 to 5, text) with a foreign key and a relationship. Add GET /books/{id}/reviews and POST /books/{id}/reviews. Test that deleting a book removes its reviews.
Rebuild exercise 1 for MongoDB behind the same store interface: write the InMemoryBookStore and a MongoBookStore, and test only the in-memory one. If you have Docker, run the Mongo version against a real server and describe in a comment what you had to change.
GraphQL: write a schema with Book and Author types, a query that returns books with their author nested, a mutation addBook, and a query with variables. Test that a client can ask for only the title.
WebSockets: build a live sensor feed. A client connects to /ws/sensors/{id}; the server sends a JSON reading every time POST /sensors/{id}/readings is called. Test with TestClient and a second connection that must not receive the first sensor’s readings.
Add a heartbeat to your WebSocket chat: the server sends {"type": "ping"} and closes connections that do not answer. Write the test with a fake clock or a very short interval. In a comment, explain why the connection list does not work with several Uvicorn workers.
Write an app with lifespan that opens a fake “database pool” (a class with connect() and close()), stores it in app.state, and records events. Test start-up, shutdown, and a failing start-up. Then rewrite it with on_event and list in a comment what is different.
Split a small project into routers: users, items and admin (protected by a router dependency), included under /api/v1. Add a mounted v2 sub-app with one changed route. Test that /docs lists only the v1 routes and that /v2/docs lists v2.
Write a middleware that logs method, path, status code and duration into a list, and another that adds X-Content-Type-Options: nosniff and X-Frame-Options: DENY to every response. Test both and write in a comment what changes if you swap their order.
Write a rate-limit middleware (5 requests per client address per window). Return 429 with a Retry-After header. Test the sixth request and the reset of the window with a fake clock. Why would a dependency be the better tool for a limit on one route only?
Mount a small Flask app (two routes) under /legacy. Then write the same two routes in FastAPI under /v2, and test that both versions return the same data. Write a short migration plan as comments.
Streaming: write POST /chat that takes a prompt and streams a fake answer word by word as SSE, then a final event: done with the word count. Test the full stream, and that a client who disconnects early does not cause an error. Add a keep-alive comment line every N tokens.
Security: extend lesson 11 with a scopes idea: users have a role (reader or admin), a dependency require_role("admin"), and a refresh token endpoint with a longer lifetime. Test each role, an expired access token and a valid refresh token. Write in a comment why a refresh token should be stored carefully.
Write a Settings class for a deployable service (database URL, JWT key as SecretStr, allowed origins as a list, docs flag). Build the app with a factory, wire CORS and TrustedHostMiddleware from the settings, and test two different configurations.
Embedded exercise: build a complete device-management service. Devices register with an API key, post readings (SQLite via SQLAlchemy), and a dashboard client subscribes over a WebSocket for live readings and over SSE for alerts. Add a JWT login for operators, /health and /ready, a Dockerfile and a compose file, and at least 25 tests. Write a one-page README.md for it.
Predict first, then run, and explain each result:
python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.testclient import TestClient

log = []

@asynccontextmanager
async def lifespan(app):
    log.append("start")
    yield
    log.append("stop")

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def first(request, call_next):
    log.append("first in")
    response = await call_next(request)
    log.append("first out")
    return response

@app.middleware("http")
async def second(request, call_next):
    log.append("second in")
    response = await call_next(request)
    log.append("second out")
    return response

@app.get("/")
def root():
    log.append("endpoint")
    return {}

client = TestClient(app)
client.get("/")
print(log)
with TestClient(app) as started:
    started.get("/")
print(log)
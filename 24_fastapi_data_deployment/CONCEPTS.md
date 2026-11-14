# Module 24: FastAPI Data, Realtime and Deployment, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | CRUD | Verbs | POST create (201), GET read (200/404), PUT replace, PATCH change part, DELETE (204) |
| 01 | CRUD | Models | Separate Create, Update (all optional) and Read (adds id) models |
| 01 | CRUD | Details | `model_dump(exclude_unset=True)` for PATCH; 404 missing, 409 duplicate; paging with `skip` and `limit` (max) |
| 02 | SQL | SQLAlchemy 2.0 | Engine (connections), model (`Mapped`, `mapped_column`), session (unit of work: commit, rollback) |
| 02 | SQL | FastAPI pattern | One session per request from a `yield` dependency; `from_attributes=True` reads ORM objects |
| 02 | SQL | Testing | Override `get_db` with an in-memory SQLite (`StaticPool`); never touch the real file |
| 02 | SQL | Tables | `create_all` for learning; Alembic migrations in real projects |
| 03 | MongoDB | Model | Database, collection, document; no fixed schema; `_id` is an ObjectId (send as text) |
| 03 | MongoDB | Driver | PyMongo async API: `AsyncMongoClient`, `await` network calls, `async for` over `find()` |
| 03 | MongoDB | Design | A store interface with a real and an in-memory implementation; tests swap it with `dependency_overrides` |
| 04 | GraphQL | Idea | One endpoint, typed schema, the client picks the fields; query, mutation, subscription |
| 04 | GraphQL | Strawberry | `@strawberry.type`, `@strawberry.field`, `@strawberry.mutation`, `GraphQLRouter`; snake_case becomes camelCase |
| 04 | GraphQL | Errors | Reported in an `errors` list, not by HTTP status |
| 05 | WebSockets | Concept | A connection that stays open; messages both ways; handshake then frames |
| 05 | WebSockets | API | `accept()`, `receive_text/json`, `send_text/json`, `WebSocketDisconnect`, `close(code=1008)` |
| 05 | WebSockets | Rooms | A `ConnectionManager` with `connect`, `disconnect`, `broadcast`; one process only, so use Redis pub/sub to scale |
| 06 | Events | `lifespan` | `@asynccontextmanager`: code before `yield` is start-up, after it is shutdown; the recommended way |
| 06 | Events | `on_event` | `startup` and `shutdown` decorators: older, deprecated, ignored when `lifespan` is set |
| 06 | Events | Use | Load a model, open a pool or client once; keep it on `app.state`; tests need `with TestClient(app)` |
| 07 | Routers | `APIRouter` | Prefix, tags, dependencies per router; `include_router`; one app, one `/docs` |
| 07 | Sub-apps | `mount` | An independent app under a path with its own `/docs`; not in the main documentation; for versions |
| 07 | Layout | Project | `routers/`, `schemas/`, `models/`, `services/`, `deps.py`, `config.py`, `main.py`, `tests/` |
| 08 | Middleware | Idea | Wraps every request and response; `@app.middleware("http")` with `call_next` |
| 08 | Middleware | Order | The one added last is outermost; it may answer without calling `call_next` |
| 08 | Middleware | Built in | `GZipMiddleware`, `TrustedHostMiddleware`, `CORSMiddleware`, `HTTPSRedirectMiddleware` |
| 08 | Middleware | Uses | Timing, request ids (`request.state`), security headers; prefer dependencies for per-route checks |
| 09 | Flask | Mounting | `app.mount("/flask", WSGIMiddleware(flask_app))` with `a2wsgi`; runs in a thread pool |
| 09 | Flask | Purpose | Gradual migration of an old Flask or Django app; not shown in `/docs`; not for new code |
| 10 | Streaming | `StreamingResponse` | Async or sync generator; headers and status go first; report late errors inside the stream |
| 10 | Streaming | SSE | `text/event-stream`; `data: ...` plus a blank line; `event:` names; `Cache-Control: no-cache` |
| 10 | Streaming | Choice | SSE for server-to-client streams (LLM tokens), WebSocket for two-way, NDJSON for line-by-line JSON |
| 11 | Security | Passwords | Store an Argon2 hash (`pwdlib`), never the password; verify with `verify` |
| 11 | Security | JWT | `jwt.encode` with `sub` and `exp`; `jwt.decode` checks signature and expiry; the payload is readable, not secret |
| 11 | Security | Flow | `/token` with form data returns a bearer token; `OAuth2PasswordBearer` and a `get_current_user` dependency |
| 11 | Security | Habits | Long random key from the environment, HTTPS, short lifetimes, 401 with `WWW-Authenticate: Bearer` |
| 12 | Deployment | Running | `fastapi run`, `uvicorn --workers N`; one process per container; reverse proxy for HTTPS |
| 12 | Deployment | Docker | Install requirements first (cache), non-root user, `HEALTHCHECK`, `CMD ["uvicorn", ...]` |
| 12 | Deployment | Operations | Settings from environment, secrets from the platform, `/health` (liveness), `/ready` (readiness), docs off |
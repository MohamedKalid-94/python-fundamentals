import secrets
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from pydantic_settings import BaseSettings

# DEPENDENCY INJECTION: you declare WHAT a function needs; FastAPI builds it and passes it in.
#   def endpoint(page: Annotated[dict, Depends(pagination)])
# Use it for: shared parameters, authentication, database sessions, settings, clients (an LLM or vector store).
#   - a dependency can have its own parameters (path, query, header, body ...): they are validated too
#   - a dependency can depend on other dependencies (sub-dependencies)
#   - the SAME dependency used twice in one request runs ONCE (use_cache=True is the default)
#   - a dependency with  yield  runs code AFTER the request: the place to close a database session
#   - a class works as a dependency: Annotated[Pager, Depends()]
#   - @app.get(..., dependencies=[Depends(check)]) runs a check without needing its value
#   - FastAPI(dependencies=[...]) applies one to every route
#   - app.dependency_overrides[original] = replacement   swaps a dependency IN TESTS (fake database, fake user)

app = FastAPI()

API_KEY = "secret-key"


# 1. A function dependency: shared pagination
def pagination(skip: int = 0, limit: Annotated[int, Query(le=100)] = 10):
    return {"skip": skip, "limit": limit}


Pagination = Annotated[dict, Depends(pagination)]       # an alias keeps the endpoints short


@app.get("/items")
def items(page: Pagination):
    data = list(range(1, 21))
    return data[page["skip"]: page["skip"] + page["limit"]]


# 2. A class dependency
class Pager:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit


@app.get("/pages")
def pages(pager: Annotated[Pager, Depends()]):
    return {"skip": pager.skip, "limit": pager.limit}


# 3. Sub-dependencies: profile -> get_current_user -> get_api_key
def get_api_key(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key is None or not secrets.compare_digest(x_api_key.encode(), API_KEY.encode()):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


def get_current_user(api_key: Annotated[str, Depends(get_api_key)]):
    return {"name": "ann"}


@app.get("/profile")
def profile(user: Annotated[dict, Depends(get_current_user)]):
    return user


# 4. A check that returns nothing useful: put it in the decorator
@app.get("/admin", dependencies=[Depends(get_api_key)])
def admin():
    return {"admin": True}


# 5. yield: setup before, cleanup after (runs even if the endpoint raised an error)
events: list[str] = []


class FakeDb:
    def query(self, n: int) -> int:
        return n * 2


def get_db():
    events.append("open")
    db = FakeDb()
    try:
        yield db
    finally:
        events.append("close")


@app.get("/db/{n}")
def read_db(n: int, db: Annotated[FakeDb, Depends(get_db)]):
    return {"result": db.query(n)}


# 6. Settings as a dependency, created ONCE (lru_cache), and replaceable in tests
class Settings(BaseSettings):
    app_name: str = "my-api"
    max_items: int = 100


@lru_cache
def get_settings():
    return Settings()


@app.get("/info")
def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {"app_name": settings.app_name, "max_items": settings.max_items}


# 7. Caching inside one request
calls = {"n": 0}


def counted():
    calls["n"] += 1
    return calls["n"]


@app.get("/cached")
def cached(a: Annotated[int, Depends(counted)], b: Annotated[int, Depends(counted)]):
    return {"a": a, "b": b, "calls": calls["n"]}


@app.get("/uncached")
def uncached(
    a: Annotated[int, Depends(counted, use_cache=False)],
    b: Annotated[int, Depends(counted, use_cache=False)],
):
    return {"a": a, "b": b, "calls": calls["n"]}
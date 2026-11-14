from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

# START-UP and SHUTDOWN code: do expensive work ONCE, not on every request.
# Typical for AI apps: load a model or an embedding index, open a database pool, create an HTTP client;
# close them cleanly at shutdown.
#
# TWO STYLES
#   lifespan (recommended)   one async context manager: code BEFORE yield = start-up, AFTER = shutdown.
#                            Resources can live in local variables and are cleaned up by the same function.
#   on_event("startup") / on_event("shutdown")   the older decorators (in your syllabus): still work,
#                            but are deprecated. You will meet them in old code and tutorials.
# You cannot use both in the same app: when lifespan is given, on_event handlers are ignored.
#
# Keep shared objects on app.state; endpoints reach them through request.app.state.
# In tests, the lifespan runs ONLY when TestClient is used as a context manager: with TestClient(app) as client:
# If start-up raises an error, the application does not start.

events: list[str] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    events.append("startup")
    app.state.model = {"name": "fake-model", "loaded": True}        # pretend: an expensive object
    yield                                                           # the application runs here
    events.append("shutdown")
    del app.state.model


app = FastAPI(lifespan=lifespan)


@app.get("/predict/{text}")
def predict(text: str, request: Request):
    model = request.app.state.model
    return {"model": model["name"], "length": len(text)}


# The older style
legacy_app = FastAPI()


@legacy_app.on_event("startup")
async def legacy_startup():
    events.append("legacy startup")


@legacy_app.on_event("shutdown")
def legacy_shutdown():
    events.append("legacy shutdown")


# A start-up error stops the application
@asynccontextmanager
async def failing_lifespan(app: FastAPI):
    raise RuntimeError("database not reachable")
    yield


failing_app = FastAPI(lifespan=failing_lifespan)
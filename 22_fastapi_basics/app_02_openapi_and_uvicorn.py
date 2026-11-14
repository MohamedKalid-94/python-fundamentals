from fastapi import FastAPI

# OPENAPI is the standard (formerly "Swagger") for describing an HTTP API in a JSON file.
# FastAPI builds that file FROM YOUR CODE, so the docs can never be out of date.
#   /openapi.json    the machine-readable description
#   /docs            Swagger UI: read the API AND try it in the browser
#   /redoc           ReDoc: a cleaner read-only view
# Tools use openapi.json to generate client code (TypeScript, Java ...) and tests.
# Your Next.js front end can generate a typed client from it.

app = FastAPI(
    title="Sensor API",
    description="Demo API for the course",
    version="1.0.0",
)


@app.get("/sensors", tags=["sensors"], summary="List sensors")
def list_sensors():
    """Return all sensors. This docstring becomes the description in /docs."""
    return [{"id": 1, "name": "temp"}]


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


# An app with the documentation switched off (a common choice in production)
private_app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


# UVICORN is the ASGI SERVER: it listens on a port and calls your app.
#   WSGI (Flask, Django)   one request at a time per worker, synchronous
#   ASGI (FastAPI)         async, WebSockets, many connections in one event loop
#
#   uvicorn app_02_openapi_and_uvicorn:app                       module:variable, then defaults
#   uvicorn app_02_openapi_and_uvicorn:app --reload              restart when a file changes (development only)
#   uvicorn app_02_openapi_and_uvicorn:app --host 0.0.0.0 --port 9000     reachable from the network
#   uvicorn app_02_openapi_and_uvicorn:app --workers 4           4 processes (cannot be combined with --reload)
#   uvicorn ... --log-level debug
#   python -m uvicorn ...                                        the same, using the interpreter of your venv
#   fastapi dev file.py     development: reload on, 127.0.0.1
#   fastapi run file.py     production style: no reload, listens on all interfaces
#
# EMBEDDED ANALOGY: the server is the super-loop. It waits for events (connections) and calls
# your handlers; a handler that blocks freezes every other client, as in a bare-metal main loop.

if __name__ == "__main__":      # lets you start it with:  python app_02_openapi_and_uvicorn.py
    import uvicorn

    uvicorn.run("app_02_openapi_and_uvicorn:app", host="127.0.0.1", port=8000, reload=True)
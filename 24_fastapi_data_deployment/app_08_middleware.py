import time
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

# MIDDLEWARE is code that wraps EVERY request and response, before and after your path operation:
#
#   request ->  [middleware 1 ->  [middleware 2 ->  your endpoint ]  <- middleware 2 ] <- middleware 1 -> response
#
# Use it for: timing, request ids for logs, security headers, compression, CORS (Module 23), blocking by rule.
#   @app.middleware("http")           write your own: async def f(request, call_next)
#       response = await call_next(request)      <- everything inside runs here
#   app.add_middleware(Class, **options)         add a ready-made one
# ORDER: the middleware added LAST is the OUTERMOST: it sees the request first and the response last.
# A middleware can answer by itself without calling call_next (see "blocked" below).
# LIMITS: @app.middleware("http") is easy but not meant for heavy traffic or streaming bodies;
# a pure ASGI middleware is the faster form. For checks on a few routes, prefer dependencies (Module 23).
# Built in: GZipMiddleware (compress big answers), TrustedHostMiddleware (reject a wrong Host header),
# HTTPSRedirectMiddleware, CORSMiddleware.

app = FastAPI()


@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
    return response


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    request.state.request_id = request_id               # endpoints and log lines can read it
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.middleware("http")
async def block_path(request: Request, call_next):
    if request.url.path == "/blocked":
        return JSONResponse(status_code=403, content={"detail": "blocked by middleware"})
    return await call_next(request)


app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["testserver", "localhost", "127.0.0.1"])


@app.get("/")
def root(request: Request):
    return {"request_id": request.state.request_id}


@app.get("/big")
def big():
    return {"data": "x" * 2000}
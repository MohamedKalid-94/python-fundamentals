from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# CORS (Cross-Origin Resource Sharing). A BROWSER only lets a web page call another ORIGIN
# (scheme + host + port) if that server allows it. Your Next.js page on http://localhost:3000 calling
# your API on http://localhost:8000 is "cross-origin" and fails without CORS headers.
#
#   simple request     the browser adds  Origin: http://localhost:3000
#                      the server answers  Access-Control-Allow-Origin: http://localhost:3000
#   preflight          before PUT, DELETE, JSON bodies, or custom headers the browser first sends an OPTIONS request
#                      with Access-Control-Request-Method / -Headers, and the server says what is allowed
#
# IMPORTANT
#   - CORS is enforced by the BROWSER, not by the server: a request from curl or Python still gets its
#     answer. CORS is not a security feature for your API; it only protects users' browsers.
#   - list the exact origins you trust. allow_origins=["*"] is fine for a public API with no cookies or
#     login, and for local experiments; do not combine it with credentials.
#   - allow_credentials=True lets cookies and Authorization travel; the origin must then be listed.
#   - the Origin must match exactly: http://localhost:3000 is not http://127.0.0.1:3000.

app = FastAPI()

origins = ["http://localhost:3000", "https://myapp.example.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=600,                    # the browser may remember the preflight answer for 10 minutes
)


@app.get("/data")
def data():
    return {"value": 42}


# A development-only app that allows everything
dev_app = FastAPI()
dev_app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@dev_app.get("/data")
def dev_data():
    return {"value": 42}
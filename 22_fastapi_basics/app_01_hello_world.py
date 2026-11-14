from fastapi import FastAPI

# WHAT FASTAPI IS
#   A modern Python framework for building web APIs.
#   It is built from two libraries:
#     Starlette   the web part: routing, requests, responses, WebSockets, middleware
#     Pydantic    the data part: validation and conversion, driven by TYPE HINTS
#   It runs on ASGI (an asynchronous server interface), so it handles many waiting
#   connections in one process (Module 20, coroutines).
#
# WHY IT IS POPULAR FOR AI APPS
#   - type hints give you validation, conversion and documentation for free
#   - automatic interactive docs at /docs
#   - async support: waiting for an LLM or a vector store does not block other requests
#   - one of the fastest Python frameworks, and easy to test
#
# RUN IT (two ways, from this folder):
#   fastapi dev app_01_hello_world.py                       auto-reload, 127.0.0.1:8000
#   uvicorn app_01_hello_world:app --reload                 the same, with Uvicorn directly
# THEN OPEN:  http://127.0.0.1:8000/        and        http://127.0.0.1:8000/docs
# PowerShell: Invoke-RestMethod http://127.0.0.1:8000/       (curl is an alias there; use curl.exe)

app = FastAPI()                 # the application object: "app" is the name the server looks for


@app.get("/")                   # a PATH OPERATION: HTTP method (GET) + path (/)
def home():                     # the path operation FUNCTION
    return {"message": "Hello World"}       # a dict is converted to JSON for you


# FastAPI answers for you when nothing matches:
#   unknown path    404  {"detail": "Not Found"}
#   wrong method    405  {"detail": "Method Not Allowed"}
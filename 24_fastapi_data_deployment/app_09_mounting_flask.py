from a2wsgi import WSGIMiddleware
from fastapi import FastAPI
from flask import Flask, request
from markupsafe import escape

# WSGI is the OLD synchronous Python web interface (Flask, Django). FastAPI speaks ASGI.
# a2wsgi wraps a WSGI app so it can be MOUNTED inside FastAPI under a path:
#   app.mount("/flask", WSGIMiddleware(flask_app))
# Every request under /flask goes to Flask; everything else goes to FastAPI.
#
# WHY: you have an old Flask or Django application and want to move it to FastAPI GRADUALLY.
#   1. mount the old app under /legacy      2. write new routes in FastAPI
#   3. move the old routes one by one       4. remove the mount when it is empty
# NOTES
#   - the WSGI app runs in a thread pool: it works, but without async benefits
#   - Flask and FastAPI share nothing: no common dependencies, sessions or middleware
#   - the Flask routes do NOT appear in FastAPI's /docs
#   - do not use this for new code; it is a migration tool
# Install: pip install flask a2wsgi

flask_app = Flask(__name__)


@flask_app.route("/")
def flask_home():
    return "Hello from Flask"


@flask_app.route("/hello/<name>")
def flask_hello(name):
    return f"Hello {escape(name)} from Flask"


@flask_app.route("/add")
def flask_add():
    a = request.args.get("a", 0, type=int)
    b = request.args.get("b", 0, type=int)
    return {"sum": a + b}                                   # Flask turns a dict into JSON


app = FastAPI()


@app.get("/fastapi")
def fastapi_route():
    return {"framework": "fastapi"}


app.mount("/flask", WSGIMiddleware(flask_app))              # mount AFTER the normal routes
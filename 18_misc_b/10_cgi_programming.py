import html
import http.cookies
import os
import subprocess
import sys
import threading
import urllib.request
from pathlib import Path
from urllib.parse import parse_qs
from wsgiref.simple_server import WSGIRequestHandler, make_server

# CGI (Common Gateway Interface) is the OLD way for a web server to run a program per request:
#   server -> starts your script, passes the request in ENVIRONMENT VARIABLES (and stdin for POST)
#   script -> prints headers, a blank line, then the page on stdout
# The Python "cgi" module was removed in Python 3.13, but the protocol is easy to follow with the
# standard library alone. Modern Python uses WSGI (synchronous) or ASGI (asynchronous, FastAPI).
#
#   REQUEST_METHOD   GET / POST          QUERY_STRING   the part after "?"
#   CONTENT_LENGTH   size of the body    CONTENT_TYPE   type of the body
#   HTTP_USER_AGENT  headers become HTTP_*      REMOTE_ADDR   the client's address

SCRIPT = Path(__file__).parent / "cgi_bin" / "hello_cgi.py"

def run_cgi(variables, stdin_text=""):
    """Run the script the way a web server would, and split its answer into headers and body."""
    env = {**os.environ, **variables}
    result = subprocess.run([sys.executable, str(SCRIPT)], input=stdin_text, env=env,
                            capture_output=True, text=True)
    head, _, body = result.stdout.partition("\n\n")
    headers = dict(line.split(": ", 1) for line in head.splitlines())
    return headers, body.strip()

# 1. A GET request
print(run_cgi({"REQUEST_METHOD": "GET", "QUERY_STRING": "name=Ann"}))
# ({'Content-Type': 'text/html; charset=utf-8', 'Status': '200 OK'}, '<h1>Hello, Ann!</h1>')

# 2. A POST request: the data arrives on stdin
print(run_cgi({"REQUEST_METHOD": "POST", "CONTENT_LENGTH": "8"}, "name=Bob")[1])
# <h1>Hello, Bob!</h1>

# 3. Default value, and protection against script injection (XSS)
print(run_cgi({"REQUEST_METHOD": "GET", "QUERY_STRING": ""})[1])                    # <h1>Hello, world!</h1>
print(run_cgi({"REQUEST_METHOD": "GET", "QUERY_STRING": "name=%3Cscript%3E"})[1])
# <h1>Hello, &lt;script&gt;!</h1>

# 4. The modern way: WSGI. A "web application" is just a function.
def app(environ, start_response):
    name = parse_qs(environ["QUERY_STRING"]).get("name", ["world"])[0]
    body = f"Hello, {html.escape(name)}!".encode()
    start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8"),
                              ("Content-Length", str(len(body)))])
    return [body]

class Quiet(WSGIRequestHandler):
    def log_message(self, *args):
        pass

server = make_server("127.0.0.1", 0, app, handler_class=Quiet)
threading.Thread(target=server.serve_forever, daemon=True).start()
with urllib.request.urlopen(f"http://127.0.0.1:{server.server_port}/?name=Ann", timeout=2) as response:
    print(response.status, response.read())     # 200 b'Hello, Ann!'
server.shutdown()
server.server_close()

# 5. Cookies
cookie = http.cookies.SimpleCookie()
cookie["session"] = "abc123"
cookie["session"]["path"] = "/"
print(cookie.output())                          # Set-Cookie: session=abc123; Path=/
print(http.cookies.SimpleCookie("a=1; b=2")["b"].value)         # 2

# CGI -> WSGI -> ASGI
#   CGI    a NEW process for every request: simple, slow
#   WSGI   one long-running process, the app is a function (Flask, Django, gunicorn)
#   ASGI   the same with async/await and WebSockets (FastAPI, Starlette, uvicorn)
#       from fastapi import FastAPI
#       app = FastAPI()
#       @app.get("/hello")
#       def hello(name: str = "world"):
#           return {"message": f"Hello, {name}!"}
# SECURITY  escape every value you put in HTML, validate input, never trust headers or
#           environment variables from the client, never run scripts the user uploads.
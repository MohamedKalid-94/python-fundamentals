import http.server
import json
import socket
import threading
import urllib.error
import urllib.request
from urllib.parse import (parse_qs, parse_qsl, quote, unquote, urlencode,
                          urljoin, urlparse)

# A URL:  scheme://user:password@host:port/path?query#fragment

# 1. Take a URL apart
u = urlparse("https://user:pw@example.com:8080/path/to/page.html?x=1&y=two&x=3#section")
print(u.scheme, u.netloc, u.hostname, u.port)   # https user:pw@example.com:8080 example.com 8080
print(u.username, u.password)                   # user pw
print(u.path, u.query, u.fragment)              # /path/to/page.html x=1&y=two&x=3 section

# 2. The query string
print(parse_qs(u.query))                        # {'x': ['1', '3'], 'y': ['two']}
print(parse_qsl(u.query))                       # [('x', '1'), ('y', 'two'), ('x', '3')]

# 3. Build a query string
print(urlencode({"q": "python sockets", "page": 2}))                    # q=python+sockets&page=2
print(urlencode({"q": "python sockets", "page": 2}, quote_via=quote))   # q=python%20sockets&page=2
print(urlencode({"a": [1, 2]}, doseq=True))                             # a=1&a=2

# 4. Percent-encoding (spaces and special characters)
print(quote("a b/c?d"), quote("a b/c", safe=""), quote("café"), unquote("%E2%82%AC"))
# a%20b/c%3Fd a%20b%2Fc caf%C3%A9 €

# 5. Join and change URLs
base = "https://example.com/a/b/c.html"
print(urljoin(base, "../d.html"), urljoin(base, "/x"), urljoin(base, "d.html"))
# https://example.com/a/d.html https://example.com/x https://example.com/a/b/d.html
print(u._replace(query="z=1").geturl())
# https://user:pw@example.com:8080/path/to/page.html?z=1#section

# 6. Without a scheme the host is NOT recognised
bare = urlparse("example.com/path")
print(bare.netloc == "", bare.path)             # True example.com/path


# ---------- A small local web server, so the client code below can really run ----------
class Handler(http.server.BaseHTTPRequestHandler):
    def reply(self, body, content_type="text/plain"):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parts = urlparse(self.path)
        if parts.path == "/hello":
            self.reply(json.dumps({"message": "hello"}).encode(), "application/json")
        elif parts.path == "/ua":
            self.reply(self.headers.get("User-Agent", "").encode())
        elif parts.path == "/echo":
            self.reply(json.dumps(parse_qs(parts.query)).encode(), "application/json")
        else:
            self.send_error(404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        self.reply(self.rfile.read(length).upper())

    def log_message(self, *args):               # keep the console quiet
        pass


server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
port = server.server_address[1]
threading.Thread(target=server.serve_forever, daemon=True).start()
base_url = f"http://127.0.0.1:{port}"

# 7. A GET request with urllib
with urllib.request.urlopen(f"{base_url}/hello", timeout=2) as response:
    print(response.status, response.reason, response.headers["Content-Type"])
    # 200 OK application/json
    print(json.loads(response.read()))          # {'message': 'hello'}

# 8. HTTP errors are exceptions
try:
    urllib.request.urlopen(f"{base_url}/missing", timeout=2)
except urllib.error.HTTPError as e:
    print(e.code, e.reason)                     # 404 Not Found

# 9. A POST request (the data is bytes)
request = urllib.request.Request(f"{base_url}/anything", data=b"abc", method="POST")
with urllib.request.urlopen(request, timeout=2) as response:
    print(response.read())                      # b'ABC'

# 10. Custom headers
request = urllib.request.Request(f"{base_url}/ua", headers={"User-Agent": "demo-client"})
with urllib.request.urlopen(request, timeout=2) as response:
    print(response.read().decode())             # demo-client

# 11. Send a query string safely
query = urlencode({"name": "Ann", "n": 1})
with urllib.request.urlopen(f"{base_url}/echo?{query}", timeout=2) as response:
    print(json.loads(response.read()))          # {'name': ['Ann'], 'n': ['1']}

# 12. A server that is not there: the error is wrapped in URLError
probe = socket.socket()
probe.bind(("127.0.0.1", 0))
dead_port = probe.getsockname()[1]
probe.close()
try:
    urllib.request.urlopen(f"http://127.0.0.1:{dead_port}/", timeout=1)
except urllib.error.URLError as e:
    print(type(e.reason).__name__)              # ConnectionRefusedError

server.shutdown()
server.server_close()

# HTTP CHEAT SHEET
#   GET read        POST create/send       PUT replace        DELETE remove       PATCH change a part
#   200 OK   201 Created   204 No Content   301/302 redirect   400 bad request   401 login needed
#   403 forbidden   404 not found   429 too many requests   500 server error   503 unavailable
#
# For real projects most people use the third-party "requests" (or "httpx") package:
#   import requests
#   r = requests.get("https://api.example.com/items", params={"page": 2}, timeout=5)
#   r.raise_for_status();  data = r.json()
# Installing packages with pip is covered in Module 18. Always pass a timeout, and never turn
# off HTTPS certificate checks.
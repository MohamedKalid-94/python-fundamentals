import http.server
import json
import socket
import socketserver
import struct
import threading
from ipaddress import ip_address, ip_network
from urllib.parse import urlencode, urljoin, urlsplit, urlunsplit
import urllib.request


def recv_exactly(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("connection closed")
        buf += chunk
    return buf


# 1. A port scanner (on your own machine): which ports accept a connection?
def scan(host, ports, timeout=0.5):
    result = {}
    for port in ports:
        with socket.socket() as s:
            s.settimeout(timeout)
            result[port] = s.connect_ex((host, port)) == 0      # 0 means "connected"
    return result

listener = socket.socket()
listener.bind(("127.0.0.1", 0))
listener.listen()
open_port = listener.getsockname()[1]
probe = socket.socket()
probe.bind(("127.0.0.1", 0))
closed_port = probe.getsockname()[1]
probe.close()

print(list(scan("127.0.0.1", [open_port, closed_port]).values()))      # [True, False]
listener.close()


# 2. A line-based echo server with socketserver (one thread per client)
class EchoHandler(socketserver.StreamRequestHandler):
    def handle(self):
        for line in self.rfile:                 # reads until the client stops sending
            self.wfile.write(b"echo: " + line)

echo = socketserver.ThreadingTCPServer(("127.0.0.1", 0), EchoHandler)
echo.daemon_threads = True
threading.Thread(target=echo.serve_forever, daemon=True).start()

with socket.create_connection(echo.server_address, timeout=2) as c:
    c.sendall(b"hello\nworld\n")
    c.shutdown(socket.SHUT_WR)                  # "I have finished sending"
    data = b""
    while chunk := c.recv(1024):
        data += chunk
print(data)                                     # b'echo: hello\necho: world\n'
echo.shutdown()
echo.server_close()


# 3. A tiny JSON request/response protocol with a length prefix
def send_json(sock, obj):
    data = json.dumps(obj).encode()
    sock.sendall(struct.pack(">I", len(data)) + data)

def recv_json(sock):
    (n,) = struct.unpack(">I", recv_exactly(sock, 4))
    return json.loads(recv_exactly(sock, n))

def rpc_server(sock):
    for _ in range(2):
        request = recv_json(sock)
        if request["cmd"] == "add":
            send_json(sock, {"result": sum(request["args"])})
        else:
            send_json(sock, {"error": "unknown command"})

a, b = socket.socketpair()
t = threading.Thread(target=rpc_server, args=(b,))
t.start()
send_json(a, {"cmd": "add", "args": [2, 3]})
print(recv_json(a))                             # {'result': 5}
send_json(a, {"cmd": "fly"})
print(recv_json(a))                             # {'error': 'unknown command'}
t.join()
a.close()
b.close()


# 4. A binary frame for a sensor: 0xAA | type | length | payload | checksum
def build_frame(msg_type, payload):
    body = bytes([0xAA, msg_type, len(payload)]) + payload
    return body + bytes([sum(body) & 0xFF])

def parse_frame(frame):
    if frame[0] != 0xAA:
        raise ValueError("bad header")
    if sum(frame[:-1]) & 0xFF != frame[-1]:
        raise ValueError("bad checksum")
    return frame[1], frame[3:3 + frame[2]]

frame = build_frame(0x01, (253).to_bytes(2, "big", signed=True))       # 25.3 degrees in tenths
print(frame.hex())                              # aa010200fdaa
msg_type, payload = parse_frame(frame)
print(msg_type, int.from_bytes(payload, "big", signed=True) / 10)      # 1 25.3

corrupted = frame[:-1] + b"\x00"
try:
    parse_frame(corrupted)
except ValueError as e:
    print(e)                                    # bad checksum


# 5. UDP with a timeout and a retry (UDP can lose packets)
usrv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
usrv.bind(("127.0.0.1", 0))
uport = usrv.getsockname()[1]

def lossy_server():
    for n in range(2):
        data, addr = usrv.recvfrom(100)
        if n == 1:
            usrv.sendto(b"pong", addr)          # the first datagram is "lost" on purpose

t = threading.Thread(target=lossy_server)
t.start()
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(0.1)
for attempt in range(1, 4):
    client.sendto(b"ping", ("127.0.0.1", uport))
    try:
        reply, _ = client.recvfrom(100)
        break
    except TimeoutError:
        print(f"attempt {attempt}: no reply")
print(reply, attempt)
# attempt 1: no reply
# b'pong' 2
t.join()
client.close()
usrv.close()


# 6. A JSON "sensor API" and a client that formats the answer
class SensorApi(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"temp": 25.3}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass

api = http.server.ThreadingHTTPServer(("127.0.0.1", 0), SensorApi)
threading.Thread(target=api.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{api.server_address[1]}/temp"
with urllib.request.urlopen(url, timeout=2) as response:
    data = json.loads(response.read())
print(f"{data['temp']:.1f} C")                  # 25.3 C
api.shutdown()
api.server_close()


# 7. Build a URL with a query string
def build_url(base, path, **params):
    url = urljoin(base, path)
    return f"{url}?{urlencode(params)}" if params else url

print(build_url("https://api.example.com", "/v1/items", page=2, q="a b"))
# https://api.example.com/v1/items?page=2&q=a+b


# 8. Normalise a URL: lower-case scheme and host, drop the default port and the fragment
def normalize(url):
    p = urlsplit(url)
    host = (p.hostname or "").lower()
    default = {"http": 80, "https": 443}.get(p.scheme.lower())
    netloc = host if p.port in (None, default) else f"{host}:{p.port}"
    return urlunsplit((p.scheme.lower(), netloc, p.path or "/", p.query, ""))

print(normalize("HTTP://Example.COM:80/a?x=1#frag"))        # http://example.com/a?x=1
print(normalize("https://example.com"))                     # https://example.com/


# 9. Which addresses can a /29 network use?
net = ip_network("192.168.1.0/29")
hosts = list(net.hosts())
print(len(hosts), hosts[0], hosts[-1], ip_address("192.168.1.5") in net)
# 6 192.168.1.1 192.168.1.6 True
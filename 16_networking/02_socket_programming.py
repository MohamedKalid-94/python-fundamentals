import select
import socket
import struct
import threading

# A SOCKET is one end of a network connection. The functions have the same names as in C.
#
#   TCP SERVER                          TCP CLIENT
#   socket()                            socket()
#   bind((host, port))                  connect((host, port))
#   listen()                            send / recv  (sendall / recv)
#   accept() -> (conn, address)         close()
#   recv / send on conn
#   close()
#
#   UDP: no listen/accept/connect. The server does bind() then recvfrom()/sendto().
#        The client just does sendto() and recvfrom().

# 1. A TCP echo server (in a thread) and a client
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # allow a quick restart
server.bind(("127.0.0.1", 0))                   # port 0: the OS picks a free port
server.listen()
port = server.getsockname()[1]
print(isinstance(port, int), port > 1023)       # True True

seen = []

def serve_once():
    conn, addr = server.accept()                # waits for a client
    with conn:
        data = conn.recv(1024)
        seen.append(addr[0])
        conn.sendall(data.upper())              # send the answer

t = threading.Thread(target=serve_once)
t.start()

with socket.create_connection(("127.0.0.1", port), timeout=2) as client:
    client.sendall(b"hello")                    # sockets send BYTES, not str
    print(client.recv(1024))                    # b'HELLO'
t.join()
print(seen)                                     # ['127.0.0.1']
server.close()
# text <-> bytes:  "café".encode("utf-8")   and   data.decode("utf-8")

# 2. TCP is a BYTE STREAM: it does not keep message boundaries
c, d = socket.socketpair()                      # two connected sockets in one program
c.sendall(b"one")
c.sendall(b"two")
print(d.recv(10))                               # b'onetwo'      two sends, one receive
c.close()
d.close()

# 3. So a protocol needs FRAMING: here a 4-byte length in front of every message
def send_msg(sock, text):
    data = text.encode("utf-8")
    sock.sendall(struct.pack(">I", len(data)) + data)

def recv_exactly(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:                           # b"" means the other side closed
            raise ConnectionError("connection closed")
        buf += chunk
    return buf

def recv_msg(sock):
    (length,) = struct.unpack(">I", recv_exactly(sock, 4))
    return recv_exactly(sock, length).decode("utf-8")

a, b = socket.socketpair()
send_msg(a, "first")
send_msg(a, "second")
print([recv_msg(b), recv_msg(b)])               # ['first', 'second']
a.close()
print(b.recv(10))                               # b''     the other side has closed
b.close()
# Other framing choices: a delimiter ("\n"), fixed-size frames, or a start byte + length.

# 4. A server that handles several clients at the same time (one thread per client)
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind(("127.0.0.1", 0))
srv.listen()
port2 = srv.getsockname()[1]

def handle(conn):
    with conn:
        name = conn.recv(100).decode()
        conn.sendall(f"hello {name}".encode())

def accept_loop():
    for _ in range(3):
        conn, _addr = srv.accept()
        threading.Thread(target=handle, args=(conn,)).start()

acceptor = threading.Thread(target=accept_loop)
acceptor.start()

replies = []

def ask(name):
    with socket.create_connection(("127.0.0.1", port2), timeout=2) as sock:
        sock.sendall(name.encode())
        replies.append(sock.recv(100).decode())

clients = [threading.Thread(target=ask, args=(n,)) for n in "abc"]
for t in clients:
    t.start()
for t in clients:
    t.join()
acceptor.join()
srv.close()
print(sorted(replies))                          # ['hello a', 'hello b', 'hello c']

# 5. UDP: datagrams, no connection
usrv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
usrv.bind(("127.0.0.1", 0))
uport = usrv.getsockname()[1]

def udp_server():
    data, addr = usrv.recvfrom(1024)
    usrv.sendto(b"pong:" + data, addr)

t = threading.Thread(target=udp_server)
t.start()
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as uc:
    uc.settimeout(2)
    uc.sendto(b"ping", ("127.0.0.1", uport))
    data, addr = uc.recvfrom(1024)
    print(data, addr[1] == uport)               # b'pong:ping' True
t.join()
usrv.close()

# 6. Typical errors
probe = socket.socket()
probe.bind(("127.0.0.1", 0))
dead_port = probe.getsockname()[1]
probe.close()                                   # now nobody listens on dead_port
try:
    socket.create_connection(("127.0.0.1", dead_port), timeout=5)
except ConnectionRefusedError:
    print("ConnectionRefusedError")             # ConnectionRefusedError   (Windows needs about 2 s)

waiter = socket.socket()
waiter.bind(("127.0.0.1", 0))
waiter.listen()
waiter.settimeout(0.05)                         # a timeout instead of waiting forever
try:
    waiter.accept()
except TimeoutError:
    print("TimeoutError")                       # TimeoutError   (socket.timeout in older code)
waiter.close()

# 7. select(): ask which sockets have data, without blocking
x, y = socket.socketpair()
readable, _, _ = select.select([y], [], [], 0.05)
print(len(readable))                            # 0       nothing to read yet
x.sendall(b"data")
readable, _, _ = select.select([y], [], [], 1)
print(len(readable), y.recv(10))                # 1 b'data'

# 8. shutdown(): "I have finished SENDING", the other side then reads b""
x.shutdown(socket.SHUT_WR)
print(y.recv(10))                               # b''
x.close()
y.close()

# RULES OF THUMB
# - sendall() sends everything; send() may send only part of the data.
# - recv(n) returns AT MOST n bytes (it may return fewer). b"" means the peer closed.
# - ALWAYS set a timeout (settimeout) so a dead peer cannot freeze the program.
# - Bind to "127.0.0.1" for local use. "0.0.0.0" listens on ALL interfaces (the whole network).
# - Many clients: a thread per client (above), the selectors module, socketserver, or asyncio.
# - Encryption: wrap a socket with the ssl module (TLS); never send secrets in plain text.
# - Never use pickle for data that comes from the network (it can run code).
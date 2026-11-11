# Module 16: Networking, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Networking | Layers | Application (HTTP, MQTT), transport (TCP, UDP), internet (IP), link (Ethernet, Wi-Fi) |
| 01 | Networking | Address and port | IP address picks the computer; the port picks the program (0 to 65535) |
| 01 | Networking | Port ranges | 0-1023 well known, 1024-49151 registered, 49152-65535 ephemeral |
| 01 | Networking | TCP | Connection, reliable, ordered BYTE STREAM (no message boundaries) |
| 01 | Networking | UDP | No connection, datagrams, may be lost or reordered, message boundaries kept |
| 01 | Networking | DNS | `socket.gethostbyname("localhost")` is `127.0.0.1`; `getaddrinfo` for more detail |
| 01 | Networking | `ipaddress` | `ip_address`, `ip_network`, `.is_private`, `.hosts()`, `in net`, `.subnets()` |
| 01 | Networking | IPv4 bytes | `inet_aton` / `inet_ntoa`; an address is 4 bytes |
| 01 | Networking | Byte order | The network is big-endian: `struct.pack(">H", x)`, `htons`, `ntohs` |
| 01 | Networking | `struct` | `pack`, `unpack`, `calcsize` with formats like `">BBH"` |
| 02 | Sockets | Server steps | `socket()`, `bind()`, `listen()`, `accept()`, `recv`/`sendall`, `close()` |
| 02 | Sockets | Client steps | `socket()`, `connect()` (or `create_connection`), `sendall`/`recv`, `close()` |
| 02 | Sockets | Types | `AF_INET` (IPv4), `AF_INET6`; `SOCK_STREAM` (TCP), `SOCK_DGRAM` (UDP) |
| 02 | Sockets | Port 0 | `bind(("127.0.0.1", 0))` lets the OS pick a free port; read it with `getsockname()` |
| 02 | Sockets | Bytes | Sockets send and receive `bytes`; `encode()` and `decode()` for text |
| 02 | Sockets | `recv(n)` | Returns at most `n` bytes; `b""` means the peer closed |
| 02 | Sockets | `sendall` | Sends everything; `send` may send only part |
| 02 | Sockets | Framing | TCP merges and splits data: use a length prefix, a delimiter or fixed frames |
| 02 | Sockets | Many clients | A thread per client, `selectors` / `select`, `socketserver`, or `asyncio` |
| 02 | Sockets | UDP | `bind` + `recvfrom` on the server; `sendto` + `recvfrom` on the client |
| 02 | Sockets | Errors | `ConnectionRefusedError` (nobody listens), `TimeoutError` (use `settimeout`), `ConnectionError` |
| 02 | Sockets | `shutdown(SHUT_WR)` | "I am done sending"; the peer then reads `b""` |
| 02 | Sockets | `socketpair()` | Two connected sockets in one program (good for tests) |
| 02 | Sockets | Safety | Bind to `127.0.0.1` for local use; use `ssl` for encryption; never `pickle` network data |
| 03 | URLs | Parts | `urlparse(url)`: `scheme`, `netloc`, `hostname`, `port`, `path`, `query`, `fragment` |
| 03 | URLs | Query | `parse_qs` (dict of lists), `parse_qsl` (list of pairs), `urlencode` (`doseq=True` for lists) |
| 03 | URLs | Encoding | `quote` and `unquote`; `quote(x, safe="")` also encodes `/` |
| 03 | URLs | Join | `urljoin(base, relative)` handles `../` and `/absolute` |
| 03 | URLs | Change | `u._replace(query=...).geturl()` |
| 03 | URLs | No scheme | `urlparse("example.com/path")` puts everything into `path` |
| 03 | URLs | Client | `urllib.request.urlopen(url, timeout=...)`, `Request(url, data=..., headers=..., method=...)` |
| 03 | URLs | Errors | `HTTPError` (has `.code`, `.reason`), `URLError` (`.reason` holds the cause) |
| 03 | URLs | Server | `http.server.ThreadingHTTPServer` with a `BaseHTTPRequestHandler` (`do_GET`, `do_POST`) |
| 03 | URLs | Real projects | The `requests` or `httpx` package; always set a timeout and keep certificate checks on |
| 03 | URLs | Status codes | 200 OK, 201 Created, 301/302 redirect, 400, 401, 403, 404, 429, 500, 503 |
| 04 | Generics | Idea | Write code once and keep the type information for every use |
| 04 | Generics | `TypeVar` | `T = TypeVar("T")`: the same type everywhere in one signature |
| 04 | Generics | Class | `class Stack(Generic[T])`; use `Stack[int]` in annotations |
| 04 | Generics | Not enforced | Python ignores the hints at run time; mypy and Pyright check them |
| 04 | Generics | Limits | `TypeVar("N", int, float)` (constraints) or `bound=Protocol` |
| 04 | Generics | Helpers | `Callable[[T], V]`, `Iterable[T]`, `list[T]`, `dict[K, V]`, `T \| None` |
| 04 | Generics | Introspection | `get_origin(list[int])` and `get_args(dict[str, int])` |
| 05 | Generics 3.12 | Syntax | `class Box[T]:`, `def last[T](...)`, `[N: (int, float)]`, `[S: Square]` |
| 05 | Generics 3.12 | Alias | `type Pairs[K, V] = list[tuple[K, V]]` |
| 06 | Examples | Port scan | `connect_ex(...) == 0` means the port is open |
| 06 | Examples | `socketserver` | `StreamRequestHandler` with `ThreadingTCPServer` for a line protocol |
| 06 | Examples | Protocol design | Length prefix + JSON, or `0xAA | type | length | payload | checksum` |
| 06 | Examples | UDP retry | `settimeout`, resend on `TimeoutError`, give up after N attempts |
| 06 | Examples | URL helpers | `urljoin` + `urlencode` to build, `urlsplit` + `urlunsplit` to normalise |
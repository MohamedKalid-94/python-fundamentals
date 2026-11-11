Write the questions as # comments and your solutions as code below each one. Use 127.0.0.1 and port 0 for every server.

Use ipaddress to print, for 10.1.2.0/23: the netmask, the broadcast address, the number of usable hosts, the first and the last host, and whether 10.1.3.200 and 10.1.4.1 belong to it.
Convert "192.168.10.77" to its 4 bytes, to a single integer, and back, in three ways (inet_aton, int(ip_address(...)), a manual shift and mask).
Split 192.168.1.0/24 into 8 equal subnets and print each one with its number of usable hosts.
Use struct to build a 6-byte header with a version (1 byte), a flags field (1 byte), a length (2 bytes) and a sequence number (2 bytes), all big-endian. Unpack it, then print the same data in little-endian and compare the bytes.
Write a TCP echo server in a thread and a client that sends 3 messages one after another and prints the answers. Show what happens when the client sends the 3 messages very quickly (the stream merges them).
Write send_msg and recv_msg with a 2-byte length prefix, and test them with 5 messages of different sizes (including an empty one and one of 70,000 bytes, which does not fit in 2 bytes: handle the error).
Write a server that accepts 5 clients at the same time, each sending a number, and replies with the number squared. Collect and sort the replies in the clients.
Write a chat-like server with socketserver.ThreadingTCPServer that keeps a list of connected clients and sends every line it receives to all the other clients (a broadcast). Test it with 3 clients in threads.
Write a UDP “time server” that answers b"TIME" with a fixed string and b"QUIT" by stopping, plus a client with a timeout and 3 retries. Make the server drop the first request to test the retry.
Write a port scanner for 127.0.0.1 ports 1 to 1024 that uses a thread pool (Module 15), prints the open ports sorted and the time it took, and compare it with a version without threads. (Open one port yourself so the result is not empty.)
Use select.select or selectors to build a server that handles 3 clients in ONE thread.
Write a client for the server of example 3 in file 06 that retries three times with a growing delay when the connection is refused, and gives up with a clear message.
Parse these URLs and print the scheme, host, port (with the default for the scheme when missing), path, query as a dictionary and fragment: https://example.com/a/b?x=1&y=2#top, http://localhost:8000/api/items?id=5&id=6, ftp://user@files.example.org/pub/.
Write is_valid_http_url(text) that accepts only http and https URLs with a host, and test it with 8 good and bad strings ("javascript:alert(1)", "example.com", "http://", ...).
Write with_query(url, **changes) that adds or replaces query parameters of a URL while keeping the others, using parse_qsl, urlencode and _replace.
Start a local http.server that serves GET /items (a JSON list) and POST /items (adds an item and returns 201). Write a client with urllib.request that adds three items and then reads the list. Show how a 404 appears as an HTTPError.
Add a header-based check to the server of exercise 16 (an X-Api-Key header) that answers 401 when it is missing or wrong, and show the client handling it.
Write a small “key-value store” server over TCP with commands SET key value, GET key, DEL key (one command per line), and a client that tests all three, including a missing key.
Embedded exercise: define a binary protocol for a sensor with frames 0x7E | type | length | payload | CRC8 (use your CRC-8 from Module 12), write encode and decode, then send 10 frames over a socketpair and decode them from a stream where the frames are cut at random points (a receiver that buffers).
Embedded exercise: write a “gateway”: a thread that reads simulated UART bytes from a queue, assembles frames, and sends each one as JSON over UDP to a collector socket, which prints the values it receives.
Write a generic Stack[T], a generic Queue[T] and a generic function chunked(items: Iterable[T], size: int) -> list[list[T]] with full type hints, then run mypy on the file (pip install mypy) and fix what it reports. Add one deliberate type mistake to see its message.
Predict first, then run, and explain each result in a comment:
python
import socket
from urllib.parse import urlparse, parse_qs, urljoin, quote

a, b = socket.socketpair()
a.sendall(b"ab")
a.sendall(b"cd")
a.close()
print(b.recv(3), b.recv(3), b.recv(3))

u = urlparse("//example.com:81/p?q=1&q=2")
print(u.scheme == "", u.hostname, u.port, parse_qs(u.query))

print(urljoin("http://x.org/a/b", "c"), urljoin("http://x.org/a/b/", "../c"))
print(quote("100% sure/ok"), quote("100% sure/ok", safe=""))

print(int.from_bytes(b"\x01\x00", "big"), int.from_bytes(b"\x01\x00", "little"))
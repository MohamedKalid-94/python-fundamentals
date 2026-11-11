#!/usr/bin/env python3
import html
import os
import sys
from urllib.parse import parse_qs

method = os.environ.get("REQUEST_METHOD", "GET")
if method == "POST":
    length = int(os.environ.get("CONTENT_LENGTH", "0") or 0)
    params = parse_qs(sys.stdin.read(length))
else:
    params = parse_qs(os.environ.get("QUERY_STRING", ""))

name = html.escape(params.get("name", ["world"])[0])      # ESCAPE user input

print("Content-Type: text/html; charset=utf-8")
print("Status: 200 OK")
print()                                                   # the blank line ends the headers
print(f"<h1>Hello, {name}!</h1>")
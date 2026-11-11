# Module 18: Miscellaneous B, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | PIP | `python -m pip` | Always use it so you install into the SAME Python you run |
| 01 | PIP | Commands | `install`, `install -U`, `uninstall`, `list`, `show`, `freeze`, `install -r requirements.txt`, `install -e .` |
| 01 | PIP | Versions | `==1.2.3`, `>=1.2`, `<3`, `!=`, `~=` |
| 01 | PIP | Virtual environment | `python -m venv .venv`, then activate; one environment per project; do not commit it |
| 01 | PIP | Files | `requirements.txt` lists packages; `pyproject.toml` describes a project |
| 01 | PIP | Safety | Check package names, pin versions, `pip-audit` |
| 02 | Database | DB-API | `connect`, `execute`, `fetchone`, `fetchall`, `commit`, `rollback`, `close` |
| 02 | Database | SQLite | In the standard library; `":memory:"` or a file |
| 02 | Database | Parameters | `?` or `:name`; NEVER put values into SQL with f-strings (SQL injection) |
| 02 | Database | Cursor | `rowcount`, `lastrowid`, `description`, `fetchmany(n)`, loop over it |
| 02 | Database | Transactions | `with conn:` commits, or rolls back on an error |
| 02 | Database | Constraints | `NOT NULL`, `UNIQUE`, `CHECK`, `FOREIGN KEY` raise `IntegrityError`; use `PRAGMA foreign_keys = ON` |
| 02 | Database | Rows | `conn.row_factory = sqlite3.Row` gives column names |
| 02 | Database | Layout | Keep SQL in `.sql` files, Python in `.py` files |
| 03 | Weak References | `weakref.ref(obj)` | Call it to get the object or `None`; it does not keep the object alive |
| 03 | Weak References | Containers | `WeakValueDictionary` (caches), `WeakSet` (observers), `WeakKeyDictionary` |
| 03 | Weak References | Limits | Not for `int`, `str`, `list`, `dict`, `tuple`; fine for class instances and functions |
| 03 | Weak References | `finalize` | A cleanup when an object dies (better than `__del__`) |
| 03 | Weak References | Back-links | A child holds a weak reference to its parent to avoid cycles |
| 03 | Weak References | `gc` | `gc.collect()` frees reference cycles |
| 04 | Serialization | `pickle` | Python objects to bytes, types preserved; Python only |
| 04 | Serialization | Danger | Unpickling can run code: NEVER unpickle untrusted data |
| 04 | Serialization | Custom | `__getstate__` and `__setstate__` leave out unpicklable parts (locks, connections) |
| 04 | Serialization | Others | `shelve` (a dict in a file), `tomllib` (read TOML, 3.11+), `struct` (binary layouts) |
| 04 | Serialization | Choose | JSON for exchange, pickle for your own caches, TOML for config, sqlite for queries |
| 05 | JSON | Calls | `dumps`, `loads` (text); `dump`, `load` (files) |
| 05 | JSON | Options | `indent`, `sort_keys`, `separators`, `ensure_ascii=False` |
| 05 | JSON | Mapping | dict is object, list and tuple are array, `None` is `null`; tuples come back as lists, dict keys as strings |
| 05 | JSON | Unknown types | `default=function` or a `JSONEncoder` subclass; `object_hook` and `parse_float` when decoding |
| 05 | JSON | Errors | `JSONDecodeError` (a `ValueError`) for single quotes or trailing commas |
| 05 | JSON | Also | JSON Lines for logs; strip code fences from model answers before `loads` |
| 06 | Templating | `string.Template` | `$name`, `${name}`; `substitute` (KeyError if missing), `safe_substitute`, `$$` |
| 06 | Templating | Escaping | `html.escape` on every user value placed in HTML |
| 06 | Templating | `format_map` | With a `__missing__` dictionary to keep unknown placeholders |
| 06 | Templating | `textwrap` | `wrap`, `fill`, `dedent`, `indent`, `shorten` |
| 06 | Templating | Real use | Jinja2 for pages and e-mails; templates also generate code (C headers) |
| 07 | Output Formatting | `print` | `sep`, `end`, `file`, `flush`; `redirect_stdout` captures output |
| 07 | Output Formatting | Specs | `>8`, `<8`, `^8`, `08b`, `#x`, `,`, `_`, `.2f`, `.1%`, `.2e` |
| 07 | Output Formatting | Tables | Work out the column width from the data: `f"{name:<{w}}"` |
| 07 | Output Formatting | `pprint` | `pformat(data, width=..., sort_dicts=False)` |
| 07 | Output Formatting | `reprlib` | A short repr of huge objects |
| 07 | Output Formatting | `__format__` | Your class decides what `f"{obj:spec}"` gives |
| 08 | Performance | Clocks | `perf_counter` (wall time), `process_time` (CPU time) |
| 08 | Performance | `timeit` | Repeat small code; use the minimum of `repeat()` runs |
| 08 | Performance | Profilers | `cProfile` and `pstats` (which functions), `tracemalloc` (memory), `line_profiler`, `py-spy` |
| 08 | Performance | Wins | Sets and dicts for lookups, `join`, generators, `deque`, built-ins, NumPy, `lru_cache` |
| 08 | Performance | Rule | Measure first; a better algorithm beats micro-tricks |
| 09 | Compression | `zlib` | `compress`, `decompress`, levels 1 to 9, `crc32`, `adler32`, `compressobj` for streams |
| 09 | Compression | Formats | `gzip`, `bz2`, `lzma` (smaller, slower), `zipfile`, `tarfile`, `shutil.make_archive` |
| 09 | Compression | Limits | Random data does not compress |
| 09 | Compression | Safety | Extract untrusted archives carefully (`filter="data"`); beware zip bombs |
| 10 | CGI | Protocol | The server starts the script; request data comes in environment variables and stdin; the script prints headers, a blank line, the body |
| 10 | CGI | Variables | `REQUEST_METHOD`, `QUERY_STRING`, `CONTENT_LENGTH`, `HTTP_*` |
| 10 | CGI | Status | The `cgi` module is gone in Python 3.13; use WSGI (`wsgiref`, Flask) or ASGI (FastAPI) |
| 10 | CGI | Cookies | `http.cookies.SimpleCookie` |
| 10 | CGI | Security | Escape output, validate input, never trust client data |
| 11 | XML | Tree | `ET.fromstring`, `find`, `findall`, `iter`, `.tag`, `.attrib`, `.get()`, `.text`, `.tail` |
| 11 | XML | Build | `ET.Element`, `ET.SubElement`, `ET.indent`, `ET.tostring(encoding="unicode")`, `ElementTree.write` |
| 11 | XML | Extras | Namespaces (`{uri}tag`), `ParseError`, `iterparse` for big files, `minidom` pretty printing |
| 11 | XML | Security | ElementTree is not safe for untrusted XML: use `defusedxml` |
| 12 | GUI | tkinter | `Tk`, `ttk.Label/Entry/Button`, `StringVar`, `grid`, `bind`, `after`, `mainloop` |
| 12 | GUI | Event loop | A slow callback freezes the window; use a thread plus `after()`; never touch widgets from a thread |
| 12 | GUI | Layout | `pack`, `grid`, `place` |
| 12 | GUI | Needs | A desktop display |
| 13 | GUIs | Choose | tkinter (small tools), PySide6 (desktop products), Gradio and Streamlit (AI demos, dashboards), FastAPI plus a front end (web products), Kivy (mobile) |
| 14 | Command line | Raw | `sys.argv` |
| 14 | Command line | `argparse` | Positional, optional, `type`, `default`, `choices`, `nargs`, `action` (`store_true`, `count`, `append`, `version`) |
| 14 | Command line | Testing | `parse_args(list)` lets you test a parser without a terminal |
| 14 | Command line | Errors | Usage goes to stderr and the exit code is 2 |
| 14 | Command line | Groups | `add_mutually_exclusive_group`, `add_subparsers`, `set_defaults(func=...)` |
| 14 | Command line | Shape | `main(argv=None)` returns an exit code; `sys.exit(main())` |
| 15 | Docstrings | What | The first string of a module, class or function; stored in `__doc__` |
| 15 | Docstrings | Reading | `help()`, `inspect.getdoc()`, `python -m pydoc` |
| 15 | Docstrings | Style | PEP 257: triple double quotes, imperative summary line, then details; Google, NumPy or reST layouts |
| 15 | Docstrings | `doctest` | `>>>` examples in docstrings are tests: `doctest.testmod()` |
| 15 | Docstrings | Types | Put types in annotations, not docstrings |
| 16 | Email | Build | `EmailMessage`: headers, `set_content`, `add_attachment`, `add_alternative` |
| 16 | Email | Send | `smtplib.SMTP(host, port)` then `send_message`; `starttls()` on 587, `SMTP_SSL` on 465 |
| 16 | Email | Parse | `email.message_from_bytes(data, policy=policy.default)`, `get_body`, `iter_attachments`, `walk` |
| 16 | Email | Helpers | `formataddr`, `parseaddr`, `formatdate`, `make_msgid` |
| 16 | Email | Rules | No passwords in code (environment variables), app passwords, rate limits, SPF/DKIM, use an email API for volume |
| 17 | Extensions | `ctypes` | `Structure`, `BigEndianStructure`, `_pack_`, `sizeof`, arrays, pointers, `CDLL`, `CFUNCTYPE` |
| 17 | Extensions | Calls | Set `argtypes` and `restype` for every C function |
| 17 | Extensions | Other ways | `cffi`, Cython, C extension with `Python.h`, `pybind11`, `PyO3`, NumPy and Numba |
| 17 | Extensions | `memoryview` | Zero-copy access to a buffer |
| 17 | Extensions | `subprocess` | `run([...], capture_output=True, text=True, check=True)`; avoid `shell=True` with user text |
| 18 | Tools | Hashes | `hashlib.sha256`, `hmac`, `secrets`; md5 and sha1 are not for security |
| 18 | Tools | Encodings | `base64`, `bytes.hex()`, `uuid` |
| 18 | Tools | Data tools | `Counter`, `defaultdict`, `deque`, `ChainMap`, `OrderedDict`, `heapq`, `bisect` |
| 18 | Tools | Code tools | `ast.literal_eval` (safe), `ast.parse`, `dis`, `unittest` |
| 18 | Tools | `python -m` | `http.server`, `json.tool`, `venv`, `timeit`, `zipfile`, `pdb` |
| 19 | Odds and Ends | Special objects | `...` (Ellipsis), `NotImplemented` |
| 19 | Odds and Ends | Strings | Equal strings built at run time are different objects; use `==`; `sys.intern` |
| 19 | Odds and Ends | Classes | `__slots__` (less memory, no new attributes), `@total_ordering`, `TypedDict` |
| 19 | Odds and Ends | `contextlib` | `ExitStack` (cleanups run in reverse), `nullcontext`, `suppress` |
| 19 | Odds and Ends | Others | `zip(strict=True)`, `zip(*matrix)`, `atexit.register`, `__pycache__` |
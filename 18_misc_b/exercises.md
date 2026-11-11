Write the questions as # comments and your solutions as code below each one. Put any SQL you write in .sql files.

PIP, serialization, JSON

Create a virtual environment named .venv, activate it, install requests, run pip freeze > requirements.txt, then delete the environment and rebuild it from the file. Write down every command you used.
Write parse_requirements(text) that returns a list of (name, specifier) pairs and ignores comments, blank lines and -e lines.
Save a dictionary that contains a datetime, a set, a Decimal and a dataclass as JSON (with default= or a JSONEncoder) and load it back with the right types (object_hook).
Write a small save(obj, path) / load(path) pair that uses pickle, and show with a class that holds a lock how __getstate__ and __setstate__ fix the error. Then explain why you should not load a pickle file from the internet.
Convert a JSON file of 1000 records to JSON Lines and back, and compare the file sizes and the time each way takes.
Write safe_json_loads(text, default=None) that never raises, strips Markdown code fences, and returns the default for invalid JSON.

Database

Create a library.db with the tables authors, books and loans (with foreign keys) from schema.sql, load sample data from seed.sql, and write the queries in queries.sql: books per author, books currently on loan, the author with the most books.
Write insert_many(conn, rows) with executemany, make it all-or-nothing with a transaction, and show that one bad row rolls back every row.
Show an SQL-injection attack on a function that builds SQL with an f-string, then fix it with parameters. Print both results.
Write a Repository class around sqlite3 with add, get, list, update and delete methods that returns dataclasses (using sqlite3.Row).

Weak references, formatting, performance

Build a cache with WeakValueDictionary for objects created by a slow load(name) function. Show that a second load of the same name is instant while the object is alive, and slow again after it is deleted.
Print a report as a table with computed column widths: name left-aligned, price right-aligned with 2 decimals and a thousands separator, a percentage column and a total row. Then print the same data with pprint and as JSON.
Compare three ways of building a string of 100,000 numbers (+=, a list with join, an io.StringIO) with timeit, and profile one of them with cProfile. Use tracemalloc to compare the memory of a list and a generator for 1 million squares.

Compression, CGI, XML

Write backup(folder, target) that creates a .zip of a folder, then verify(target) that checks it with testzip() and compares a CRC32 of every file with the original.
Write the CGI script of this lesson again so that it reads a form with two numbers and returns their sum as JSON (Content-Type: application/json), and test it with subprocess for GET and POST. Then write the same thing as a WSGI app.
Parse an RSS-like XML file (title, link, items with dates), print the 3 newest items, then write a new XML file that contains only the items from a given month.
Write dict_to_xml(tag, data) and xml_to_dict(element) for nested dictionaries and lists, and test the round trip.

GUI, command line, docstrings

Build a tkinter app with an entry, a “Convert” button, and a listbox that keeps a history of the last 5 conversions (km to miles). Add a --interactive mode like in the lesson and a self-test mode that drives the window from code.
Write a command-line tool logstat with argparse: logstat count FILE --level ERROR, logstat top FILE -n 5 (most frequent messages), --json for machine-readable output, and --version. Return exit code 0, 1 or 2, and test it by calling main(argv) with lists.
Write docstrings in Google style for a module of 5 functions and a class, add doctest examples, run python -m doctest -v, and generate the documentation with python -m pydoc -w.

Email, extensions, tools, odds and ends

Using the fake SMTP server of file 16, write send_report(to, subject, rows) that sends an HTML table with a plain-text alternative and a CSV attachment, then parse the received message and check every part.
Use ctypes to describe the C struct struct Reading { uint8_t id; uint16_t value; int32_t time; } in two versions (natural alignment and packed), print the sizes and the offsets of each field (Reading.value.offset), and unpack a 7-byte buffer in big-endian order.
Write sha256_file(path, chunk=65536) that hashes a big file without loading it all, compare it with hashlib.file_digest (Python 3.11+), and write verify(path, expected) using hmac.compare_digest.
Use ast to write a function that lists the names of all functions and classes defined in a .py file, and the names of the modules it imports, without running it.
Predict first, then run, and explain each result in a comment:
python
import json, sqlite3, weakref, gc, zlib, argparse

print(json.dumps({1: (1, 2), "k": None, "s": {"a"} and "x"}))
print(json.loads(json.dumps([1.0, True, "é"]), parse_float=str))

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (a INTEGER UNIQUE)")
try:
    with conn:
        conn.execute("INSERT INTO t VALUES (1)")
        conn.execute("INSERT INTO t VALUES (1)")
except sqlite3.IntegrityError:
    pass
print(conn.execute("SELECT COUNT(*) FROM t").fetchone())

class K: pass
k = K()
r = weakref.ref(k)
k2 = k
del k
print(r() is k2)
del k2
gc.collect()
print(r())

print(zlib.decompress(zlib.compress(b"ab" * 50)) == b"ab" * 50)

p = argparse.ArgumentParser()
p.add_argument("-v", action="count", default=0)
p.add_argument("names", nargs="*")
print(p.parse_args(["-vv", "a", "b"]))
import os

# THE THREE STEPS: open -> read or write -> close
# open(path, mode="r", encoding=None)
#
#   mode  meaning
#   "r"   read (default); the file must exist
#   "w"   write; creates the file, or EMPTIES it if it exists
#   "a"   append; creates the file, or adds to the end
#   "x"   create; fails if the file already exists
#   "+"   add reading AND writing: "r+", "w+", "a+"
#   "t"   text mode (default)
#   "b"   binary mode: "rb", "wb", "ab"

# 1. open() and close()
f = open("hello.txt", "w", encoding="utf-8")
f.write("Hello, file!")
f.close()
print(f.closed)                              # True

f = open("hello.txt", "r", encoding="utf-8")
print(f.read())                              # Hello, file!
f.close()

# 2. The with statement closes the file for you (the standard way)
with open("hello.txt", encoding="utf-8") as f:
    text = f.read()
print(text, f.closed)                        # Hello, file! True

# 3. Errors
try:
    open("missing.txt", encoding="utf-8")
except FileNotFoundError as e:
    print(type(e).__name__, e.filename)      # FileNotFoundError missing.txt

try:
    open("hello.txt", "x", encoding="utf-8")
except FileExistsError as e:
    print(type(e).__name__)                  # FileExistsError

# 4. A closed file cannot be used
try:
    f.read()
except ValueError as e:
    print(e)                                 # I/O operation on closed file.

# 5. Information about a file object
with open("hello.txt", encoding="utf-8") as f:
    print(f.name, f.mode, f.encoding, f.closed)     # hello.txt r utf-8 False
    print(type(f))                           # <class '_io.TextIOWrapper'>

# 6. Binary mode gives bytes, text mode gives str
with open("hello.txt", "rb") as f:
    print(f.read())                          # b'Hello, file!'

# 7. with closes the file even when an error happens inside
try:
    with open("hello.txt", encoding="utf-8") as f:
        raise ValueError("boom")
except ValueError:
    print(f.closed)                          # True

os.remove("hello.txt")
import json
import os


def show(path):
    """Print the exact content of a text file (repr shows the \\n characters)."""
    with open(path, encoding="utf-8") as f:
        print(repr(f.read()))


# 1. "w": create the file, or EMPTY it
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("First line\n")             # write() does NOT add a newline
    f.write("Second line\n")
    n = f.write("Third")
    print(n)                            # 5     write() returns the number of characters
show("notes.txt")                       # 'First line\nSecond line\nThird'

# 2. "a": add to the end
with open("notes.txt", "a", encoding="utf-8") as f:
    f.write("\nFourth")
show("notes.txt")                       # 'First line\nSecond line\nThird\nFourth'

# 3. "w" again: everything is replaced
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("Only this")
show("notes.txt")                       # 'Only this'

# 4. writelines(): a list of strings (it does NOT add newlines either)
with open("lines.txt", "w", encoding="utf-8") as f:
    f.writelines(["a\n", "b\n", "c\n"])
show("lines.txt")                       # 'a\nb\nc\n'

# 5. print(..., file=f) adds spaces and the newline for you
with open("p.txt", "w", encoding="utf-8") as f:
    print("hello", 42, file=f)
    print("world", file=f)
show("p.txt")                           # 'hello 42\nworld\n'

# 6. Writing in a loop
with open("squares.csv", "w", encoding="utf-8") as f:
    f.write("n,square\n")
    for i in range(1, 4):
        f.write(f"{i},{i * i}\n")
show("squares.csv")                     # 'n,square\n1,1\n2,4\n3,9\n'

# 7. "r+": read AND write, starting at position 0 (the file must exist)
with open("rw.txt", "w", encoding="utf-8") as f:
    f.write("Hello")
with open("rw.txt", "r+", encoding="utf-8") as f:
    f.write("J")
show("rw.txt")                          # 'Jello'

# 8. "x": create, fail if the file exists
try:
    open("rw.txt", "x", encoding="utf-8")
except FileExistsError:
    print("rw.txt already exists")      # rw.txt already exists

# 9. write() accepts ONLY a string in text mode
try:
    with open("bad.txt", "w", encoding="utf-8") as f:
        f.write(123)
except TypeError as e:
    print(type(e).__name__)             # TypeError
with open("bad.txt", "w", encoding="utf-8") as f:
    f.write(str(123))                   # convert first
show("bad.txt")                         # '123'

# 10. Binary mode writes BYTES
with open("data.bin", "wb") as f:
    f.write(bytes([1, 2, 3]))
    f.write(b"\xff")
with open("data.bin", "rb") as f:
    print(f.read())                     # b'\x01\x02\x03\xff'

try:
    with open("data.bin", "wb") as f:
        f.write("text")
except TypeError as e:
    print(type(e).__name__)             # TypeError

# 11. UTF-8: characters and bytes are different things
with open("cafe.txt", "w", encoding="utf-8") as f:
    f.write("café")
with open("cafe.txt", "rb") as f:
    raw = f.read()
print(raw, len("café"), len(raw))      # b'caf\xc3\xa9' 4 5

# 12. JSON: save a dictionary
data = {"name": "Ann", "scores": [90, 85]}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
show("data.json")
# '{\n  "name": "Ann",\n  "scores": [\n    90,\n    85\n  ]\n}'
with open("data.json", encoding="utf-8") as f:
    print(json.load(f))                 # {'name': 'Ann', 'scores': [90, 85]}

# Cleanup
for name in ["notes.txt", "lines.txt", "p.txt", "squares.csv", "rw.txt",
             "bad.txt", "data.bin", "cafe.txt", "data.json"]:
    os.remove(name)
import os
from itertools import islice
from pathlib import Path

# Prepare a sample file
with open("poem.txt", "w", encoding="utf-8") as f:
    f.write("line one\nline two\nline three\nline four\n")

# 1. read(): the whole file as one string
with open("poem.txt", encoding="utf-8") as f:
    print(repr(f.read()))           # 'line one\nline two\nline three\nline four\n'

# 2. read(n): the next n characters
with open("poem.txt", encoding="utf-8") as f:
    print(repr(f.read(4)))          # 'line'
    print(repr(f.read(5)))          # ' one\n'     (continues where it stopped)

# 3. readline(): one line at a time ('' at the end of the file)
with open("poem.txt", encoding="utf-8") as f:
    print(repr(f.readline()))       # 'line one\n'
    print(repr(f.readline()))       # 'line two\n'

# 4. readlines(): a list of all lines (newlines included)
with open("poem.txt", encoding="utf-8") as f:
    print(f.readlines())
    # ['line one\n', 'line two\n', 'line three\n', 'line four\n']

# 5. Loop over the file object: one line at a time, memory friendly
with open("poem.txt", encoding="utf-8") as f:
    for line in f:
        print(line.rstrip("\n"))
# line one
# line two
# line three
# line four

# 6. Line numbers
with open("poem.txt", encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        print(f"{number}: {line.strip()}")
# 1: line one
# 2: line two
# 3: line three
# 4: line four

# 7. Lines without the newline
with open("poem.txt", encoding="utf-8") as f:
    print(f.read().splitlines())
    # ['line one', 'line two', 'line three', 'line four']

# 8. After the end, read() returns an empty string
with open("poem.txt", encoding="utf-8") as f:
    f.read()
    print(repr(f.read()))           # ''

# 9. Count lines and words
with open("poem.txt", encoding="utf-8") as f:
    text = f.read()
print(len(text.splitlines()), len(text.split()))        # 4 8

# 10. Search
with open("poem.txt", encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        if "three" in line:
            print(number, line.strip())                 # 3 line three

# 11. The first n lines
with open("poem.txt", encoding="utf-8") as f:
    print(list(islice(f, 2)))       # ['line one\n', 'line two\n']

# 12. The last line
with open("poem.txt", encoding="utf-8") as f:
    print(f.read().splitlines()[-1])                    # line four

# 13. Binary files in chunks
with open("blob.bin", "wb") as f:
    f.write(bytes(range(10)))

chunks = []
with open("blob.bin", "rb") as f:
    while chunk := f.read(4):
        chunks.append(chunk)
print(chunks)       # [b'\x00\x01\x02\x03', b'\x04\x05\x06\x07', b'\x08\t']

# 14. A missing file
try:
    with open("nope.txt", encoding="utf-8") as f:
        f.read()
except FileNotFoundError:
    print("file not found")         # file not found

# 15. pathlib: read in one line
print(len(Path("poem.txt").read_text(encoding="utf-8").splitlines()))   # 4

os.remove("poem.txt")
os.remove("blob.bin")
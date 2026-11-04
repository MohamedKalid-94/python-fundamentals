import os
from io import BytesIO, StringIO

# --- seek() and tell(): the position inside the file (bytes, like fseek and ftell) ---
with open("m.bin", "wb") as f:
    f.write(b"0123456789")

with open("m.bin", "rb") as f:
    print(f.tell())                     # 0
    print(f.read(3))                    # b'012'
    print(f.tell())                     # 3
    f.seek(7)                           # absolute position
    print(f.read(2))                    # b'78'
    f.seek(-2, 2)                       # 2 bytes before the END  (whence: 0 start, 1 current, 2 end)
    print(f.read())                     # b'89'
    f.seek(2)
    f.seek(2, 1)                        # 2 bytes forward from the CURRENT position
    print(f.tell())                     # 4
    f.seek(0)
    print(f.readline())                 # b'0123456789'
    print(f.read())                     # b''       end of the file
    print(f.readable(), f.writable(), f.seekable())     # True False True
    print(isinstance(f.fileno(), int))  # True      the operating system's file descriptor

# --- truncate(): cut the file to a size ---
with open("m.bin", "r+b") as f:
    f.truncate(4)
    f.seek(0)
    print(f.read())                     # b'0123'

# --- Text mode: only simple seeks are allowed ---
with open("t.txt", "w", encoding="utf-8") as f:
    print(f.readable(), f.writable())   # False True
    f.write("0123456789")

with open("t.txt", encoding="utf-8") as f:
    f.seek(0, 2)                        # to the end
    print(f.tell())                     # 10
    f.seek(0)
    print(f.read(3))                    # 012

# --- flush(): push the buffered data to the file now ---
f = open("buf.bin", "wb")
f.write(b"hello")
print(os.path.getsize("buf.bin"))       # 0       still waiting in the buffer
f.flush()
print(os.path.getsize("buf.bin"))       # 5
f.close()                               # close() also flushes

# --- writelines(), readlines(), next() ---
with open("l.txt", "w", encoding="utf-8") as f:
    f.writelines(["a\n", "b\n"])
with open("l.txt", encoding="utf-8") as f:
    print(f.readlines())                # ['a\n', 'b\n']
with open("l.txt", encoding="utf-8") as f:
    print(repr(next(f)))                # 'a\n'

# --- In-memory files: StringIO (text) and BytesIO (bytes) behave like real files ---
buf = StringIO()
buf.write("hi\n")
buf.write("there\n")
print(repr(buf.getvalue()))             # 'hi\nthere\n'
buf.seek(0)
print(repr(buf.readline()))             # 'hi\n'

for line in StringIO("a\nb\n"):
    print(line.strip())
# a
# b

print(BytesIO(b"abc").read(2))          # b'ab'

for name in ["m.bin", "t.txt", "buf.bin", "l.txt"]:
    os.remove(name)
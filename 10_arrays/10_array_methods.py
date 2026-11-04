import os
from array import array

a = array("i", [3, 1, 2, 3])

# Searching and counting
print(a.count(3), a.index(3))               # 2 0

# Attributes
print(a.typecode, a.itemsize)               # i 4
print(a.buffer_info()[1])                   # 4        number of items

# append, extend, insert, remove, pop, reverse: see the earlier files
a.reverse()
print(a)                                    # array('i', [3, 2, 1, 3])

# tolist() and fromlist()
print(a.tolist())                           # [3, 2, 1, 3]
b = array("i")
b.fromlist([7, 8])
print(b)                                    # array('i', [7, 8])

# tobytes() and frombytes(): the raw memory (like memcpy to a buffer)
raw = array("B", [1, 2, 255]).tobytes()
print(raw)                                  # b'\x01\x02\xff'
x = array("B")
x.frombytes(raw)
print(x)                                    # array('B', [1, 2, 255])

# byteswap(): change the endianness of every item
h = array("H", [1, 256])
h.byteswap()
print(h)                                    # array('H', [256, 1])

# The same idea with plain integers
print((258).to_bytes(2, "big"), (258).to_bytes(2, "little"))   # b'\x01\x02' b'\x02\x01'
print(int.from_bytes(b"\x01\x02", "big"), int.from_bytes(b"\x01\x02", "little"))   # 258 513

# tofile() and fromfile(): binary files (file handling is covered in Module 11)
packet = array("B", [1, 2, 3, 250])
with open("demo.bin", "wb") as f:
    packet.tofile(f)

loaded = array("B")
with open("demo.bin", "rb") as f:
    loaded.fromfile(f, 4)
print(loaded)                               # array('B', [1, 2, 3, 250])
os.remove("demo.bin")

# fromunicode() and tounicode() exist for the 'u' (wide character) typecode,
# which is deprecated: use str, bytes or bytearray for text instead.

# Built-in functions
n = array("i", [4, 8, 1])
print(len(n), sum(n), min(n), max(n))       # 3 13 1 8
print(sorted(n), list(enumerate(n)))        # [1, 4, 8] [(0, 4), (1, 8), (2, 1)]
print(any(n), all(n))                       # True True
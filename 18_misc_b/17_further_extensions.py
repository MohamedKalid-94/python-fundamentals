import ctypes
import subprocess
import sys

# "Extending Python" means using code written in OTHER languages (mostly C) from Python.
# The easiest way needs no compiler: ctypes.

# 1. Describe C data types and structs
class Padded(ctypes.Structure):
    _fields_ = [("a", ctypes.c_uint8), ("b", ctypes.c_uint32)]

class Packed(ctypes.Structure):
    _pack_ = 1                                  # like __attribute__((packed))
    _fields_ = [("a", ctypes.c_uint8), ("b", ctypes.c_uint32)]

print(ctypes.sizeof(Padded), ctypes.sizeof(Packed))             # 8 5       padding, as in C
print(ctypes.sizeof(ctypes.c_int16), ctypes.sizeof(ctypes.c_double))    # 2 8

# 2. A binary header with a fixed byte order
class Header(ctypes.BigEndianStructure):        # LittleEndianStructure also exists
    _pack_ = 1
    _fields_ = [("version", ctypes.c_uint8),
                ("flags", ctypes.c_uint8),
                ("length", ctypes.c_uint16)]

h = Header.from_buffer_copy(b"\x01\x02\x00\x10")
print(h.version, h.flags, h.length)             # 1 2 16
print(bytes(h))                                 # b'\x01\x02\x00\x10'
h.length = 258
print(bytes(h).hex())                           # 01020102

# 3. Arrays, buffers, pointers
numbers = (ctypes.c_int * 3)(1, 2, 3)
print(list(numbers), ctypes.sizeof(numbers))    # [1, 2, 3] 12
buf = ctypes.create_string_buffer(b"abc", 8)
print(buf.value, buf.raw)                       # b'abc' b'abc\x00\x00\x00\x00\x00'
x = ctypes.c_int(5)
pointer = ctypes.pointer(x)
pointer.contents.value = 9
print(x.value)                                  # 9

# 4. Call a function of the C library
if sys.platform == "win32":
    libc = ctypes.cdll.msvcrt
else:
    libc = ctypes.CDLL(None)                    # the C library already loaded in the Python process
print(libc.abs(-5), libc.strlen(b"hello"))      # 5 5

# 5. Let C call YOUR Python function (a callback): qsort with a Python comparison
CMP = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

def compare(a, b):
    return a[0] - b[0]

values = (ctypes.c_int * 5)(5, 1, 4, 2, 3)
libc.qsort(values, len(values), ctypes.sizeof(ctypes.c_int), CMP(compare))
print(list(values))                             # [1, 2, 3, 4, 5]
# For other libraries:  lib = ctypes.CDLL("./mylib.so")  (".dll" on Windows)
#   lib.my_function.argtypes = [ctypes.c_int, ctypes.c_double]
#   lib.my_function.restype = ctypes.c_double
# ALWAYS set argtypes and restype: the defaults assume int and can corrupt values.

# 6. memoryview: look at the same memory without copying (the "buffer protocol")
raw = bytearray(b"abcd")
view = memoryview(raw)
view[0] = 65
print(bytes(raw), bytes(view[1:3]))             # b'Abcd' b'bc'

# 7. Run another program and read its output
result = subprocess.run([sys.executable, "-c", "print('hi')"], capture_output=True, text=True)
print(repr(result.stdout), result.returncode)   # 'hi\n' 0
# subprocess.run(["gcc", "main.c", "-o", "main"], check=True)   check=True raises an error if it fails
# Never build the command from user text with shell=True.

# HOW PEOPLE EXTEND PYTHON
#   ctypes          call a C library or DLL with no compiler (this file)
#   cffi            like ctypes, but reads C declarations
#   Cython          Python-like code compiled to C: big speed-ups for loops
#   C extension     write a module in C with Python.h (see 17_c_extension_notes.md)
#   pybind11 / nanobind   C++ classes and functions as Python modules
#   PyO3 / maturin  the same in Rust
#   NumPy, Numba    numeric speed without writing C yourself
#   Embedding       the reverse: run Python INSIDE a C program (Py_Initialize)
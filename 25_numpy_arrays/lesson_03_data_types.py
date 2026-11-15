import numpy as np

# DATA TYPES (dtype)
#   bool          np.bool_          True or False (1 byte)
#   signed int    int8 int16 int32 int64        unsigned: uint8 uint16 uint32 uint64 (no negative numbers)
#   float         float16 float32 float64       (float64 = Python float, the default)
#   complex       complex64 complex128
#   text          '<U5' = Unicode text, up to 5 characters        bytes 'S5'
#   time          datetime64, timedelta64 (Module 28)
#   Defaults: Python int -> int64, Python float -> float64 (NumPy 2, also on Windows).
# Character codes: 'i4' = int32, 'f8' = float64, 'u1' = uint8, '<' little endian, '>' big endian.

a = np.array([1, 2, 3], dtype=np.int8)
b = np.array([1, 2, 3], dtype="f4")
print(a.dtype, a.itemsize, b.dtype, b.itemsize)
print(np.dtype("<u2"), np.dtype(">u2"), np.dtype("<u2").itemsize)

# Change the type with astype: it always returns a COPY
c = np.array([1.9, -1.9, 2.5])
print(c.astype(int), c.astype(np.float32), c.astype(bool))        # int truncates toward zero
print(np.array(["1", "2.5"]).astype(float))

# Limits
print(np.iinfo(np.uint8).min, np.iinfo(np.uint8).max, np.iinfo(np.int16).max)
print(np.finfo(np.float32).eps, np.finfo(np.float64).eps)

# OVERFLOW: integers WRAP AROUND silently (a classic embedded bug, now in Python)
samples = np.array([250, 255], dtype=np.uint8)
print(samples + 10)                         # 260 -> 4, 265 -> 9
print(np.array([127], dtype=np.int8) + 1)   # -128
try:
    samples + 300                           # 300 does not fit in uint8
except OverflowError as error:
    print("OverflowError:", error)
print(samples.astype(np.uint16) + 10)       # widen first, then calculate

# PROMOTION: mixing types gives the type that can hold both
print(np.result_type(np.int8, np.uint8), np.result_type(np.int32, np.float32), np.result_type(np.int64, np.float32))
print((np.array([1, 2], dtype=np.int8) + np.array([1, 2], dtype=np.int16)).dtype)
print((np.array([1, 2], dtype=np.float32) * 2.5).dtype)      # a Python float does not widen float32

# FLOATS ARE APPROXIMATE
print(float(np.float16(0.1)), float(np.float32(0.1)))
print(0.1 + 0.2 == 0.3, np.isclose(0.1 + 0.2, 0.3))
print(np.can_cast(np.int64, np.float32), np.can_cast(np.int8, np.int16))

# EXPECTED OUTPUT
# int8 1 float32 4
# uint16 >u2 2
# [ 1 -1  2] [ 1.9 -1.9  2.5] [ True  True  True]
# [1.  2.5]
# 0 255 32767
# 1.1920929e-07 2.220446049250313e-16
# [4 9]
# [-128]
# OverflowError: Python integer 300 out of bounds for uint8
# [260 265]
# int16 float64 float64
# int16
# float32
# 0.0999755859375 0.10000000149011612
# False True
# False True
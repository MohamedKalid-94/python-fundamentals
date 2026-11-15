import struct

import numpy as np

# ARRAYS FROM EXISTING DATA
#   np.array(obj)        always COPIES (lists, tuples, nested lists, other arrays)
#   np.asarray(obj)      does NOT copy if obj is already an array with the right dtype
#   np.frombuffer(buf)   a VIEW on bytes: no copy (read-only for bytes). Perfect for sensor frames.
#   np.fromiter(it, dtype, count)   from any iterator (a generator)
#   np.copy(a)           an explicit copy         a.tolist()   back to a Python list

data = [(1, 2), (3, 4)]
print(np.array(data))
print(np.array((1, 2, 3)))

a = np.array([1, 2, 3])
print(np.asarray(a) is a, np.array(a) is a)          # asarray returns the same object, array makes a copy
print(np.asarray([1, 2, 3]).tolist())

print(np.fromiter((x * x for x in range(5)), dtype=int))
print(np.fromiter(range(10), dtype=int, count=3))

# FROM BYTES: links to Module 10 (bytes, arrays, endianness) and Module 16 (struct)
frame = struct.pack("<4H", 100, 200, 300, 65535)         # 4 unsigned 16-bit values, little endian
print(frame)
little = np.frombuffer(frame, dtype="<u2")
big = np.frombuffer(frame, dtype=">u2")                  # the same bytes read with the wrong byte order
print(little, big)
print(little.flags.writeable)                            # bytes are read-only, so is the view
editable = little.copy()
editable[0] = 1
print(editable)

# A bytearray is writable: the array and the buffer share the memory
buffer = bytearray(frame)
view = np.frombuffer(buffer, dtype="<u2")
view[0] = 1
print(buffer[:2], view[0])

# From text: np.array(line.split(), dtype=float). Files are read with loadtxt (Module 28).
print(np.array("1.5 2.5 3.5".split(), dtype=float))

# EXPECTED OUTPUT
# [[1 2]
#  [3 4]]
# [1 2 3]
# True False
# [1, 2, 3]
# [ 0  1  4  9 16]
# [0 1 2]
# b'd\x00\xc8\x00,\x01\xff\xff'
# [  100   200   300 65535] [25600 51200 11265 65535]
# False
# [    1   200   300 65535]
# bytearray(b'\x01\x00') 1
# [1.5 2.5 3.5]
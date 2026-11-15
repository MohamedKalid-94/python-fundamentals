import numpy as np

# SWAPPING AXES
#   a.swapaxes(i, j)           exchange TWO axes (a view)           np.swapaxes(a, i, j)
#   a.T                        reverse ALL axes                     np.transpose(a, axes)    any order
#   np.moveaxis(a, src, dst)   move one axis to a new position (the others keep their order)

a = np.arange(24).reshape(2, 3, 4)
print(np.swapaxes(a, 0, 2).shape, a.swapaxes(1, 2).shape)
b = np.arange(6).reshape(2, 3)
print(b.swapaxes(0, 1).tolist() == b.T.tolist())
s = b.swapaxes(0, 1)
s[0, 0] = 99
print(b[0, 0], np.shares_memory(b, s))             # swapaxes is a view
print(np.moveaxis(a, 0, -1).shape, a.transpose(2, 0, 1).shape)
batch = np.zeros((8, 32, 64, 3))                   # (images, height, width, channels)
print(np.moveaxis(batch, -1, 1).shape)             # (images, channels, height, width)

# BYTE SWAPPING: the same value stored with the bytes in the other order.
#   Data from a big-endian device (network order, many MCUs) must be read as ">", or swapped.
#   "<" little endian, ">" big endian. The numbers below assume a little-endian machine (x86 and ARM PCs).
x = np.array([1, 256, 65535], dtype="<u2")
print(x.tobytes())
y = x.byteswap()                                   # bytes swapped, the dtype label unchanged
print(y, y.dtype)                                  # the VALUES now look wrong
print(y.tobytes())
z = x.view(">u2")                                  # the SAME bytes read as big endian
print(z)
w = x.astype(">u2")                                # the same VALUES stored as big endian
print(w, w.dtype, w.tobytes())
print(x.dtype.byteorder, w.dtype.byteorder, np.dtype("u1").byteorder)    # "=" native, ">" big, "|" not applicable

# A frame from a big-endian device, read two ways
raw = bytes([0x01, 0x02, 0x03, 0x04])
wrong = np.frombuffer(raw, dtype="<u2")
right = np.frombuffer(raw, dtype=">u2")
print(wrong, right)
print(wrong.byteswap().tolist() == right.tolist())
native = right.astype(right.dtype.newbyteorder("="))     # convert to native byte order before heavy calculations
print(native.dtype, native.tolist())

# In-place swapping changes the array itself
q = np.array([1, 2], dtype="<u2")
q.byteswap(inplace=True)
print(q)

# EXPECTED OUTPUT
# (4, 3, 2) (2, 4, 3)
# True
# 99 True
# (3, 4, 2) (4, 2, 3)
# (8, 3, 32, 64)
# b'\x01\x00\x00\x01\xff\xff'
# [  256     1 65535] uint16
# b'\x00\x01\x01\x00\xff\xff'
# [  256     1 65535]
# [    1   256 65535] >u2 b'\x00\x01\x01\x00\xff\xff'
# = > |
# [ 513 1027] [258 772]
# True
# uint16 [258, 772]
# [256 512]
import numpy as np

# ARRAY ATTRIBUTES: facts about an array, available without calculating anything.
#   shape      tuple of the axis lengths        ndim     number of axes        size    number of elements
#   dtype      the element type                 itemsize bytes per element     nbytes  size * itemsize
#   strides    BYTES to step along each axis    flags    memory layout and ownership
#   T, real, imag, flat, base                   len(a) is the length of the FIRST axis
# To change a shape, make a new array with reshape; do not assign to a.shape.

a = np.arange(24, dtype=np.int32).reshape(2, 3, 4)
print(a.ndim, a.shape, a.size, a.dtype, a.itemsize, a.nbytes)
print(len(a), a.shape[0], a.shape[-1], np.shape(a), np.size(a, axis=1))
print(a.nbytes == a.size * a.itemsize)

# STRIDES: how many bytes to jump to reach the next element along each axis
print(a.strides)                                  # (48, 16, 4): 3*4*4, 4*4, 4
print(a.T.strides)                                # reversed: the same memory read in another order
print(a[:, ::2].strides, a[::-1].strides)         # steps of 2 double a stride, a reversal makes it negative
i, j, k = 1, 2, 3
offset = i * a.strides[0] + j * a.strides[1] + k * a.strides[2]
print(offset, (i * 12 + j * 4 + k) * 4)           # element [i, j, k] sits at this byte offset (pointer arithmetic)
print(a.view(np.uint8)[0, 0, :8])                 # the raw bytes of the first two elements (little endian)

# ITEMSIZE and the dtype decide the memory use
print(np.zeros(1000, dtype=np.uint8).nbytes, np.zeros(1000, dtype=np.float64).nbytes)
print(np.dtype(np.complex128).itemsize, np.dtype("U5").itemsize)

# FLAGS and BASE
print(a.flags["C_CONTIGUOUS"], a.flags["F_CONTIGUOUS"], a.flags["WRITEABLE"])
print(a.T.flags["C_CONTIGUOUS"], a.T.flags["F_CONTIGUOUS"])
owner = np.arange(6)
piece = owner[2:]
print(owner.flags["OWNDATA"], piece.flags["OWNDATA"], owner.base is None, piece.base is owner)
frozen = np.arange(3)
frozen.flags.writeable = False
try:
    frozen[0] = 1
except ValueError as error:
    print("ValueError:", error)

# real and imag, and T
z = np.array([1 + 2j, 3 - 4j])
print(z.real, z.imag, z.dtype)
print(np.arange(6).reshape(2, 3).T.shape)

# Strides make a sliding window possible WITHOUT copying
signal = np.arange(6)
windows = np.lib.stride_tricks.sliding_window_view(signal, 3)
print(windows)
print(windows.strides, windows.flags["WRITEABLE"])

# EXPECTED OUTPUT
# 3 (2, 3, 4) 24 int32 4 96
# 2 2 4 (2, 3, 4) 3
# True
# (48, 16, 4)
# (4, 16, 48)
# (48, 32, 4) (-48, 16, 4)
# 92 92
# [0 0 0 0 1 0 0 0]
# 1000 8000
# 16 20
# True False True
# False True
# True False True True
# ValueError: assignment destination is read-only
# [1. 3.] [ 2. -4.] complex128
# (3, 2)
# [[0 1 2]
#  [1 2 3]
#  [2 3 4]
#  [3 4 5]]
# (8, 8) False
import numpy as np

# THE NDARRAY OBJECT
#   ndim      number of dimensions (axes)
#   shape     tuple with the length of every axis
#   size      total number of elements
#   dtype     the type of ALL elements (one type per array)
#   itemsize  bytes per element          nbytes   total bytes
# An array has a FIXED size and ONE dtype; that is what makes it fast. A list can hold anything.

scalar = np.array(7)                         # 0-D
vector = np.array([1, 2, 3])                 # 1-D
matrix = np.array([[1, 2, 3], [4, 5, 6]])    # 2-D: 2 rows, 3 columns
cube = np.zeros((2, 3, 4))                   # 3-D: 2 blocks of 3 rows x 4 columns

for name, a in [("scalar", scalar), ("vector", vector), ("matrix", matrix), ("cube", cube)]:
    print(name, a.ndim, a.shape, a.size)

print(matrix)
print(type(matrix).__name__, matrix.dtype, matrix.itemsize, matrix.nbytes)

# One type for everything: NumPy picks the "widest" type that fits all the values
print(np.array([1, 2, 3]).dtype)             # int64
print(np.array([1, 2.5]).dtype)              # float64
print(np.array([1, True]).dtype)             # int64 (True counts as 1)
print(np.array([1, "a"]).dtype.kind)         # "U": numbers became text
print(np.array([1, 2], dtype=float))         # you can ask for a type

# minimum dimensions, and axes
print(np.array([1, 2, 3], ndmin=2).shape)    # (1, 3)
print(matrix.sum(axis=0), matrix.sum(axis=1))    # axis 0 = down the rows, axis 1 = along the columns

# Ragged lists do not make an array
try:
    np.array([[1, 2], [3]])
except ValueError as error:
    print("ValueError:", str(error)[:50])

# EXPECTED OUTPUT
# scalar 0 () 1
# vector 1 (3,) 3
# matrix 2 (2, 3) 6
# cube 3 (2, 3, 4) 24
# [[1 2 3]
#  [4 5 6]]
# ndarray int64 8 48
# int64
# float64
# int64
# U
# [1. 2.]
# (1, 3)
# [5 7 9] [ 6 15]
# ValueError: setting an array element with a sequence. The requ
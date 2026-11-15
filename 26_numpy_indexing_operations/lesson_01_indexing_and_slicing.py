import numpy as np

# INDEXING picks single elements:   a[i]   a[i, j]   (negative numbers count from the end)
# SLICING picks ranges:             a[start:stop:step]   (the stop is excluded; every part is optional)
#   a[1:4]  a[:3]  a[2:]  a[::2]  a[::-1]  a[-3:]
#   2-D: a[rows, columns], with an index or a slice in each place
#   ...  (Ellipsis) stands for "all the axes in between";   np.newaxis adds an axis
# A basic slice is a VIEW (Module 25, lesson 12): writing to it changes the original.

a = np.arange(10, 20)
print(a[0], a[-1], a[3])
print(a[2:5], a[:3], a[7:], a[::3], a[::-1])
print(a[-3:], a[1:-1], a[5:2], a[20:])          # out-of-range slices are fine and may be empty

m = np.arange(12).reshape(3, 4)
print(m)
print(m[1, 2], m[1][2], m[-1, -1])              # m[1, 2] is the normal form
print(m[1])                                     # one row
print(m[:, 1])                                  # one column
print(m[:2, 1:3])                               # a block
print(m[::2, ::2])                              # every second row and column
print(m[:, ::-1])                               # the columns in reverse order

cube = np.arange(24).reshape(2, 3, 4)
print(cube[1, 2, 3], cube[..., 0].shape, cube[0, ...].shape)
print(cube[:, 0, :].shape, cube[:, :, 1:3].shape)
print(m[np.newaxis, 1].shape, m[1, np.newaxis].shape, m[:, np.newaxis, :].shape)

# Assignment through an index or a slice
b = np.zeros(6, dtype=int)
b[1] = 5
b[3:5] = [7, 8]
b[::2] = -1
print(b)
m[:, 0] = 0
m[0] = [9, 9, 9, 9]
print(m)

# A slice is a view
part = m[1:, 1:]
part[0, 0] = 100
print(m[1, 1], np.shares_memory(m, part))

# Errors
try:
    a[10]
except IndexError as error:
    print("IndexError:", error)
try:
    m[3, 0]
except IndexError as error:
    print("IndexError:", error)

# EXPECTED OUTPUT
# 10 19 13
# [12 13 14] [10 11 12] [17 18 19] [10 13 16 19] [19 18 17 16 15 14 13 12 11 10]
# [17 18 19] [11 12 13 14 15 16 17 18] [] []
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]
# 6 6 11
# [4 5 6 7]
# [1 5 9]
# [[1 2]
#  [5 6]]
# [[ 0  2]
#  [ 8 10]]
# [[ 3  2  1  0]
#  [ 7  6  5  4]
#  [11 10  9  8]]
# 23 (2, 3) (3, 4)
# (2, 4) (2, 3, 2)
# (1, 4) (1, 4) (3, 1, 4)
# [-1  5 -1  7 -1  0]
# [[ 9  9  9  9]
#  [ 0  5  6  7]
#  [ 0  9 10 11]]
# 100 True
# IndexError: index 10 is out of bounds for axis 0 with size 10
# IndexError: index 3 is out of bounds for axis 0 with size 3
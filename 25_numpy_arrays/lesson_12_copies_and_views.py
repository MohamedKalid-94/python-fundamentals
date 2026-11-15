import numpy as np

# COPIES AND VIEWS
#   view     a NEW array object that SHARES its data with another array (a.base points to the owner)
#   copy     a NEW array with its OWN data
#   Basic slices, reshape (usually), ravel, transpose, T and view() give VIEWS.
#   Fancy indexing (a list or an integer array), boolean masks, flatten(), copy() and astype() give COPIES.
#   b = a is not a copy at all: it is a second NAME for the same array.

a = np.arange(6)
alias = a
alias[0] = 100
print(a[0], alias is a)

a = np.arange(6)
sliced = a[1:4]                       # a view
sliced[0] = 50
print(a, sliced.base is a, sliced.flags["OWNDATA"], a.flags["OWNDATA"])

copied = a[1:4].copy()
copied[0] = -1
print(a[1], np.shares_memory(a, copied))

fancy = a[[0, 2, 4]]                  # fancy indexing: a copy
fancy[0] = -9
print(a[0], np.shares_memory(a, fancy))
masked = a[a > 3]                     # a boolean mask: a copy
print(masked, np.shares_memory(a, masked))

v = a.view()
v[1] = 7
print(a[1], v.base is a)
print(a.view(np.uint8).shape, a.view(np.int32).shape)      # a view can reinterpret the same bytes

# Writing through a slice changes the original: a feature and a trap
matrix = np.arange(9).reshape(3, 3)
row = matrix[1]
row[:] = 0
print(matrix)
matrix[:, 0] = [10, 20, 30]
print(matrix)

# Be safe: copy when you need an independent array
safe = matrix[:2, :2].copy()
safe[:] = -1
print(matrix[0, 0])

# A small view keeps its big array alive: copy the small part so the big one can be freed
big = np.zeros(1_000_000)
small = big[:3].copy()
print(small.base is None, small.nbytes)

# np.shares_memory is exact, np.may_share_memory is a quick check that only compares the memory ranges
x = np.arange(10)
print(np.shares_memory(x[::2], x[1::2]), np.may_share_memory(x[::2], x[1::2]))

# EXPECTED OUTPUT
# 100 True
# [ 0 50  2  3  4  5] True False True
# 50 False
# 0 False
# [50  4  5] False
# 7 True
# (48,) (12,)
# [[0 1 2]
#  [0 0 0]
#  [6 7 8]]
# [[10  1  2]
#  [20  0  0]
#  [30  7  8]]
# 10
# True 24
# False True
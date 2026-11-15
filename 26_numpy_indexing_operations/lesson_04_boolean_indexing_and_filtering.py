import numpy as np

# BOOLEAN INDEXING: a True/False array of the same shape selects the elements where it is True.
#   a[a > 4]                  the elements that satisfy the condition (a COPY, always 1-D for a 2-D mask)
#   (cond1) & (cond2)  |  ~   combine masks. Always use PARENTHESES. Python's and / or / not do NOT work.
#   a[mask] = value           assign where the mask is True
#   np.where(cond, x, y)      choose element by element; np.where(cond) gives the positions
# Element-wise comparisons: == != < <= > >=  or  np.equal, np.less ...

a = np.array([3, 8, 1, 9, 4, 7])
mask = a > 4
print(mask, mask.dtype)
print(a[mask], a[a % 2 == 0], a[(a > 2) & (a < 8)], a[(a < 2) | (a > 8)], a[~(a > 4)])
try:
    a[(a > 2) and (a < 8)]
except ValueError as error:
    print("ValueError:", str(error)[:60])

# Assignment through a mask, and np.where
b = a.copy()
b[b > 4] = 0
print(b)
print(np.where(a > 4, a, -1))                    # a NEW array: a where the condition holds, otherwise -1
print(np.clip(a, 2, 8))

m = np.arange(12).reshape(3, 4)
print(m[m % 5 == 0])                             # a mask on a 2-D array gives a 1-D result
print(m[m[:, 0] > 3])                            # a mask over the rows: the rows whose first element is > 3
print(m[:, m[0] > 1])                            # a mask over the columns

# Comparison functions
x = np.array([1.0, 2.0, 3.0])
y = np.array([1.0, 2.5, 3.0])
print(x == y, x != y, x < y, np.equal(x, y), np.greater_equal(x, y))
print(np.array_equal(x, y), np.array_equal(x, x.copy()))
print(np.isclose(0.1 + 0.2, 0.3), np.allclose([1.0, 2.0], [1.0 + 1e-9, 2.0]))

# Counting and testing masks
print(np.any(a > 8), np.all(a > 0), (a > 4).sum(), np.count_nonzero(a > 4), (a > 4).mean())
print(np.nonzero(a > 4), np.flatnonzero(a > 4))
print(np.extract(a > 4, a), np.compress(a > 4, a))
print(np.select([a < 3, a < 8], ["low", "mid"], default="high"))

# A mask makes a COPY
d = a[a > 4]
d[0] = 0
print(a[1])

# NaN is never equal to anything, not even to itself: use isnan
n = np.array([1.0, np.nan, 3.0])
print(n == np.nan, np.isnan(n), n[~np.isnan(n)])

# EXPECTED OUTPUT
# [False  True False  True False  True] bool
# [8 9 7] [8 4] [3 4 7] [1 9] [3 1 4]
# ValueError: The truth value of an array with more than one element is am
# [3 0 1 0 4 0]
# [-1  8 -1  9 -1  7]
# [3 8 2 8 4 7]
# [ 0  5 10]
# [[ 4  5  6  7]
#  [ 8  9 10 11]]
# [[ 2  3]
#  [ 6  7]
#  [10 11]]
# [ True False  True] [False  True False] [False  True False] [ True False  True] [ True False  True]
# False True
# True True
# True True 3 3 0.5
# (array([1, 3, 5]),) [1 3 5]
# [8 9 7] [8 9 7]
# ['mid' 'high' 'low' 'high' 'mid' 'mid']
# 8
# [False False False] [False  True False] [1. 3.]
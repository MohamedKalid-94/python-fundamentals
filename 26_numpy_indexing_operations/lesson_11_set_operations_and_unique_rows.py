import numpy as np

# SET OPERATIONS on arrays (the results are SORTED and without duplicates)
#   np.unique(a)         the distinct values              (return_index, return_inverse, return_counts)
#   np.union1d(a, b)     in a OR b                        np.intersect1d(a, b)    in a AND b
#   np.setdiff1d(a, b)   in a but NOT in b                np.setxor1d(a, b)       in exactly ONE of them
#   np.isin(a, b)        a True/False array: is each element of a found in b?  (np.in1d is the old name; it is gone)

a = np.array([3, 1, 2, 3, 1])
b = np.array([2, 3, 4])
print(np.unique(a))
values, first, inverse, counts = np.unique(a, return_index=True, return_inverse=True, return_counts=True)
print(values, first, inverse, counts)
print(values[inverse].tolist() == a.tolist())            # the inverse rebuilds the original
print(np.union1d(a, b), np.intersect1d(a, b), np.setdiff1d(a, b), np.setxor1d(a, b))
print(np.isin(a, b), a[np.isin(a, b)], a[~np.isin(a, b)])
common, in_a, in_b = np.intersect1d(a, b, return_indices=True)
print(common, in_a, in_b)

# UNIQUE ROWS: unique with axis=0
rows = np.array([[1, 2], [3, 4], [1, 2], [5, 6], [3, 4]])
print(np.unique(rows, axis=0))
unique_rows, row_counts = np.unique(rows, axis=0, return_counts=True)
print(unique_rows.tolist(), row_counts)                  # every distinct row and how often it occurs
_, first_rows = np.unique(rows, axis=0, return_index=True)
print(rows[np.sort(first_rows)])                         # the unique rows in their ORIGINAL order
print(np.unique(rows, axis=1).shape)                     # unique columns

# UNION of arrays with several columns: stack, then keep the unique rows
p = np.array([[1, 2], [3, 4]])
q = np.array([[3, 4], [5, 6]])
print(np.unique(np.vstack((p, q)), axis=0))

# Text, and NaN
print(np.unique(np.array(["b", "a", "b"])), np.unique([np.nan, 1, np.nan]))

# Finding the duplicated values
vals, cnt = np.unique(a, return_counts=True)
print(vals[cnt > 1])

# Is one array a subset of another?
print(np.isin([1, 2], a).all(), np.isin([1, 9], a).all())

# EXPECTED OUTPUT
# [1 2 3]
# [1 2 3] [1 2 0] [2 0 1 2 0] [2 1 2]
# True
# [1 2 3 4] [2 3] [1] [1 4]
# [ True False  True  True False] [3 2 3] [1 1]
# [2 3] [2 0] [0 1]
# [[1 2]
#  [3 4]
#  [5 6]]
# [[1, 2], [3, 4], [5, 6]] [2 2 1]
# [[1 2]
#  [3 4]
#  [5 6]]
# (5, 2)
# [[1 2]
#  [3 4]
#  [5 6]]
# ['a' 'b'] [ 1. nan]
# [1 3]
# True False
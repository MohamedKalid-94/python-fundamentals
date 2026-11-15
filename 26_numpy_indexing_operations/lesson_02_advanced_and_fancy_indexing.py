import numpy as np

# ADVANCED (FANCY) INDEXING: use a LIST or an ARRAY of positions instead of a slice.
#   a[[0, 2, 4]]            the elements at those positions, in that order, repeats allowed
#   a[index_array]          the result has the SHAPE of the index array
#   m[[0, 2], [1, 3]]       two index lists are taken as PAIRS: (0, 1) and (2, 3)
#   m[np.ix_(rows, cols)]   the rows x columns block
# Fancy indexing always makes a COPY (a basic slice makes a view).

a = np.array([10, 20, 30, 40, 50])
print(a[[0, 2, 4]], a[[-1, -2]], a[[1, 1, 1]])           # repeats are allowed
index = np.array([[0, 1], [3, 4]])
print(a[index])                                          # the result has the shape of the index array

m = np.arange(12).reshape(3, 4)
print(m[[0, 2]])                                         # rows 0 and 2
print(m[:, [0, 3]])                                      # columns 0 and 3
print(m[[0, 1, 2], [1, 2, 3]])                           # PAIRS: (0,1) (1,2) (2,3)
print(m[[0, 2]][:, [1, 3]])                              # a sub-matrix, in two steps
print(m[np.ix_([0, 2], [1, 3])])                         # the same in one step (rows x columns)
print(m[[0, 1], 1:3])                                    # a list mixed with a slice

# Fancy indexing makes a COPY
c = a[[0, 1]]
c[0] = 0
print(a[0], np.shares_memory(a, c))

# Assignment with fancy indexing
b = np.zeros(5, dtype=int)
b[[0, 2, 4]] = [1, 2, 3]
b[[1, 1]] = [8, 9]                                       # the same position twice: the last value wins
print(b)

# Repeated positions with +=: the plain form counts a repeat only ONCE
counts = np.zeros(3, dtype=int)
counts[[0, 0, 1]] += 1
print(counts)
counts = np.zeros(3, dtype=int)
np.add.at(counts, [0, 0, 1], 1)                          # every repeat counts
print(counts)
print(np.bincount([0, 0, 1], minlength=3))               # the fast way to count

# take, put and friends
print(np.take(a, [4, 0]), np.take(m, [0, 5], axis=None))
p = np.zeros(4, dtype=int)
np.put(p, [1, 3], [7, 9])
print(p)
print(m[np.arange(3), m.argmax(axis=1)])                 # the largest element of every row
print(np.take_along_axis(m, np.array([[3], [0], [1]]), axis=1).ravel())

# Out-of-range positions are an error
try:
    a[[0, 9]]
except IndexError as error:
    print("IndexError:", error)

# EXPECTED OUTPUT
# [10 30 50] [50 40] [20 20 20]
# [[10 20]
#  [40 50]]
# [[ 0  1  2  3]
#  [ 8  9 10 11]]
# [[ 0  3]
#  [ 4  7]
#  [ 8 11]]
# [ 1  6 11]
# [[ 1  3]
#  [ 9 11]]
# [[ 1  3]
#  [ 9 11]]
# [[1 2]
#  [5 6]]
# 10 False
# [1 9 2 0 3]
# [1 1 0]
# [2 1 0]
# [2 1 0]
# [50 10] [0 5]
# [0 7 0 9]
# [ 3  7 11]
# [3 4 9]
# IndexError: index 9 is out of bounds for axis 0 with size 5
import numpy as np

# SORTING                                    SEARCHING                         COUNTING
#   np.sort(a, axis)  a sorted COPY            np.argmax / np.argmin             np.count_nonzero(mask)
#   a.sort()          sorts IN PLACE           np.where(cond)  positions         mask.sum()
#   np.argsort(a)     the ORDER (indices)      np.nonzero  np.flatnonzero        np.bincount(ints)
#   np.lexsort(keys)  several keys, LAST first np.searchsorted(sorted, values)   np.unique(a, return_counts=True)
#   np.partition      the k smallest only      np.isin(a, values)
# Sorting is ascending. For descending order use [::-1] or sort the negative values.

a = np.array([30, 10, 20, 10, 40])
print(np.sort(a), a, np.sort(a)[::-1])                   # np.sort returns a sorted COPY
a2 = a.copy()
a2.sort()
print(a2)                                                # in place
order = np.argsort(a, kind="stable")                     # stable: equal elements keep their original order
print(order, a[order])                                   # (the default sort does not promise this for ties)
print(np.argsort(-a, kind="stable"))                     # descending order: sort the negative values

# Sorting with fancy indexing: reorder ANOTHER array by the order of this one
names = np.array(["c", "a", "b", "d", "e"])
print(names[np.argsort(a, kind="stable")])

# Sorting along an axis
m = np.array([[3, 1, 2], [9, 7, 8], [6, 4, 5]])
print(np.sort(m, axis=1))                                # every row sorted
print(np.sort(m, axis=0))                                # every column sorted
print(np.sort(m, axis=None))                             # everything, flattened
print(m[np.argsort(m[:, 0])[::-1]])                      # rows ordered by the first column, descending

# lexsort: the LAST key is the main key
last = np.array(["Smith", "Jones", "Smith", "Jones"])
first = np.array(["Bo", "Cy", "Al", "Al"])
print(np.lexsort((first, last)))                         # by last name, then by first name
print(last[np.lexsort((first, last))], first[np.lexsort((first, last))])

# Partial sorting: the k smallest or largest, without sorting everything
big = np.array([9, 4, 7, 1, 8, 2])
print(np.sort(np.partition(big, 2)[:3]))                 # the 3 smallest
print(np.sort(big[np.argpartition(big, -2)[-2:]]))       # the 2 largest

# SEARCHING
print(np.argmax(a), np.argmin(a), a.max(), a.min())      # the FIRST position of a repeated extreme
print(np.argmax(m, axis=1), np.argmax(m, axis=0))
row, column = np.unravel_index(np.argmax(m), m.shape)
print(int(row), int(column))
print(np.where(a == 10), np.where(a > 15, "big", "small"))
sorted_a = np.sort(a)
print(sorted_a, np.searchsorted(sorted_a, [5, 10, 25, 99]), np.searchsorted(sorted_a, 10, side="right"))
print(np.isin(a, [10, 40]), np.flatnonzero(np.isin(a, [10, 40])))

# COUNTING
print(np.count_nonzero(a > 15), (a == 10).sum(), np.bincount([1, 1, 3]))
print(np.unique(a, return_counts=True))
print(np.flip(a), np.flip(m, axis=0)[0])

# EXPECTED OUTPUT
# [10 10 20 30 40] [30 10 20 10 40] [40 30 20 10 10]
# [10 10 20 30 40]
# [1 3 2 0 4] [10 10 20 30 40]
# [4 0 2 1 3]
# ['a' 'd' 'b' 'c' 'e']
# [[1 2 3]
#  [7 8 9]
#  [4 5 6]]
# [[3 1 2]
#  [6 4 5]
#  [9 7 8]]
# [1 2 3 4 5 6 7 8 9]
# [[9 7 8]
#  [6 4 5]
#  [3 1 2]]
# [3 1 2 0]
# ['Jones' 'Jones' 'Smith' 'Smith'] ['Al' 'Cy' 'Al' 'Bo']
# [1 2 4]
# [8 9]
# 4 1 40 10
# [0 0 0] [1 1 1]
# 1 0
# (array([1, 3]),) ['big' 'small' 'big' 'small' 'big']
# [10 10 20 30 40] [0 0 3 5] 2
# [False  True False  True  True] [1 3 4]
# 3 2 [0 2 0 1]
# (array([10, 20, 30, 40]), array([2, 1, 1, 1]))
# [40 10 20 10 30] [6 4 5]
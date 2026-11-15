import numpy as np

# ITERATING OVER AN ARRAY
#   for row in a                  iterates over the FIRST axis (the rows of a 2-D array)
#   a.flat                        a flat iterator over ALL elements (row by row)
#   np.ndenumerate(a)             (index, value) pairs for every element
#   np.ndindex(shape)             every index tuple
#   np.nditer(a, ...)             the general iterator: order, writing, several arrays at once
# BUT: a Python loop over array elements is SLOW. Prefer whole-array operations (Modules 26 and 28).

a = np.arange(6).reshape(2, 3)
print(a)
for row in a:
    print("row", row)
for value in a.flat:
    print(value, end=" ")
print()
for index, value in np.ndenumerate(a):
    if value % 2 == 0:
        print(index, value)
print(list(np.ndindex(2, 2)))

# nditer: order and modification
for value in np.nditer(a, order="F"):               # column by column
    print(int(value), end=" ")
print()
b = a.copy()
with np.nditer(b, op_flags=["readwrite"]) as iterator:
    for element in iterator:
        element[...] = element * 10                 # [...] writes into the array
print(b)

# External loop: the iterator hands over whole chunks instead of single numbers
for chunk in np.nditer(a, flags=["external_loop"], order="F"):
    print(chunk)

# Two arrays at once (they are broadcast together)
for x, y in np.nditer([np.arange(3), np.array([10, 20, 30])]):
    print(int(x + y), end=" ")
print()

# The loop and the vectorized form give the same result
total = 0
for value in a.flat:
    total += value * value
print(total, (a * a).sum())

# EXPECTED OUTPUT
# [[0 1 2]
#  [3 4 5]]
# row [0 1 2]
# row [3 4 5]
# 0 1 2 3 4 5
# (0, 0) 0
# (0, 2) 2
# (1, 1) 4
# [(0, 0), (0, 1), (1, 0), (1, 1)]
# 0 3 1 4 2 5
# [[ 0 10 20]
#  [30 40 50]]
# [0 3]
# [1 4]
# [2 5]
# 10 21 32
# 55 55
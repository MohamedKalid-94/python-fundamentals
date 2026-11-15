import numpy as np

# ARRAY CREATION ROUTINES: make an array without typing the values
#   zeros(shape)  ones(shape)  full(shape, value)  empty(shape)  (empty = NOT initialised, contents are random)
#   eye(n)  identity(n)  diag(v)     *_like(other) copies the shape and dtype of another array
#   np.array(list)  np.asarray(x)  np.copy(x)  np.fromfunction(f, shape)
# shape is an int or a tuple. The dtype is float64 unless you ask for another one.

print(np.zeros(3))
print(np.ones((2, 3), dtype=int))
print(np.full((2, 2), 7))
print(np.full(3, 0.5))
print(np.empty((2, 3)).shape)               # only the SHAPE is meaningful
print(np.eye(3))
print(np.eye(3, 4, k=1, dtype=int))         # k shifts the diagonal
print(np.identity(2, dtype=int))
print(np.diag([1, 2, 3]))                   # a vector becomes a diagonal matrix
print(np.diag(np.arange(9).reshape(3, 3)))  # a matrix gives back its diagonal

template = np.array([[1, 2], [3, 4]], dtype=np.int16)
print(np.zeros_like(template), np.zeros_like(template).dtype)
print(np.full_like(template, 9))
print(np.ones_like(template, dtype=float))

# A function of the indices
print(np.fromfunction(lambda row, column: row * 10 + column, (3, 3), dtype=int))

# np.triu / np.tril keep the upper / lower triangle
print(np.triu(np.ones((3, 3), dtype=int)))

# ARRAY MANIPULATION (the overview from your syllabus). The groups, and where each is taught:
#   shape            reshape ravel flatten resize                       lessons 08 and 11
#   axes             transpose moveaxis expand_dims squeeze             lessons 08 and 11 (swapaxes in Module 26)
#   joining          concatenate stack vstack hstack dstack block       lesson 09
#   splitting        split array_split hsplit vsplit dsplit             lesson 10
#   adding/removing  append insert delete                               Module 26
#   rearranging      flip roll rot90 sort                               Module 26

# EXPECTED OUTPUT
# [0. 0. 0.]
# [[1 1 1]
#  [1 1 1]]
# [[7 7]
#  [7 7]]
# [0.5 0.5 0.5]
# (2, 3)
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]
# [[0 1 0 0]
#  [0 0 1 0]
#  [0 0 0 1]]
# [[1 0]
#  [0 1]]
# [[1 0 0]
#  [0 2 0]
#  [0 0 3]]
# [0 4 8]
# [[0 0]
#  [0 0]] int16
# [[9 9]
#  [9 9]]
# [[1. 1.]
#  [1. 1.]]
# [[ 0  1  2]
#  [10 11 12]
#  [20 21 22]]
# [[1 1 1]
#  [0 1 1]
#  [0 0 1]]
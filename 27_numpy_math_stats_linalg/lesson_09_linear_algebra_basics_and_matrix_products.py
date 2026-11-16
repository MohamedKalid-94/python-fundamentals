import warnings

import numpy as np

# LINEAR ALGEBRA BASICS with ordinary 2-D arrays
#   A + B, A - B       element by element (the shapes must match or broadcast)
#   A * B              element by element too (NOT the matrix product)
#   A @ B              the MATRIX PRODUCT   (np.matmul, np.dot for 2-D)       shapes (n,k) @ (k,m) -> (n,m)
#   v @ w              the dot product of two vectors       np.outer(v, w)    all products v[i] * w[j]
#   np.trace  np.linalg.matrix_power  np.einsum  np.tensordot  np.cross  np.kron
# THE MATRIX LIBRARY: np.matrix (where * means the matrix product) is old and pending removal.
# New code uses np.array and @ (shown at the end, only so you can read old code).

A = np.array([[1, 2], [3, 4]])
B = np.array([[0, 1], [1, 0]])
print(A + B)
print(A - B)
print(A * B)                                         # element by element
print(A @ B)                                         # matrix product
print(np.array_equal(A @ B, np.dot(A, B)), np.array_equal(A @ B, np.matmul(A, B)))
print(np.array_equal(A @ B, B @ A))                  # the matrix product is NOT commutative

# Vectors
v = np.array([1, 2])
w = np.array([3, 4])
print(v @ w, np.dot(v, w), np.inner(v, w), np.vdot(v, w))
print(np.outer(v, w))
print(A @ v, v @ A)                                  # matrix times vector, vector times matrix
print(np.cross([1, 0, 0], [0, 1, 0]))                # the cross product of two 3-D vectors

# Shapes: (n, k) @ (k, m) -> (n, m)
C = np.arange(6).reshape(2, 3)
D = np.arange(6).reshape(3, 2)
print((C @ D).shape, (D @ C).shape)
try:
    C @ C
except ValueError as error:
    print("ValueError:", str(error)[:60])

# Trace, powers, identity
print(np.trace(A), np.linalg.matrix_power(A, 3).tolist(), np.linalg.matrix_power(A, 0).tolist())
print(np.array_equal(np.eye(2, dtype=int) @ A, A))

# Batches: matmul multiplies a whole stack of matrices at once
stack = np.arange(8).reshape(2, 2, 2)
print((stack @ np.eye(2)).shape, np.matmul(stack, stack).shape)

# einsum: write the sums with index letters
print(np.array_equal(np.einsum("ij,jk->ik", A, B), A @ B), np.einsum("i,i->", v, w), np.einsum("ii->", A))
print(np.tensordot(A, B, axes=1).tolist() == (A @ B).tolist())

# Element-wise matrix operations
print(A ** 2, np.sqrt(A.astype(float)).round(3), np.maximum(A, 2))
print(A.T, A.T @ A)

# Linear maps: rotate points by 90 degrees (2-D rotation matrix)
angle = np.pi / 2
R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
points = np.array([[1.0, 0.0], [0.0, 2.0]])
print(np.round(points @ R.T, 6) + 0.0)

# The legacy np.matrix, for reading old code only
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    M = np.matrix([[1, 2], [3, 4]])
print(type(M).__name__, caught[0].category.__name__)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    print(M * M)                                     # the MATRIX product here...
    print(M.I.round(2))
print(A * A)                                         # ...but the element-wise product for an array

# EXPECTED OUTPUT
# [[1 3]
#  [4 4]]
# [[1 1]
#  [2 4]]
# [[0 2]
#  [3 0]]
# [[2 1]
#  [4 3]]
# True True
# False
# 11 11 11 11
# [[3 4]
#  [6 8]]
# [ 5 11] [ 7 10]
# [0 0 1]
# (2, 2) (3, 3)
# ValueError: matmul: Input operand 1 has a mismatch in its core dimension
# 5 [[37, 54], [81, 118]] [[1, 0], [0, 1]]
# True
# (2, 2, 2) (2, 2, 2)
# True 11 5
# True
# [[ 1  4]
#  [ 9 16]] [[1.    1.414]
#  [1.732 2.   ]] [[2 2]
#  [3 4]]
# [[1 3]
#  [2 4]] [[10 14]
#  [14 20]]
# [[ 0.  1.]
#  [-2.  0.]]
# matrix PendingDeprecationWarning
# [[ 7 10]
#  [15 22]]
# [[-2.   1. ]
#  [ 1.5 -0.5]]
# [[ 1  4]
#  [ 9 16]]
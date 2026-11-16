import numpy as np

# np.linalg: the linear algebra toolbox
#   inv(A)  det(A)  matrix_rank(A)  cond(A)  pinv(A)          solve(A, b)  lstsq(A, b)
#   eig(A) eigvals(A)  eigh(S) eigvalsh(S) (symmetric matrices, sorted values)      svd(A)
#   norm(x, ord)         vector and matrix norms
#   LinAlgError          raised for a singular matrix
# Eigenvectors and the U and V of an SVD are only defined up to a SIGN, so this lesson checks them
# with equations instead of printing them.

A = np.array([[4.0, 7.0], [2.0, 6.0]])
inverse = np.linalg.inv(A)
print(np.round(inverse, 3), np.allclose(A @ inverse, np.eye(2)))
print(np.round(np.linalg.det(A), 6), np.linalg.matrix_rank(A), np.round(np.linalg.cond(A), 4))

# DETERMINANT and a singular matrix (the rows are dependent: no inverse)
S = np.array([[1.0, 2.0], [2.0, 4.0]])
print(np.round(np.linalg.det(S), 6) + 0.0, np.linalg.matrix_rank(S))
try:
    np.linalg.inv(S)
except np.linalg.LinAlgError as error:
    print("LinAlgError:", error)
print(np.round(np.linalg.pinv(S), 3))                # the pseudo-inverse always exists

# SOLVING LINEAR EQUATIONS:  2x + y = 5  and  x + 3y = 10
coefficients = np.array([[2.0, 1.0], [1.0, 3.0]])
constants = np.array([5.0, 10.0])
solution = np.linalg.solve(coefficients, constants)
print(solution, np.allclose(coefficients @ solution, constants))
# solve is faster and more accurate than inv(A) @ b: prefer it

# EIGENVALUES and EIGENVECTORS:  A v = lambda v
sym = np.array([[2.0, 1.0], [1.0, 2.0]])
values, vectors = np.linalg.eigh(sym)                 # for symmetric matrices: sorted, real
print(values, np.round(np.abs(vectors), 4))
print(all(np.allclose(sym @ vectors[:, i], values[i] * vectors[:, i]) for i in range(2)))
general = np.array([[2.0, 0.0], [1.0, 3.0]])
print(np.sort(np.linalg.eigvals(general).real))
rotation = np.array([[0.0, -1.0], [1.0, 0.0]])        # a 90-degree rotation: complex eigenvalues
print(np.sort_complex(np.linalg.eigvals(rotation)))
print(np.round(np.linalg.eigvals(np.array([[1.0, 2.0], [3.0, 4.0]])).real.sum(), 6), np.trace(np.array([[1, 2], [3, 4]])))

# SINGULAR VALUE DECOMPOSITION:  M = U * diag(s) * Vt
M = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
U, s, Vt = np.linalg.svd(M, full_matrices=False)
print(U.shape, s.shape, Vt.shape, np.round(s, 4))
print(np.allclose(U * s @ Vt, M))                     # rebuild M from the three parts
rank1 = s[0] * np.outer(U[:, 0], Vt[0])               # the best rank-1 approximation
print(np.round(np.linalg.norm(M - rank1), 4), np.round(s[1], 4))     # the error equals the next singular value

# NORMS
v = np.array([3.0, 4.0])
print(np.linalg.norm(v), np.linalg.norm(v, 1), np.linalg.norm(v, np.inf))      # L2, L1, maximum
W = np.array([[1.0, 2.0], [3.0, 4.0]])
print(np.round(np.linalg.norm(W), 4), np.linalg.norm(W, 1), np.linalg.norm(W, np.inf))   # Frobenius, max column sum, max row sum
print(np.round(np.linalg.norm(W, 2), 4), np.round(np.linalg.norm(W, "nuc"), 4))          # largest singular value, nuclear

# LEAST SQUARES: the best line y = slope * x + intercept through noisy points
x = np.array([0.0, 1.0, 2.0, 3.0])
y = np.array([1.1, 2.9, 5.2, 6.8])
design = np.column_stack((x, np.ones_like(x)))
(slope, intercept), residuals, rank, _ = np.linalg.lstsq(design, y, rcond=None)
print(np.round(slope, 3), np.round(intercept, 3), rank)

# EXPECTED OUTPUT
# [[ 0.6 -0.7]
#  [-0.2  0.4]] True
# 10.0 2 10.4039
# 0.0 1
# LinAlgError: Singular matrix
# [[0.04 0.08]
#  [0.08 0.16]]
# [1. 3.] True
# [1. 3.] [[0.7071 0.7071]
#  [0.7071 0.7071]]
# True
# [2. 3.]
# [0.-1.j 0.+1.j]
# 5.0 5
# (3, 2) (2,) (2, 2) [9.5255 0.5143]
# True
# 0.5143 0.5143
# 5.0 7.0 4.0
# 5.4772 6.0 7.0
# 5.465 5.831
# 1.94 1.09 2
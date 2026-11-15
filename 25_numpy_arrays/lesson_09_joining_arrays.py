import numpy as np

# CONCATENATING: join arrays along an EXISTING axis (all other axes must match).
# STACKING: join arrays along a NEW axis (all shapes must be equal).
#   concatenate((a, b), axis=0)   vstack = along rows (axis 0)   hstack = along columns (axis 1)
#   stack((a, b), axis=0)         a new axis                     dstack = along a third axis
#   column_stack: 1-D arrays become columns                      block: assemble from blocks
# OLD NAME: np.row_stack is gone in current NumPy: use np.vstack.

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

print(np.concatenate((a, b)))                    # axis=0 is the default
print(np.concatenate((a, b), axis=1))
print(np.concatenate((a, [[9, 9]])))             # the shapes may differ along the joining axis
print(np.concatenate((a, b), axis=None))         # flattens first

print(np.vstack((a, b)).shape, np.hstack((a, b)).shape, np.dstack((a, b)).shape)
print(np.stack((a, b)).shape, np.stack((a, b), axis=1).shape, np.stack((a, b), axis=-1).shape)

# 1-D arrays
x = np.array([1, 2, 3])
y = np.array([4, 5, 6])
print(np.vstack((x, y)))
print(np.hstack((x, y)))
print(np.column_stack((x, y)))
print(np.stack((x, y), axis=1).tolist() == np.column_stack((x, y)).tolist())

# block: put 2-D pieces together
print(np.block([[np.eye(2, dtype=int), np.zeros((2, 1), dtype=int)],
                [np.zeros((1, 2), dtype=int), np.ones((1, 1), dtype=int)]]))

# A mismatch is an error
try:
    np.concatenate((a, np.array([1, 2, 3])))
except ValueError as error:
    print("ValueError:", str(error)[:60])

# Collecting results: build a list first, join once (appending to an array in a loop copies it every time)
frames = [np.full(3, i) for i in range(3)]
print(np.stack(frames))

# EXPECTED OUTPUT
# [[1 2]
#  [3 4]
#  [5 6]
#  [7 8]]
# [[1 2 5 6]
#  [3 4 7 8]]
# [[1 2]
#  [3 4]
#  [9 9]]
# [1 2 3 4 5 6 7 8]
# (4, 2) (2, 4) (2, 2, 2)
# (2, 2, 2) (2, 2, 2) (2, 2, 2)
# [[1 2 3]
#  [4 5 6]]
# [1 2 3 4 5 6]
# [[1 4]
#  [2 5]
#  [3 6]]
# True
# [[1 0 0]
#  [0 1 0]
#  [0 0 1]]
# ValueError: all the input arrays must have same number of dimensions, bu
# [[0 0 0]
#  [1 1 1]
#  [2 2 2]]
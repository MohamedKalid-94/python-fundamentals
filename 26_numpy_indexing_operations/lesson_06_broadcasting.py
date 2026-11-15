import numpy as np

# BROADCASTING: how NumPy combines arrays of DIFFERENT shapes without copying the data.
# Compare the two shapes from the LAST axis backwards:
#   1. if the shapes have different numbers of axes, add 1s on the LEFT of the shorter one
#   2. two sizes are compatible if they are equal, or if one of them is 1
#   3. an axis of size 1 is "stretched" to the other size
#   4. otherwise: ValueError
#   (3,) with (2, 3)  -> (2, 3)        (2, 1) with (1, 3) -> (2, 3)        (3,) with (3, 1) -> (3, 3)

a = np.array([1, 2, 3])
print(a + 10)                                   # a scalar is stretched over everything
m = np.arange(6).reshape(2, 3)
print(m + a)                                    # (2, 3) + (3,)   -> (2, 3)
col = np.array([[10], [20]])
print(m + col)                                  # (2, 3) + (2, 1) -> (2, 3)
print(np.array([1, 2, 3]) * np.array([[1], [10], [100]]))     # (3,) * (3, 1) -> (3, 3): an "outer product"
print(np.broadcast_shapes((2, 3), (3,)), np.broadcast_shapes((5, 1, 4), (3, 1)))

try:
    m + np.array([1, 2])
except ValueError as error:
    print("ValueError:", error)

# The classic pitfall: a row and a column give a whole TABLE, not a vector
x = np.array([1, 2, 3])
y = np.array([[1], [2], [3]])
print((x + y).shape)

# Centering and scaling columns (a data-science staple)
data = np.array([[1.0, 100.0], [2.0, 200.0], [3.0, 300.0]])
print(data - data.mean(axis=0))                 # subtract the mean of each COLUMN
print(data / data.max(axis=0))
print(data - data.mean(axis=1, keepdims=True))  # keepdims=True keeps the (3, 1) shape so it still broadcasts

# broadcast_to gives a read-only VIEW: no data is copied (the stride is 0)
b = np.broadcast_to(a, (2, 3))
print(b.shape, b.strides, b.flags["WRITEABLE"])

# A distance table between points: (3, 1) minus (1, 3)
points = np.array([0, 2, 5])
print(np.abs(points[:, None] - points[None, :]))

# A grid of a function without meshgrid
rows = np.arange(3)[:, None]
cols = np.arange(4)[None, :]
print(rows * 10 + cols)

# 2-D points: distances between all pairs, by adding an axis
pts = np.array([[0.0, 0.0], [3.0, 4.0], [6.0, 8.0]])
diff = pts[:, None, :] - pts[None, :, :]        # (3, 1, 2) - (1, 3, 2) -> (3, 3, 2)
print(np.sqrt((diff ** 2).sum(axis=-1)))

# EXPECTED OUTPUT
# [11 12 13]
# [[1 3 5]
#  [4 6 8]]
# [[10 11 12]
#  [23 24 25]]
# [[  1   2   3]
#  [ 10  20  30]
#  [100 200 300]]
# (2, 3) (5, 3, 4)
# ValueError: operands could not be broadcast together with shapes (2,3) (2,)
# (3, 3)
# [[  -1. -100.]
#  [   0.    0.]
#  [   1.  100.]]
# [[0.33333333 0.33333333]
#  [0.66666667 0.66666667]
#  [1.         1.        ]]
# [[ -49.5   49.5]
#  [ -99.    99. ]
#  [-148.5  148.5]]
# (2, 3) (0, 8) False
# [[0 2 5]
#  [2 0 3]
#  [5 3 0]]
# [[ 0  1  2  3]
#  [10 11 12 13]
#  [20 21 22 23]]
# [[ 0.  5. 10.]
#  [ 5.  0.  5.]
#  [10.  5.  0.]]
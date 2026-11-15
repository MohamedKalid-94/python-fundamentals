import numpy as np

# RESHAPING: same data, new shape. The number of elements must stay the same.
#   a.reshape(shape)   a view when possible (no copy), a copy otherwise
#   -1 in a shape means "work this one out"
#   order="C" row by row (default), order="F" column by column
#   a.resize(shape)    changes the array IN PLACE;   np.resize(a, shape) repeats the data to fill
#   np.newaxis (None), np.expand_dims, np.squeeze    add or remove axes of length 1

a = np.arange(12)
print(a.reshape(3, 4))
print(a.reshape(2, -1).shape, a.reshape(-1, 6).shape)
print(a.reshape(2, 2, 3))
print(a.reshape(3, 4, order="F"))

try:
    a.reshape(5, 3)
except ValueError as error:
    print("ValueError:", error)

# A reshape is usually a VIEW: both arrays share the memory
b = a.reshape(3, 4)
b[0, 0] = 99
print(a[0], np.shares_memory(a, b))
a[0] = 0

# Adding and removing axes
v = np.array([1, 2, 3])
print(v.shape, v[np.newaxis, :].shape, v[:, np.newaxis].shape)       # row vector and column vector
print(np.expand_dims(v, axis=0).shape, np.expand_dims(v, axis=-1).shape)
print(np.squeeze(np.zeros((1, 3, 1))).shape)
print(np.zeros((1, 3, 1)).squeeze(axis=0).shape)

# resize
r = np.array([1, 2, 3])
print(np.resize(r, (2, 4)))                  # repeats the data to fill
r.resize(5, refcheck=False)                  # in place: pads with zeros
print(r)

# Typical uses
image = np.arange(24).reshape(2, 3, 4)       # 2 channels, 3 rows, 4 columns
print(image.reshape(2, -1).shape)            # every channel flattened to a vector
batch = np.arange(6).reshape(3, 2)
print(batch.reshape(-1).shape, batch.reshape(1, -1).shape)

# EXPECTED OUTPUT
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]
# (2, 6) (2, 6)
# [[[ 0  1  2]
#   [ 3  4  5]]
#
#  [[ 6  7  8]
#   [ 9 10 11]]]
# [[ 0  3  6  9]
#  [ 1  4  7 10]
#  [ 2  5  8 11]]
# ValueError: cannot reshape array of size 12 into shape (5,3)
# 99 True
# (3,) (1, 3) (3, 1)
# (1, 3) (3, 1)
# (3,)
# (3, 1)
# [[1 2 3 1]
#  [2 3 1 2]]
# [1 2 3 0 0]
# (2, 12)
# (6,) (1, 6)
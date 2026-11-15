import numpy as np

# FLATTENING: a 1-D array from an N-D array
#   a.flatten()    always a COPY        a.ravel()    a VIEW when possible        a.reshape(-1)    like ravel
#   a.flat         an iterator / indexable object over all the elements
# TRANSPOSING: swap axes
#   a.T            reverse ALL the axes (a VIEW)        np.transpose(a, axes)    choose the order of the axes
#   np.moveaxis(a, source, destination)                 np.swapaxes comes in Module 26

a = np.arange(6).reshape(2, 3)
print(a)
print(a.flatten(), a.ravel(), a.reshape(-1))
print(a.flatten(order="F"))

flat = a.flatten()
flat[0] = 99
print(a[0, 0])                              # unchanged: flatten made a copy
view = a.ravel()
view[0] = 99
print(a[0, 0])                              # changed: ravel returned a view
a[0, 0] = 0
print(a.flat[4], a.flat[1:3])

print(a.T)
print(a.T.shape, np.transpose(a).shape, a.T.T.tolist() == a.tolist())
print(a.T.flags["C_CONTIGUOUS"], a.T.flags["F_CONTIGUOUS"])     # the same memory, read in another order
print(a.T.ravel())                          # a copy is needed here: the order differs from the memory order

cube = np.arange(24).reshape(2, 3, 4)
print(cube.T.shape)                         # (4, 3, 2)
print(np.transpose(cube, (1, 0, 2)).shape)  # (3, 2, 4)
print(np.moveaxis(cube, 0, -1).shape)       # (3, 4, 2)
print(np.arange(3).T.shape)                 # a 1-D array has nothing to swap

# Use: an image from (height, width, channels) to (channels, height, width)
image = np.zeros((32, 64, 3))
print(np.transpose(image, (2, 0, 1)).shape)
# Use: a matrix times its transpose
m = np.array([[1, 2], [3, 4]])
print(m @ m.T)

# EXPECTED OUTPUT
# [[0 1 2]
#  [3 4 5]]
# [0 1 2 3 4 5] [0 1 2 3 4 5] [0 1 2 3 4 5]
# [0 3 1 4 2 5]
# 0
# 99
# 4 [1 2]
# [[0 3]
#  [1 4]
#  [2 5]]
# (3, 2) (3, 2) True
# False True
# [0 3 1 4 2 5]
# (4, 3, 2)
# (3, 2, 4)
# (3, 4, 2)
# (3,)
# (3, 32, 64)
# [[ 5 11]
#  [11 25]]
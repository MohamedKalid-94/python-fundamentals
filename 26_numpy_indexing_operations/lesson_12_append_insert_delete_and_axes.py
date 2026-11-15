import numpy as np

# CHANGING THE SIZE: arrays have a FIXED size, so each of these makes a NEW array (a copy).
#   np.append(a, values, axis)       add at the end             np.insert(a, position, values, axis)
#   np.delete(a, positions, axis)    remove                     (axis=None flattens first)
# REARRANGING (no new data): swap columns with fancy indexing, reverse with [::-1] or np.flip,
#   np.roll(a, n) shifts and wraps around,  np.rot90 turns a matrix.
# INSERTING AXES: np.newaxis (None) in an index, or np.expand_dims.

a = np.array([1, 2, 3])
print(np.append(a, 4), np.append(a, [4, 5]), a)          # a itself is unchanged
m = np.array([[1, 2], [3, 4]])
print(np.append(m, [[5, 6]], axis=0))
print(np.append(m, [[9], [9]], axis=1))
print(np.append(m, [7, 8]))                              # without an axis: flattened

print(np.insert(a, 1, 99), np.insert(a, [0, 3], [7, 8]))
print(np.insert(m, 1, [0, 0], axis=0))
print(np.insert(m, 1, 5, axis=1))                        # a scalar is broadcast into a new column
print(np.delete(a, 1), np.delete(a, [0, 2]))
print(np.delete(m, 0, axis=0))
print(np.delete(m, 1, axis=1))
print(np.delete(np.arange(10), slice(2, 8, 2)))

# Appending in a loop copies the whole array every time: collect in a list, then convert once
chunks = [np.full(2, i) for i in range(3)]
print(np.concatenate(chunks))

# SWAPPING COLUMNS
c = np.arange(12).reshape(3, 4)
print(c[:, [1, 0, 2, 3]])                                # a copy with the columns reordered
c2 = c.copy()
c2[:, [0, 3]] = c2[:, [3, 0]]                            # in place: the right side is copied first
print(c2)
print(c[:, ::-1])                                        # all the columns reversed (a view)
print(c[::-1, 0])                                        # the rows reversed, first column
print(np.flip(c, axis=1).tolist() == c[:, ::-1].tolist())
print(np.roll(np.arange(5), 2), np.roll(c, 1, axis=1)[0])
print(np.rot90(np.arange(4).reshape(2, 2)))

# INSERTING AXES
v = np.arange(3)
print(v[np.newaxis].shape, v[:, None].shape, np.expand_dims(v, (0, 2)).shape, v[None, :, None].shape)

# JOINING (recap of Module 25, lesson 09)
print(np.concatenate((a, a)), np.hstack((m, m)).shape, np.vstack((m, m)).shape)

# EXPECTED OUTPUT
# [1 2 3 4] [1 2 3 4 5] [1 2 3]
# [[1 2]
#  [3 4]
#  [5 6]]
# [[1 2 9]
#  [3 4 9]]
# [1 2 3 4 7 8]
# [ 1 99  2  3] [7 1 2 3 8]
# [[1 2]
#  [0 0]
#  [3 4]]
# [[1 5 2]
#  [3 5 4]]
# [1 3] [2]
# [[3 4]]
# [[1]
#  [3]]
# [0 1 3 5 7 8 9]
# [0 0 1 1 2 2]
# [[ 1  0  2  3]
#  [ 5  4  6  7]
#  [ 9  8 10 11]]
# [[ 3  1  2  0]
#  [ 7  5  6  4]
#  [11  9 10  8]]
# [[ 3  2  1  0]
#  [ 7  6  5  4]
#  [11 10  9  8]]
# [8 4 0]
# True
# [3 4 0 1 2] [3 0 1 2]
# [[1 3]
#  [0 2]]
# (1, 3) (3, 1) (1, 3, 1) (1, 3, 1)
# [1 2 3 1 2 3] (2, 4) (4, 2)
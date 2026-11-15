import numpy as np

# SPLITTING: cut an array into several arrays (the pieces are VIEWS of the original).
#   split(a, n)             n EQUAL parts (an error if the length is not divisible)
#   array_split(a, n)       allows unequal parts
#   split(a, [i, j])        cut BEFORE the indices i and j
#   hsplit / vsplit / dsplit = split along axis 1 / 0 / 2

a = np.arange(12)
for part in np.split(a, 3):
    print(part)
print(np.split(a, [2, 5]))                           # cuts at 2 and 5: three pieces
try:
    np.split(a, 5)
except ValueError as error:
    print("ValueError:", error)
print([p.tolist() for p in np.array_split(a, 5)])    # 12 = 3 + 3 + 2 + 2 + 2

m = np.arange(16).reshape(4, 4)
top, bottom = np.vsplit(m, 2)
left, right = np.hsplit(m, 2)
print(top)
print(right)
print(np.split(m, 2, axis=1)[0].tolist() == left.tolist())
print([p.shape for p in np.hsplit(m, [1, 3])])

# The pieces are views
pieces = np.split(a.copy(), 2)
pieces[0][0] = 100
print(pieces[0][:2], np.shares_memory(pieces[0], pieces[1]))

# Use: a train/test split by position (real data is shuffled first: Module 27)
data = np.arange(10)
train, test = np.split(data, [8])
print(train, test)

# EXPECTED OUTPUT
# [0 1 2 3]
# [4 5 6 7]
# [ 8  9 10 11]
# [array([0, 1]), array([2, 3, 4]), array([ 5,  6,  7,  8,  9, 10, 11])]
# ValueError: array split does not result in an equal division
# [[0, 1, 2], [3, 4, 5], [6, 7], [8, 9], [10, 11]]
# [[0 1 2 3]
#  [4 5 6 7]]
# [[ 2  3]
#  [ 6  7]
#  [10 11]
#  [14 15]]
# True
# [(4, 1), (4, 2), (4, 1)]
# [100   1] False
# [0 1 2 3 4 5 6 7] [8 9]
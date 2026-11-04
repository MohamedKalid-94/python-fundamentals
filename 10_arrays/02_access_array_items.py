from array import array

a = array("i", [10, 20, 30, 40, 50])
#  index:    0   1   2   3   4
#  negative: -5  -4  -3  -2  -1

# Indexing
print(a[0], a[2])                           # 10 30
print(a[-1], a[-2])                         # 50 40

try:
    print(a[5])
except IndexError as e:
    print(e)                                # array index out of range

# Slicing returns a NEW ARRAY of the same type, and never raises IndexError
print(a[1:4])                               # array('i', [20, 30, 40])
print(a[:2])                                # array('i', [10, 20])
print(a[::2])                               # array('i', [10, 30, 50])
print(a[::-1])                              # array('i', [50, 40, 30, 20, 10])
print(a[10:])                               # array('i')
print(type(a[1:4]))                         # <class 'array.array'>

# Searching
print(a.index(30))                          # 2
print(array("i", [1, 2, 2, 3]).count(2))    # 2
print(30 in a, 99 in a)                     # True False

# Built-in functions
print(len(a), sum(a), min(a), max(a))       # 5 150 10 50
print(a.tolist())                           # [10, 20, 30, 40, 50]

# Size information: buffer_info() gives (address, number of items)
info = a.buffer_info()
print(info[1], info[1] * a.itemsize)        # 5 20       (items, bytes)

# ---- CHANGING items ----
a[0] = 11
print(a)                                    # array('i', [11, 20, 30, 40, 50])

# A slice can only be replaced by an ARRAY of the same type
a[1:3] = array("i", [21, 31])
print(a)                                    # array('i', [11, 21, 31, 40, 50])

try:
    a[1:3] = [0, 0]
except TypeError as e:
    print(type(e).__name__)                 # TypeError

# The value must fit the type
try:
    array("B", [0])[0] = 300
except OverflowError as e:
    print(type(e).__name__)                 # OverflowError

# Update every item (use the index)
for i in range(len(a)):
    a[i] *= 2
print(a)                                    # array('i', [22, 42, 62, 80, 100])
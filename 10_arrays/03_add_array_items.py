from array import array

a = array("i", [1, 2, 3])

# append(x): one item at the end
a.append(4)
print(a)                                    # array('i', [1, 2, 3, 4])

# extend(iterable): every item (an array of the same type, or any iterable of valid items)
a.extend([5, 6])
print(a)                                    # array('i', [1, 2, 3, 4, 5, 6])
a.extend(array("i", [7]))
print(a)                                    # array('i', [1, 2, 3, 4, 5, 6, 7])

# insert(index, x)
a.insert(0, 0)
print(a)                                    # array('i', [0, 1, 2, 3, 4, 5, 6, 7])
a.insert(100, 8)                            # beyond the end: goes to the end
print(a)                                    # array('i', [0, 1, 2, 3, 4, 5, 6, 7, 8])

# fromlist(list): add all items of a list
a.fromlist([9])
print(a)                                    # array('i', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

# + builds a NEW array; += extends in place
b = a + array("i", [10])
print(len(a), len(b))                       # 10 11
a += array("i", [10])
print(len(a))                               # 11

# Insert several items with slice assignment
c = array("i", [1, 2, 5])
c[2:2] = array("i", [3, 4])
print(c)                                    # array('i', [1, 2, 3, 4, 5])

# Repetition
print(array("i", [0]) * 3)                  # array('i', [0, 0, 0])

# The type rules still apply
tests = [
    ("append a string", lambda: array("i").append("x")),
    ("append a float", lambda: array("i").append(1.5)),
    ("append 256 to 'B'", lambda: array("B").append(256)),
    ("extend with a 'd' array", lambda: array("i").extend(array("d", [1.0]))),
    ("add arrays of different types", lambda: array("i", [1]) + array("d", [1.0])),
]
for label, action in tests:
    try:
        action()
    except (TypeError, OverflowError) as e:
        print(label, "->", type(e).__name__)
# append a string -> TypeError
# append a float -> TypeError
# append 256 to 'B' -> OverflowError
# extend with a 'd' array -> TypeError
# add arrays of different types -> TypeError

# Building an array in a loop
squares = array("i")
for n in range(5):
    squares.append(n * n)
print(squares)                              # array('i', [0, 1, 4, 9, 16])

# Speed: append() is fast; insert(0, x) shifts every item (like memmove).
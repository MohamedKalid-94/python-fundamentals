# A tuple is an ORDERED, IMMUTABLE collection that allows DUPLICATES.

point = (3, 4)
print(point, type(point), len(point))       # (3, 4) <class 'tuple'> 2

# The parentheses are optional: the COMMAS make the tuple
t = 1, 2, 3
print(t)                                    # (1, 2, 3)

# TRAP: a single-item tuple needs a trailing comma
print(type((5)))                            # <class 'int'>
print(type((5,)))                           # <class 'tuple'>
single = 5,
print(single, type(single))                 # (5,) <class 'tuple'>

# Empty tuple
print((), tuple(), len(()))                 # () () 0

# tuple() converts any iterable
print(tuple([1, 2, 3]))                     # (1, 2, 3)
print(tuple("abc"))                         # ('a', 'b', 'c')
print(tuple(range(3)))                      # (0, 1, 2)
print(tuple({"a": 1}))                      # ('a',)

# Any types, mixed and nested
info = ("Ann", 30, ["x", "y"], (1, 2))
print(info)                                 # ('Ann', 30, ['x', 'y'], (1, 2))

# IMMUTABLE: items cannot be assigned
try:
    point[0] = 9
except TypeError as e:
    print(e)                                # 'tuple' object does not support item assignment

# A tuple of immutable items is HASHABLE, so it can be a dictionary key
print(hash((1, 2)) == hash((1, 2)))         # True
d = {(0, 0): "origin", (1, 2): "A"}
print(d[(1, 2)])                            # A

# A tuple that contains a list is NOT hashable
try:
    hash((1, [2]))
except TypeError as e:
    print(e)                                # unhashable type: 'list'

# Comparison works item by item; different types are never equal
print((1, 2) < (1, 3), (1, 2) == (1, 2), (1, 2) == [1, 2])   # True True False

# Repetition and concatenation (both create new tuples)
print((0,) * 3, (1, 2) + (3,))              # (0, 0, 0) (1, 2, 3)

# Membership and truthiness
print(2 in (1, 2, 3))                       # True
print(bool(()), bool((0,)))                 # False True

# Tuples are usually smaller than lists (CPython)
import sys
print(sys.getsizeof((1, 2, 3)) < sys.getsizeof([1, 2, 3]))   # True

# WHY USE A TUPLE
# - A fixed record: (x, y), (r, g, b), (name, age)
# - Safe constants: PIN_MODES = ("INPUT", "OUTPUT")
# - Dictionary keys and set members
# - Returning several values from a function
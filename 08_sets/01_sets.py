# A set is an UNORDERED, MUTABLE collection of UNIQUE, HASHABLE items.

fruits = {"apple", "banana", "cherry"}
print(type(fruits), len(fruits))            # <class 'set'> 3
print(sorted(fruits))                       # ['apple', 'banana', 'cherry']

# Duplicates disappear
print({1, 2, 2, 3, 3, 3})                   # {1, 2, 3}

# TRAP: {} is an empty DICT. Use set() for an empty set.
print(type({}), type(set()))                # <class 'dict'> <class 'set'>

# set() converts any iterable
print(set([1, 2, 2, 3]))                    # {1, 2, 3}
print(sorted(set("hello")))                 # ['e', 'h', 'l', 'o']
print(set(range(4)))                        # {0, 1, 2, 3}
print(set())                                # set()

# No order, so no indexing or slicing
try:
    fruits[0]
except TypeError as e:
    print(e)                                # 'set' object is not subscriptable

# Items must be HASHABLE (immutable): lists and dicts are not allowed
try:
    {[1, 2]}
except TypeError as e:
    print(e)                                # unhashable type: 'list'

# Tuples are fine, and equality ignores order
print({(1, 2), (3, 4)} == {(3, 4), (1, 2)})         # True

# Mixed types: items that compare equal count as one
print(sorted({1, 2.0, "a"}, key=str))       # [1, 2.0, 'a']
print({1, 1.0, True})                       # {1}
print({0, False, 0.0})                      # {0}

# Sets are mutable
s = {1}
s.add(2)
print(s)                                    # {1, 2}

# frozenset: an IMMUTABLE set (can be a dict key or a set member)
fs = frozenset([1, 2, 3])
print(fs)                                   # frozenset({1, 2, 3})
try:
    fs.add(4)
except AttributeError as e:
    print(e)                                # 'frozenset' object has no attribute 'add'
print(hash(fs) == hash(frozenset([3, 2, 1])))       # True

# Membership is very fast (hashing), unlike a list search
print(2 in {1, 2, 3})                       # True

# Truthiness
print(bool(set()), bool({0}))               # False True

# WHEN TO USE A SET
# - remove duplicates
# - fast "is it in there?" checks
# - maths on groups: union, intersection, difference
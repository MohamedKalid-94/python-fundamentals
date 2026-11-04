# Tuples cannot be changed. To "update" one, you build a NEW tuple.

t = (1, 2, 3)
try:
    t[0] = 99
except TypeError as e:
    print(e)                            # 'tuple' object does not support item assignment

# Way 1: tuple -> list -> change -> tuple
items = list(t)
items[0] = 99
t = tuple(items)
print(t)                                # (99, 2, 3)

# Way 2: concatenation builds a new tuple
t = t + (4,)
print(t)                                # (99, 2, 3, 4)

before = id(t)
t += (5,)
print(t, id(t) == before)               # (99, 2, 3, 4, 5) False    (a new object)

# Insert with slicing
t = (1, 2, 3)
t = t[:1] + ("x",) + t[1:]
print(t)                                # (1, 'x', 2, 3)

# Remove by position with slicing
t = t[:1] + t[2:]
print(t)                                # (1, 2, 3)

# Remove by value through a list
items = list(t)
items.remove(2)
t = tuple(items)
print(t)                                # (1, 3)

# Replace a part
t = (1, 2, 3, 4, 5)
t = t[:2] + (20, 30) + t[4:]
print(t)                                # (1, 2, 20, 30, 5)

# Items cannot be deleted, but the whole name can
try:
    del t[0]
except TypeError as e:
    print(e)                            # 'tuple' object doesn't support item deletion

del t
try:
    print(t)
except NameError:
    print("t is gone")                  # t is gone

# A mutable item inside a tuple can change in place
t = ([1, 2], 3)
t[0].append(9)
print(t)                                # ([1, 2, 9], 3)

# FAMOUS QUIRK: += on a list inside a tuple works AND raises an error
t = ([1, 2], 3)
try:
    t[0] += [5]
except TypeError as e:
    print(e)                            # 'tuple' object does not support item assignment
print(t)                                # ([1, 2, 5], 3)    (the list was extended anyway)

# sorted() returns a LIST; wrap it to get a tuple back
print(sorted((3, 1, 2)), tuple(sorted((3, 1, 2))))    # [1, 2, 3] (1, 2, 3)
a = (1, 2)
b = (3, 4)

# 1. + makes a new tuple
print(a + b)                            # (1, 2, 3, 4)
print(a, b)                             # (1, 2) (3, 4)

# 2. += also makes a NEW tuple (tuples cannot grow in place)
c = (1, 2)
c += (3,)
print(c)                                # (1, 2, 3)

# 3. * repeats
print(a * 2)                            # (1, 2, 1, 2)

# 4. Unpacking with *
print((*a, *b, 5))                      # (1, 2, 3, 4, 5)

# 5. itertools.chain for many tuples
from itertools import chain
print(tuple(chain(a, b, (5,))))         # (1, 2, 3, 4, 5)

# 6. Through lists
print(tuple(list(a) + list(b)))         # (1, 2, 3, 4)

# Join a tuple of STRINGS into one string
print(",".join(("a", "b", "c")))        # a,b,c

# Pair items with zip
print(tuple(zip((1, 2), ("a", "b"))))   # ((1, 'a'), (2, 'b'))

# Join many tuples into one
print(sum(((1, 2), (3, 4)), ()))        # (1, 2, 3, 4)   (works, but slow for big data)

# Join without duplicates, keeping the order
print(tuple(dict.fromkeys((1, 2, 3) + (3, 4, 1))))   # (1, 2, 3, 4)

# A tuple inside a tuple stays nested
print((1, 2) + ((3, 4),))               # (1, 2, (3, 4))

# + needs two tuples
try:
    print((1,) + [2])
except TypeError as e:
    print(e)                            # can only concatenate tuple (not "list") to tuple
print((1,) + tuple([2]))                # (1, 2)
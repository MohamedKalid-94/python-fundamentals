from array import array
from itertools import chain

a = array("i", [1, 2])
b = array("i", [3, 4])

# 1. + makes a NEW array (both must have the same typecode)
print(a + b)                                # array('i', [1, 2, 3, 4])
print(a, b)                                 # array('i', [1, 2]) array('i', [3, 4])

# 2. extend()
c = array("i", [1, 2])
c.extend(b)
print(c)                                    # array('i', [1, 2, 3, 4])

# 3. += (in place)
d = array("i", [1, 2])
d += b
print(d)                                    # array('i', [1, 2, 3, 4])

# 4. fromlist()
e = array("i", [1, 2])
e.fromlist([3, 4])
print(e)                                    # array('i', [1, 2, 3, 4])

# 5. Build from several iterables
print(array("i", chain(a, b, [5])))         # array('i', [1, 2, 3, 4, 5])

# Different typecodes cannot be added
try:
    array("i", [1]) + array("d", [1.0])
except TypeError as e:
    print(type(e).__name__)                 # TypeError

# 6. Bytes: join the raw data
print(array("B", b"AB") + array("B", b"CD"))        # array('B', [65, 66, 67, 68])
print(a.tobytes() + b.tobytes() == array("i", [1, 2, 3, 4]).tobytes())   # True

# 7. Flatten a list of arrays
matrix = [array("i", [1, 2]), array("i", [3]), array("i", [4, 5])]
print(array("i", [v for row in matrix for v in row]))      # array('i', [1, 2, 3, 4, 5])

# 8. Interleave
print(array("i", [x for pair in zip(a, b) for x in pair]))  # array('i', [1, 3, 2, 4])

# 9. Join without duplicates
print(array("i", sorted(set(a) | set(b))))  # array('i', [1, 2, 3, 4])

# 10. Join the items into a string
print(" ".join(map(str, a + b)))            # 1 2 3 4

# Repetition builds a buffer
print(array("B", [0]) * 4)                  # array('B', [0, 0, 0, 0])
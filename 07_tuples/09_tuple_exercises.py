# 1. Swap two values
a, b = 1, 2
a, b = b, a
print(a, b)                                     # 2 1

# 2. Return the minimum and maximum together
def min_max(nums):
    return min(nums), max(nums)

print(min_max((4, 9, 1)))                       # (1, 9)

# 3. Position of the largest value, reversed tuple, count of the largest
data = (4, 9, 2, 9)
print(data.index(max(data)), data[::-1], data.count(9))     # 1 (9, 2, 9, 4) 2

# 4. Sort a list of tuples by the second item
pairs = [(1, "b"), (2, "a"), (3, "c")]
print(sorted(pairs, key=lambda x: x[1]))        # [(2, 'a'), (1, 'b'), (3, 'c')]

# 5. List of lists to a tuple of tuples
print(tuple(map(tuple, [[1, 2], [3, 4]])))      # ((1, 2), (3, 4))

# 6. Distance between two points
from math import dist
p1, p2 = (0, 0), (3, 4)
print(dist(p1, p2))                             # 5.0
print(((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5)     # 5.0

# 7. Tuples as dictionary keys (grid coordinates)
grid = {(0, 0): "start", (2, 3): "end"}
print((2, 3) in grid, grid[(0, 0)])             # True start

# 8. Dictionary to tuple of pairs, and back
pairs = tuple({"a": 1, "b": 2}.items())
print(pairs)                                    # (('a', 1), ('b', 2))
print(dict(pairs))                              # {'a': 1, 'b': 2}

# 9. Zip into records, then unzip
names = ("Ann", "Bob")
ages = (30, 25)
records = tuple(zip(names, ages))
print(records)                                  # (('Ann', 30), ('Bob', 25))
n, a = zip(*records)
print(n, a)                                     # ('Ann', 'Bob') (30, 25)

# 10. Flatten a tuple of tuples
print(tuple([v for row in ((1, 2), (3,), (4, 5)) for v in row]))    # (1, 2, 3, 4, 5)

# 11. Remove duplicates, keep the order
print(tuple(dict.fromkeys((3, 1, 3, 2, 1))))    # (3, 1, 2)

# 12. RGB to hex and back
rgb = (255, 128, 0)
hexcode = "#%02x%02x%02x" % rgb
print(hexcode)                                  # #ff8000
print(tuple(int(hexcode[i:i + 2], 16) for i in (1, 3, 5)))      # (255, 128, 0)

# 13. Is a tuple sorted?
def is_sorted(t):
    return all(x <= y for x, y in zip(t, t[1:]))

print(is_sorted((1, 2, 2, 5)), is_sorted((3, 1)))               # True False

# 14. Constants as a tuple (embedded style)
PIN_MODES = ("INPUT", "OUTPUT", "ANALOG", "PWM")
print(PIN_MODES.index("PWM"), PIN_MODES[3])     # 3 PWM

# 15. Return a status and a value
def read_sensor():
    return True, 36.5

ok, value = read_sensor()
print(ok, value)                                # True 36.5

# 16. Compare version numbers (tuples compare item by item)
print((3, 12, 1) > (3, 9, 9), (3, 11) < (3, 12))    # True True
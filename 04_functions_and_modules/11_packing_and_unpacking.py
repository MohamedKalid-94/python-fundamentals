# PACKING: several values into one tuple
point = 1, 2, 3
print(point)                    # (1, 2, 3)

# UNPACKING: one sequence into several names
x, y, z = point
print(x, y, z)                  # 1 2 3

# Works with any iterable
a, b, c = "xyz"
print(a, b, c)                  # x y z

# The count must match
try:
    p, q, r = (1, 2)
except ValueError as e:
    print(e)                    # not enough values to unpack (expected 3, got 2)

try:
    p, q = (1, 2, 3)
except ValueError as e:
    print(e)                    # too many values to unpack (expected 2)

# Swap
m, n = 1, 2
m, n = n, m
print(m, n)                     # 2 1

# STAR unpacking: collect the rest into a list
first, *rest = [1, 2, 3, 4]
print(first, rest)              # 1 [2, 3, 4]

*init, last = [1, 2, 3, 4]
print(init, last)               # [1, 2, 3] 4

head, *middle, tail = [1, 2, 3, 4, 5]
print(head, middle, tail)       # 1 [2, 3, 4] 5

lone, *others = [7]
print(lone, others)             # 7 []

h, *t = "hello"
print(h, t)                     # h ['e', 'l', 'l', 'o']

# Ignore values with _
_, second, _ = (10, 20, 30)
print(second)                   # 20

# Nested
(a1, a2), a3 = (1, 2), 3
print(a1, a2, a3)               # 1 2 3

# Unpacking in loops
for name, score in [("Ann", 90), ("Bob", 80)]:
    print(name, score)
# Ann 90
# Bob 80

# Combining with * and ** in literals and calls
list1, list2 = [1, 2], [3, 4]
print([*list1, *list2])         # [1, 2, 3, 4]
print((*list1, 5))              # (1, 2, 5)
print({*[1, 2, 2], 3})          # {1, 2, 3}
print(*"abc")                   # a b c

d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
print({**d1, **d2})             # {'a': 1, 'b': 3, 'c': 4}   later keys win
print(d1 | d2)                  # {'a': 1, 'b': 3, 'c': 4}   (Python 3.9+)
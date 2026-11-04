# UNPACKING: assign each item of a tuple to its own name

x, y = (1, 2)
print(x, y)                             # 1 2

a, b, c = 10, 20, 30                    # the parentheses are optional
print(a, b, c)                          # 10 20 30

# The count must match
try:
    p, q, r = (1, 2)
except ValueError as e:
    print(e)                            # not enough values to unpack (expected 3, got 2)

try:
    p, q = (1, 2, 3)
except ValueError as e:
    print(e)                            # too many values to unpack (expected 2)

# Star: collect the rest into a LIST
first, *rest = (1, 2, 3, 4)
print(first, rest)                      # 1 [2, 3, 4]

*init, last = (1, 2, 3, 4)
print(init, last)                       # [1, 2, 3] 4

head, *mid, tail = (1, 2, 3, 4, 5)
print(head, mid, tail)                  # 1 [2, 3, 4] 5

# Ignore values with _
_, second, _ = (10, 20, 30)
print(second)                           # 20

# Nested unpacking
(a, b), (c, d) = (1, 2), (3, 4)
print(a, b, c, d)                       # 1 2 3 4

name, (r, g, b) = ("red", (255, 0, 0))
print(name, r, g, b)                    # red 255 0 0

# Swap
m, n = 1, 2
m, n = n, m
print(m, n)                             # 2 1

# Functions that return several values
def min_max(nums):
    return min(nums), max(nums)

low, high = min_max((4, 9, 1))
print(low, high)                        # 1 9

# In loops
for name, age in (("Ann", 30), ("Bob", 25)):
    print(name, age)
# Ann 30
# Bob 25

for i, (p, q) in enumerate([(1, 2), (3, 4)]):
    print(i, p, q)
# 0 1 2
# 1 3 4

# Unpacking INTO a call with *
print(*(1, 2, 3))                       # 1 2 3

def add(a, b):
    return a + b

print(add(*(3, 4)))                     # 7

# Any iterable can be unpacked
a, b = "hi"
print(a, b)                             # h i
x, y, z = range(3)
print(x, y, z)                          # 0 1 2

# Practical: an RGB colour to a hex code
rgb = (255, 128, 0)
r, g, b = rgb
print(f"#{r:02x}{g:02x}{b:02x}")        # #ff8000
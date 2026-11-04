colors = ("red", "green", "blue", "yellow", "purple")
#  index:    0       1       2        3         4
#  negative: -5     -4      -3       -2        -1

print(colors[0], colors[2])             # red blue
print(colors[-1], colors[-2])           # purple yellow

try:
    print(colors[5])
except IndexError as e:
    print(e)                            # tuple index out of range

# Slicing returns a NEW TUPLE and never raises IndexError
print(colors[1:3])                      # ('green', 'blue')
print(colors[:2])                       # ('red', 'green')
print(colors[2:])                       # ('blue', 'yellow', 'purple')
print(colors[-3:])                      # ('blue', 'yellow', 'purple')
print(colors[::2])                      # ('red', 'blue', 'purple')
print(colors[::-1])                     # ('purple', 'yellow', 'blue', 'green', 'red')
print(colors[10:])                      # ()
print(type(colors[1:3]))                # <class 'tuple'>

# Nested tuples
nested = ((1, 2), (3, 4))
print(nested[1][0])                     # 3

# A mutable item INSIDE a tuple can still change
data = ("a", [1, 2])
data[1].append(3)
print(data)                             # ('a', [1, 2, 3])

# The two tuple methods
nums = (1, 2, 2, 3)
print(nums.index(2), nums.count(2))     # 1 2
try:
    nums.index(9)
except ValueError as e:
    print(e)                            # tuple.index(x): x not in tuple

# Membership and built-in functions
print(2 in nums, 9 not in nums)         # True True
print(len(nums), min(nums), max(nums), sum(nums))   # 4 1 3 8
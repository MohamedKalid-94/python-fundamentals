colors = ["red", "green", "blue", "yellow", "purple"]
#  index:    0       1       2        3         4
#  negative: -5     -4      -3       -2        -1

print(colors[0], colors[2])         # red blue
print(colors[-1], colors[-2])       # purple yellow

# Indexing out of range raises IndexError
try:
    print(colors[5])
except IndexError as e:
    print(e)                        # list index out of range

# Slicing: list[start:stop:step]  (same rules as strings; a NEW list is returned)
print(colors[1:3])                  # ['green', 'blue']
print(colors[:2])                   # ['red', 'green']
print(colors[2:])                   # ['blue', 'yellow', 'purple']
print(colors[-3:])                  # ['blue', 'yellow', 'purple']
print(colors[::2])                  # ['red', 'blue', 'purple']
print(colors[::-1])                 # ['purple', 'yellow', 'blue', 'green', 'red']
print(colors[10:])                  # []     slices never raise IndexError

# Nested lists
matrix = [[1, 2, 3], [4, 5, 6]]
print(matrix[1][0])                 # 4
print(matrix[0])                    # [1, 2, 3]

# Unpacking
first, *rest = colors
print(first, rest)                  # red ['green', 'blue', 'yellow', 'purple']

# Finding the position of a value
print(colors.index("blue"))         # 2
try:
    colors.index("pink")
except ValueError as e:
    print(e)                        # 'pink' is not in list

print([1, 2, 2, 3].count(2))        # 2

# Safe access
idx = 10
print(colors[idx] if 0 <= idx < len(colors) else None)     # None

print(len(colors) - 1)              # 4     the last valid index
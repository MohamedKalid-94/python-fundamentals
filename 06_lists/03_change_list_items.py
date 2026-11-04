nums = [10, 20, 30, 40, 50]

# Change ONE item
nums[0] = 11
print(nums)                         # [11, 20, 30, 40, 50]
nums[-1] = 55
print(nums)                         # [11, 20, 30, 40, 55]

# Change a RANGE with slice assignment (the new part may be a different length)
nums[1:3] = [21, 31]                # same length
print(nums)                         # [11, 21, 31, 40, 55]
nums[1:3] = [99]                    # shrinks the list
print(nums)                         # [11, 99, 40, 55]
nums[1:2] = [7, 8, 9]               # grows the list
print(nums)                         # [11, 7, 8, 9, 40, 55]
nums[1:1] = ["x"]                   # an empty slice INSERTS
print(nums)                         # [11, 'x', 7, 8, 9, 40, 55]
nums[:2] = []                       # an empty list DELETES
print(nums)                         # [7, 8, 9, 40, 55]

# Extended slices need EXACTLY the same length
letters = list("abcdef")
letters[::2] = ["X", "Y", "Z"]
print(letters)                      # ['X', 'b', 'Y', 'd', 'Z', 'f']
try:
    letters[::2] = ["A", "B"]
except ValueError as e:
    print(e)        # attempt to assign sequence of size 2 to extended slice of size 3

# Assigning to a position that does not exist
try:
    nums[10] = 1
except IndexError as e:
    print(e)                        # list assignment index out of range

# Update every item (use the index)
values = [1, 2, 3]
for i in range(len(values)):
    values[i] *= 2
print(values)                       # [2, 4, 6]

# TRAP: the loop variable is just a name, so this changes nothing
values = [1, 2, 3]
for v in values:
    v *= 2
print(values)                       # [1, 2, 3]

# Replace by condition
data = [5, 8, 3, 10]
for i, v in enumerate(data):
    if v % 2 == 0:
        data[i] = 0
print(data)                         # [5, 0, 3, 0]

# Swap two items
items = [1, 2, 3, 4]
items[0], items[-1] = items[-1], items[0]
print(items)                        # [4, 2, 3, 1]

# Nested list
grid = [[1, 2], [3, 4]]
grid[0][1] = 20
print(grid)                         # [[1, 20], [3, 4]]

# Changes are visible through every name for the same list
a = [1, 2]
b = a
b[0] = 99
print(a)                            # [99, 2]
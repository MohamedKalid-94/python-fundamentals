# A list is an ORDERED, MUTABLE collection that allows DUPLICATES.

fruits = ["apple", "banana", "cherry"]
print(fruits)                       # ['apple', 'banana', 'cherry']
print(type(fruits))                 # <class 'list'>
print(len(fruits))                  # 3

# Items can be of any type, mixed
mixed = [1, "two", 3.0, True, None, [5, 6]]
print(mixed)                        # [1, 'two', 3.0, True, None, [5, 6]]

# Empty lists
empty1 = []
empty2 = list()
print(empty1 == empty2, len(empty1))    # True 0

# list() converts any iterable
print(list("abc"))                  # ['a', 'b', 'c']
print(list((1, 2, 3)))              # [1, 2, 3]
print(list(range(5)))               # [0, 1, 2, 3, 4]
print(list({"a": 1, "b": 2}))       # ['a', 'b']       (a dict gives its keys)

# Duplicates are allowed, and ORDER matters
print([1, 2, 2, 3])                 # [1, 2, 2, 3]
print([1, 2] == [2, 1])             # False
print([1, 2, 3] < [1, 2, 4])        # True            (compared item by item)

# Nested lists
matrix = [[1, 2, 3], [4, 5, 6]]
print(matrix[1][2])                 # 6
print(len(matrix))                  # 2

# Membership
print("apple" in fruits)            # True
print("grape" not in fruits)        # True

# Truthiness
print(bool([]), bool([0]))          # False True

# Lists are MUTABLE: the same object is changed in place
nums = [1, 2, 3]
before = id(nums)
nums.append(4)
print(id(nums) == before)           # True

# Repetition
print([0] * 3)                      # [0, 0, 0]

# TRAP: repeating a list of lists repeats the SAME inner list
grid = [[0] * 2] * 2
grid[0][0] = 1
print(grid)                         # [[1, 0], [1, 0]]    both rows changed!

good = [[0] * 2 for _ in range(2)]  # a comprehension builds separate rows
good[0][0] = 1
print(good)                         # [[1, 0], [0, 0]]
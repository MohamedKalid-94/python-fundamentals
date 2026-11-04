# A tuple has only TWO methods, because it cannot change.

t = (1, 2, 2, 3, 2)
print(t.count(2))                       # 3
print(t.index(2))                       # 1
print((1, 2, 1, 2).index(2, 2))         # 3     (search starts at index 2)
print(((1, 2), (1, 2), (3,)).count((1, 2)))    # 2

print([m for m in dir(tuple) if not m.startswith("_")])
# ['count', 'index']

# Built-in functions that work on tuples
nums = (4, 8, 1)
print(len(nums), min(nums), max(nums), sum(nums))       # 3 1 8 13
print(sorted(nums), tuple(reversed(nums)))              # [1, 4, 8] (1, 8, 4)
print(any((0, 1)), all((1, 0)))                         # True False
print(tuple(enumerate(nums)))                           # ((0, 4), (1, 8), (2, 1))
print(tuple(zip(nums, "abc")))                          # ((4, 'a'), (8, 'b'), (1, 'c'))

# Tuple vs list: choose by meaning
#   list  = a collection of similar items that changes   [1, 2, 3, 4]
#   tuple = a fixed record of different parts            ("Ann", 30, "Pune")
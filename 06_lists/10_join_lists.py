a = [1, 2]
b = [3, 4]

# 1. + makes a new list
print(a + b)                        # [1, 2, 3, 4]
print(a, b)                         # [1, 2] [3, 4]

# 2. extend() changes the first list in place
x = [1, 2]
x.extend([3, 4])
print(x)                            # [1, 2, 3, 4]

# 3. += also extends in place
y = [1, 2]
y += [3, 4]
print(y)                            # [1, 2, 3, 4]

# 4. Unpacking with *
print([*a, *b, 5])                  # [1, 2, 3, 4, 5]

# 5. itertools.chain (good for many or large lists)
from itertools import chain
print(list(chain(a, b, [5])))       # [1, 2, 3, 4, 5]

# Joining a list of STRINGS into one string
print(", ".join(["a", "b", "c"]))               # a, b, c
print(", ".join(map(str, [1, 2, 3])))           # 1, 2, 3

# Join many lists into one
all_items = []
for part in [[1], [2, 3], [4]]:
    all_items.extend(part)
print(all_items)                    # [1, 2, 3, 4]

print([v for row in [[1], [2, 3], [4]] for v in row])   # [1, 2, 3, 4]
print(sum([[1], [2, 3]], []))                           # [1, 2, 3]  (works, but slow for big data)

# Pair items from two lists
print(list(zip([1, 2], ["a", "b"])))            # [(1, 'a'), (2, 'b')]

# Interleave
print([x for pair in zip([1, 2], ["a", "b"]) for x in pair])    # [1, 'a', 2, 'b']

# Join without duplicates
print(list(dict.fromkeys([1, 2, 3] + [3, 4, 1])))    # [1, 2, 3, 4]     keeps the order
print(sorted(set([1, 2, 3]) | set([3, 4, 1])))       # [1, 2, 3, 4]     sorted result

# + needs two lists
try:
    print([1] + (2,))
except TypeError as e:
    print(e)                        # can only concatenate list (not "tuple") to list
print([1] + list((2,)))             # [1, 2]
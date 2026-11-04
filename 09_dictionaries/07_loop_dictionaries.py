d = {"a": 1, "b": 2, "c": 3}

# 1. Keys (the default)
for key in d:
    print(key, end=" ")
print()                                     # a b c

# 2. Values
for value in d.values():
    print(value, end=" ")
print()                                     # 1 2 3

# 3. Keys and values together (the most common)
for key, value in d.items():
    print(key, value)
# a 1
# b 2
# c 3

# 4. With a counter
for i, (key, value) in enumerate(d.items(), start=1):
    print(i, key, value)
# 1 a 1
# 2 b 2
# 3 c 3

# 5. Sorted by key, then by value
for key in sorted(d, reverse=True):
    print(key, end=" ")
print()                                     # c b a

for key, value in sorted(d.items(), key=lambda kv: kv[1], reverse=True):
    print(key, value)
# c 3
# b 2
# a 1

# 6. With a condition
for key, value in d.items():
    if value % 2:
        print(key)
# a
# c

# 7. Look up keys from another list
for name in ["a", "z"]:
    print(name, d.get(name, 0))
# a 1
# z 0

# 8. Change values while looping (allowed)
for key in d:
    d[key] *= 10
print(d)                                    # {'a': 10, 'b': 20, 'c': 30}

# 9. Build a filtered copy with a comprehension
print({k: v for k, v in d.items() if v > 10})           # {'b': 20, 'c': 30}

# 10. Consume with popitem()
stack = {"x": 1, "y": 2}
while stack:
    print(stack.popitem())
# ('y', 2)
# ('x', 1)

# 11. Nested loop over a dictionary of lists
orders = {"o1": ["pen", "ink"], "o2": ["pad"]}
for order_id, items in orders.items():
    for item in items:
        print(order_id, item)
# o1 pen
# o1 ink
# o2 pad

# RULE: never add or remove KEYS while looping over the dictionary.
# Changing the value of an existing key is fine.
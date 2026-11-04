colors = {"red", "green", "blue"}

# A set has NO index, so you cannot ask for "the first item".
try:
    colors[0]
except TypeError as e:
    print(e)                                # 'set' object is not subscriptable

# What you CAN do:

# 1. Loop over the items (order is arbitrary, so sort when order matters)
for c in sorted(colors):
    print(c)
# blue
# green
# red

# 2. Test membership
print("red" in colors)                      # True
print("pink" in colors)                     # False

# 3. Convert to a sorted list, then index
ordered = sorted(colors)
print(ordered[0])                           # blue

# 4. Built-in functions
print(min(colors), max(colors))             # blue red
print(len(colors))                          # 3

nums = {10, 20, 30}
print(sum(nums), min(nums), max(nums))      # 60 10 30

# 5. Get ANY one item (which one is not defined)
x = next(iter(colors))
print(x in colors)                          # True

# 6. pop() removes and returns an arbitrary item (see 04_remove_set_items.py)
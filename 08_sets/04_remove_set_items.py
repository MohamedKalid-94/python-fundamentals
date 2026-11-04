# remove(x): delete x, KeyError if it is missing
s = {1, 2, 3}
s.remove(2)
print(s)                                    # {1, 3}
try:
    s.remove(99)
except KeyError as e:
    print(e)                                # 99

# discard(x): delete x, NO error if it is missing
s.discard(99)
print(s)                                    # {1, 3}

# pop(): remove and return an ARBITRARY item
single = {5}
print(single.pop(), single)                 # 5 set()

t = {1, 2, 3}
x = t.pop()
print(x in {1, 2, 3}, len(t))               # True 2

try:
    set().pop()
except KeyError as e:
    print(e)                                # 'pop from an empty set'

# clear(): empty the set
u = {1, 2}
u.clear()
print(u)                                    # set()

# Remove several items at once
v = {1, 2, 3, 4}
v -= {2, 3}
print(v)                                    # {1, 4}
v.difference_update({1})
print(v)                                    # {4}

# Keep only the items found in another set
w = {1, 2, 3, 4}
w.intersection_update({2, 3, 9})
print(w)                                    # {2, 3}

# Remove by condition: build a new set
nums = {1, 2, 3, 4, 5, 6}
nums = {n for n in nums if n % 2 == 0}
print(nums)                                 # {2, 4, 6}

# TRAP: changing a set while looping over it
s = {1, 2, 3, 4}
try:
    for n in s:
        if n % 2 == 0:
            s.remove(n)
except RuntimeError as e:
    print(e)                                # Set changed size during iteration

# FIX: loop over a copy
s = {1, 2, 3, 4}
for n in list(s):
    if n % 2 == 0:
        s.remove(n)
print(s)                                    # {1, 3}

# del removes the NAME, not an item
del s
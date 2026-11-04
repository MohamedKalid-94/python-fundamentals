s = {1, 2}

# add(x): add ONE item
s.add(3)
print(s)                                    # {1, 2, 3}
s.add(2)                                    # already there: nothing happens
print(s)                                    # {1, 2, 3}

# add() returns None (it changes the set in place)
print(s.add(4))                             # None
print(s)                                    # {1, 2, 3, 4}

# update(iterable): add EVERY item of one or more iterables
s.update([4, 5])
print(s)                                    # {1, 2, 3, 4, 5}
s.update([6], (7,), {8})
print(s)                                    # {1, 2, 3, 4, 5, 6, 7, 8}

# |= is the operator form
s |= {9}
print(s)                                    # {1, 2, 3, 4, 5, 6, 7, 8, 9}

# add() takes ONE item as it is; update() takes an iterable and unpacks it
a = set()
a.add("abc")
print(a)                                    # {'abc'}
b = set()
b.update("abc")
print(sorted(b))                            # ['a', 'b', 'c']

# Tuples can be added, lists cannot
t = set()
t.add((1, 2))
print(t)                                    # {(1, 2)}
try:
    t.add([1, 2])
except TypeError as e:
    print(e)                                # unhashable type: 'list'

# Building a set of unique values in a loop
unique = set()
for n in [3, 1, 3, 2, 1]:
    unique.add(n)
print(unique)                               # {1, 2, 3}

# A frozenset cannot be changed
try:
    frozenset([1]).add(2)
except AttributeError as e:
    print(e)                                # 'frozenset' object has no attribute 'add'

# There is no insert position and no order: items go wherever the hash puts them
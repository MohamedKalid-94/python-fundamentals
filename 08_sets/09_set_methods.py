a = {1, 2, 3}
b = {3, 4}

# Methods that RETURN a new set (the original is unchanged)
print(a.union(b))                           # {1, 2, 3, 4}
print(a.intersection(b))                    # {3}
print(a.difference(b))                      # {1, 2}
print(a.symmetric_difference(b))            # {1, 2, 4}
print(a.copy())                             # {1, 2, 3}

# Methods that return True / False
print(a.isdisjoint({7}), {1, 2}.issubset(a), a.issuperset({1, 2}))   # True True True

# Methods that CHANGE the set in place
c = {1, 2, 3}
c.difference_update({1})
print(c)                                    # {2, 3}
c.intersection_update({3, 4})
print(c)                                    # {3}
c.symmetric_difference_update({3, 9})
print(c)                                    # {9}

d = {1}
d.add(2)
d.update([3, 4])
d.discard(4)
d.remove(3)
d = {1, 2}
removed = d.pop()
print(removed in {1, 2}, len(d))            # True 1

# Methods accept ANY iterable (operators do not)
print(a.intersection([2, 3, 9]))            # {2, 3}
print(a.difference(range(2, 10)))           # {1}
print({1, 2}.issubset([1, 2, 3, 4]))        # True

# Several arguments at once
print(a.union({7}, [8]))                    # {1, 2, 3, 7, 8}
print(a.intersection({1, 2}, {2, 3}))       # {2}

# Built-in functions
s = {4, 8, 1}
print(len(s), min(s), max(s), sum(s))       # 3 1 8 13
print(sorted(s))                            # [1, 4, 8]
print(any({0, 1}), all({1, 0}))             # True False

# All the set methods
print([m for m in dir(set) if not m.startswith("_")])
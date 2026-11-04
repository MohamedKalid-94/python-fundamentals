a = {1, 2, 3}
b = {3, 4, 5}
c = {5, 6}

# 1. | and union() make a NEW set
print(a | b)                                # {1, 2, 3, 4, 5}
print(a.union(b))                           # {1, 2, 3, 4, 5}

# union() accepts ANY iterable; | needs sets on both sides
print(a.union([7, 8]))                      # {1, 2, 3, 7, 8}

# Several sets at once
print(a | b | c)                            # {1, 2, 3, 4, 5, 6}
print(a.union(b, c))                        # {1, 2, 3, 4, 5, 6}
print(a, b)                                 # {1, 2, 3} {3, 4, 5}      (unchanged)

# 2. update() and |= change the first set IN PLACE
x = {1, 2}
x.update({3})
print(x)                                    # {1, 2, 3}

# 3. Unpacking
print({*a, *b})                             # {1, 2, 3, 4, 5}

# 4. From lists
print(set([1, 2]) | set([2, 3]))            # {1, 2, 3}

# 5. Join many sets
print(set().union(*[{1}, {2, 3}, {3, 4}]))  # {1, 2, 3, 4}

# Other ways to join (details in 08_set_operators.py and 09_set_methods.py)
print(a & b)                                # {3}              only items in both
print(a ^ b)                                # {1, 2, 4, 5}     items in exactly one

# In-place versions
y = {1, 2, 3}
y.intersection_update({2, 3, 4})
print(y)                                    # {2, 3}
y.symmetric_difference_update({3, 9})
print(y)                                    # {2, 9}

# + does not exist for sets
try:
    print(a + b)
except TypeError as e:
    print(e)                                # unsupported operand type(s) for +: 'set' and 'set'

# The operator | needs two sets; the method accepts a list
try:
    print(a | [1])
except TypeError as e:
    print(e)                                # unsupported operand type(s) for |: 'set' and 'list'

# The type of the LEFT operand wins
print(frozenset({1}) | {2})                 # frozenset({1, 2})

# Join the items of a set into a string
print(", ".join(sorted({"b", "a", "c"})))   # a, b, c
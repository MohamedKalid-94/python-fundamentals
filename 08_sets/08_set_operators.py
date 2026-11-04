a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

#   a: 1 2 [3 4]        [3 4] = the overlap
#   b:      [3 4] 5 6

print(a | b)                                # {1, 2, 3, 4, 5, 6}   union
print(a & b)                                # {3, 4}               intersection
print(a - b)                                # {1, 2}               difference (in a, not in b)
print(b - a)                                # {5, 6}
print(a ^ b)                                # {1, 2, 5, 6}         symmetric difference

# Comparison operators: subset and superset
print({1, 2} <= {1, 2, 3}, {1, 2} < {1, 2, 3})      # True True    subset, proper subset
print({1, 2, 3} >= {1, 2}, {1, 2, 3} > {1, 2})      # True True    superset, proper superset
print({1, 2} <= {1, 2}, {1, 2} < {1, 2})            # True False   equal sets: subset yes, PROPER subset no
print({1, 2} == {2, 1}, {1, 2} != {1, 3})           # True True

print(a.isdisjoint({7, 8}))                 # True    no items in common

# Membership
print(3 in a, 9 not in a)                   # True True

# In-place operators
x = {1, 2, 3}
x |= {4}
print(x)                                    # {1, 2, 3, 4}
x &= {2, 3, 4, 9}
print(x)                                    # {2, 3, 4}
x -= {4}
print(x)                                    # {2, 3}
x ^= {3, 5}
print(x)                                    # {2, 5}

# Operators need sets on BOTH sides
try:
    print(a | [1])
except TypeError as e:
    print(e)                                # unsupported operand type(s) for |: 'set' and 'list'

# Precedence: & first, then ^, then |
print({1} | {2} & {2, 3})                   # {1, 2}
print(({1} | {2}) & {2, 3})                 # {2}

# Similarity of two groups
print(len(a & b), len(a | b), round(len(a & b) / len(a | b), 2))    # 2 6 0.33
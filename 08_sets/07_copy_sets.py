import copy

# Assignment does NOT copy
a = {1, 2, 3}
b = a
b.add(4)
print(a)                                    # {1, 2, 3, 4}
print(a is b)                               # True

# copy() makes a new set
c = a.copy()
print(c == a, c is a)                       # True False
c.add(5)
print(a, c)                                 # {1, 2, 3, 4} {1, 2, 3, 4, 5}

# Other ways to copy
d = set(a)
e = {*a}
f = copy.copy(a)
print(d == a, e == a, f == a)               # True True True
print(d is a, e is a, f is a)               # False False False

# An immutable copy
fs = frozenset(a)
print(fs == a)                              # True   (a frozenset equals a set with the same items)

# A shallow copy is enough: set items must be hashable (immutable),
# so there are no inner mutable objects to share. deepcopy is rarely needed.

# Protect the caller's set inside a function
def with_item(s, x):
    s = s.copy()
    s.add(x)
    return s

orig = {1}
new = with_item(orig, 2)
print(orig, new)                            # {1} {1, 2}

# Replace the contents IN PLACE (every name sees the change)
x = {1, 2}
alias = x
x.clear()
x.update({7, 8})
print(alias)                                # {7, 8}
import copy

# Assignment does NOT copy: both names point to the SAME list
a = [1, 2, 3]
b = a
b.append(4)
print(a)                            # [1, 2, 3, 4]
print(a is b)                       # True

# SHALLOW copies: a new outer list (4 ways)
a = [1, 2, 3]
c1 = a.copy()
c2 = a[:]
c3 = list(a)
c4 = copy.copy(a)
print(c1 == a, c1 is a)             # True False
print(c2 is a, c3 is a, c4 is a)    # False False False

# For simple items (numbers, strings) a shallow copy is enough
orig = [1, 2, 3]
cp = orig.copy()
cp[0] = 99
print(orig, cp)                     # [1, 2, 3] [99, 2, 3]

# TRAP: a shallow copy SHARES the inner lists
nested = [[1, 2], [3]]
shallow = nested.copy()
shallow[0].append(99)
print(nested)                       # [[1, 2, 99], [3]]    the original changed too!
print(shallow[0] is nested[0])      # True

# DEEP copy: copies everything inside as well
original = [[1, 2], [3]]
deep = copy.deepcopy(original)
deep[0].append(99)
print(original)                     # [[1, 2], [3]]
print(deep)                         # [[1, 2, 99], [3]]

# Protect the caller's list inside a function
def add_safe(lst):
    lst = lst.copy()                # work on a copy
    lst.append(1)
    return lst

data = []
new = add_safe(data)
print(data, new)                    # [] [1]

# Replace the contents in place (every name sees the change)
nums = [1, 2, 3]
alias = nums
nums[:] = [9, 9]
print(alias)                        # [9, 9]
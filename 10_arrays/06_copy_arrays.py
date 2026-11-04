import copy
from array import array

# Assignment does NOT copy
a = array("i", [1, 2, 3])
b = a
b.append(4)
print(a)                                    # array('i', [1, 2, 3, 4])
print(a is b)                               # True

# A slice makes a new array
c = a[:]
print(c == a, c is a)                       # True False
c[0] = 99
print(a, c)                                 # array('i', [1, 2, 3, 4]) array('i', [99, 2, 3, 4])

# Other ways to copy
d = copy.copy(a)
e = array(a.typecode, a)
f = copy.deepcopy(a)
print(d == a, e == a, f == a)               # True True True
print(d is a, e is a, f is a)               # False False False

# An array holds plain numbers, so a copy is always fully independent:
# there is no "shallow copy" trap like with nested lists.

# Copy to a list, and back
as_list = a.tolist()
print(as_list)                              # [1, 2, 3, 4]
print(array("i", as_list) == a)             # True

# Copy a part
print(a[1:3])                               # array('i', [2, 3])

# Protect the caller's array inside a function
def with_item(arr, x):
    arr = arr[:]
    arr.append(x)
    return arr

orig = array("i", [1])
new = with_item(orig, 2)
print(orig, new)                            # array('i', [1]) array('i', [1, 2])

# Replace the contents in place (every name sees the change)
x = array("i", [1, 2])
alias = x
x[:] = array("i", [7, 8, 9])
print(alias)                                # array('i', [7, 8, 9])
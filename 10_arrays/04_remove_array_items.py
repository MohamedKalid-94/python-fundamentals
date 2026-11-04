from array import array

a = array("i", [1, 2, 3, 2, 4])

# remove(x): delete the FIRST item equal to x
a.remove(2)
print(a)                                    # array('i', [1, 3, 2, 4])

try:
    a.remove(99)
except ValueError as e:
    print(type(e).__name__)                 # ValueError

# pop(i): delete AND RETURN an item (the last one by default)
print(a.pop(), a)                           # 4 array('i', [1, 3, 2])
print(a.pop(0), a)                          # 1 array('i', [3, 2])

try:
    array("i").pop()
except IndexError as e:
    print(e)                                # pop from empty array

try:
    array("i", [1, 2]).pop(5)
except IndexError as e:
    print(e)                                # pop index out of range

# del: by index or slice
del a[0]
print(a)                                    # array('i', [2])

b = array("i", range(6))
del b[1:3]
print(b)                                    # array('i', [0, 3, 4, 5])
del b[::2]                                  # removes the items at index 0 and 2
print(b)                                    # array('i', [3, 5])

# There is NO clear() method: delete everything with a full slice
del b[:]
print(b)                                    # array('i')

# Remove ALL occurrences: build a new array, or replace the contents in place
values = array("i", [1, 2, 3, 2, 4, 2])
values[:] = array("i", [v for v in values if v != 2])
print(values)                               # array('i', [1, 3, 4])

# TRAP: removing while looping skips items (same as lists)
c = array("i", [1, 2, 2, 3])
for v in c:
    if v == 2:
        c.remove(v)
print(c)                                    # array('i', [1, 2, 3])

# FIX: loop over a copy
c = array("i", [1, 2, 2, 3])
for v in c[:]:
    if v == 2:
        c.remove(v)
print(c)                                    # array('i', [1, 3])

# Stack: append to push, pop() to pop
stack = array("i")
stack.append(1)
stack.append(2)
print(stack.pop(), stack.pop())             # 2 1
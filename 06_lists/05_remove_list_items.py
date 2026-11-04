# remove(x): delete the FIRST item equal to x
nums = [1, 2, 3, 2]
nums.remove(2)
print(nums)                         # [1, 3, 2]
try:
    nums.remove(99)
except ValueError as e:
    print(e)                        # list.remove(x): x not in list

# pop(): delete AND RETURN an item (the last one by default)
lst = [1, 2, 3]
print(lst.pop(), lst)               # 3 [1, 2]
print(lst.pop(0), lst)              # 1 [2]

try:
    [].pop()
except IndexError as e:
    print(e)                        # pop from empty list
try:
    [1, 2].pop(5)
except IndexError as e:
    print(e)                        # pop index out of range

# del: delete by index or slice (no value returned)
data = [0, 1, 2, 3, 4, 5]
del data[0]
print(data)                         # [1, 2, 3, 4, 5]
del data[1:3]
print(data)                         # [1, 4, 5]
del data[::2]                       # removes the items at index 0 and 2
print(data)                         # [4]
del data[:]                         # empties the list
print(data)                         # []

# clear(): empty the list
x = [1, 2]
x.clear()
print(x)                            # []

# Remove ALL occurrences: build a new list without them
nums = [1, 2, 3, 2, 4, 2]
nums = [n for n in nums if n != 2]
print(nums)                         # [1, 3, 4]

# TRAP: removing while looping skips items
nums = [1, 2, 2, 3]
for n in nums:
    if n == 2:
        nums.remove(n)
print(nums)                         # [1, 2, 3]    one 2 survived!

# FIX: loop over a copy
nums = [1, 2, 2, 3]
for n in nums[:]:
    if n == 2:
        nums.remove(n)
print(nums)                         # [1, 3]

# Stack (last in, first out) and queue (first in, first out)
stack = []
stack.append(1); stack.append(2); stack.append(3)
print(stack.pop())                  # 3

queue = [1, 2, 3]
print(queue.pop(0))                 # 1      (slow for big lists; Module 17 has deque)
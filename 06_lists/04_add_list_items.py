# append(x): add ONE item at the end
fruits = ["apple"]
fruits.append("banana")
print(fruits)                       # ['apple', 'banana']

nums = [1, 2, 3]
nums.append([4, 5])                 # the whole list becomes ONE item
print(nums)                         # [1, 2, 3, [4, 5]]

# extend(iterable): add EACH item of the iterable
nums = [1, 2, 3]
nums.extend([4, 5])
print(nums)                         # [1, 2, 3, 4, 5]

letters = ["a"]
letters.extend("bc")                # a string is an iterable of characters
print(letters)                      # ['a', 'b', 'c']

nums.extend((6,))
nums.extend(range(7, 9))
print(nums)                         # [1, 2, 3, 4, 5, 6, 7, 8]

# insert(index, x): add at a position
lst = [1, 2, 3]
lst.insert(1, "x")
print(lst)                          # [1, 'x', 2, 3]
lst.insert(100, "end")              # beyond the end: goes to the end
print(lst)                          # [1, 'x', 2, 3, 'end']
lst.insert(-1, "pre")               # -1 inserts BEFORE the last item
print(lst)                          # [1, 'x', 2, 3, 'pre', 'end']

# + creates a NEW list; += extends in place
a = [1, 2]
b = a + [3]
print(a, b)                         # [1, 2] [1, 2, 3]

c = [1, 2]
alias = c
c += [3]
print(alias)                        # [1, 2, 3]    (same list was extended)

# Insert several items with slice assignment
lst = [1, 2, 3, 4]
lst[2:2] = ["a", "b"]
print(lst)                          # [1, 2, 'a', 'b', 3, 4]

# Repetition
print([1, 2] * 2)                   # [1, 2, 1, 2]

# TRAP: these methods return None, so never assign their result
result = nums.append(9)
print(result)                       # None

# Building a list in a loop
squares = []
for i in range(5):
    squares.append(i * i)
print(squares)                      # [0, 1, 4, 9, 16]

# Speed: append() is fast. insert(0, x) shifts every item (slow for big lists).
lst = [3, 1, 2]

lst.append(4)
print(lst)                          # [3, 1, 2, 4]
lst.extend([5, 6])
print(lst)                          # [3, 1, 2, 4, 5, 6]
lst.insert(0, 0)
print(lst)                          # [0, 3, 1, 2, 4, 5, 6]
lst.remove(3)
print(lst)                          # [0, 1, 2, 4, 5, 6]
print(lst.pop(), lst)               # 6 [0, 1, 2, 4, 5]
print(lst.index(2))                 # 2
print(lst.count(1))                 # 1
lst.sort(reverse=True)
print(lst)                          # [5, 4, 2, 1, 0]
lst.reverse()
print(lst)                          # [0, 1, 2, 4, 5]
backup = lst.copy()
lst.clear()
print(lst, backup)                  # [] [0, 1, 2, 4, 5]

# Built-in functions that work on lists
nums = [4, 8, 1]
print(len(nums), min(nums), max(nums), sum(nums))   # 3 1 8 13
print(sorted(nums), list(reversed(nums)))           # [1, 4, 8] [1, 8, 4]
print(any([0, 1]), all([1, 0]))                     # True False
print(list(enumerate(nums)))                        # [(0, 4), (1, 8), (2, 1)]
print(list(zip(nums, "abc")))                       # [(4, 'a'), (8, 'b'), (1, 'c')]

# All the list methods
print([m for m in dir(list) if not m.startswith("_")])
# ['append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
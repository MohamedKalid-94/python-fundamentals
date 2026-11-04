# sort()   changes the list IN PLACE and returns None
# sorted() returns a NEW sorted list and leaves the original alone

nums = [3, 1, 4, 1, 5]
print(sorted(nums))                 # [1, 1, 3, 4, 5]
print(nums)                         # [3, 1, 4, 1, 5]

nums.sort()
print(nums)                         # [1, 1, 3, 4, 5]
nums.sort(reverse=True)
print(nums)                         # [5, 4, 3, 1, 1]

# TRAP: sort() returns None
x = [2, 1].sort()
print(x)                            # None

# Strings sort by code point: uppercase comes before lowercase
words = ["banana", "apple", "Cherry"]
print(sorted(words))                # ['Cherry', 'apple', 'banana']
print(sorted(words, key=str.lower)) # ['apple', 'banana', 'Cherry']

# key= takes a function that gives the value to sort by
print(sorted(["pear", "fig", "apple", "kiwi"], key=len))
# ['fig', 'pear', 'kiwi', 'apple']       (ties keep their original order)

# Numbers stored as text
print(sorted(["10", "9", "2"]))             # ['10', '2', '9']
print(sorted(["10", "9", "2"], key=int))    # ['2', '9', '10']

# Sorting tuples by a field (lambda is covered in Module 17: read it as a tiny function)
students = [("Ann", 90), ("Bob", 85), ("Cy", 90)]
print(sorted(students, key=lambda s: s[1]))
# [('Bob', 85), ('Ann', 90), ('Cy', 90)]
print(sorted(students, key=lambda s: s[1], reverse=True))
# [('Ann', 90), ('Cy', 90), ('Bob', 85)]

# Several keys: put them in a tuple (highest score first, then name A to Z)
students2 = [("Cy", 90), ("Ann", 90), ("Bob", 85)]
print(sorted(students2, key=lambda s: (-s[1], s[0])))
# [('Ann', 90), ('Cy', 90), ('Bob', 85)]

# itemgetter is a faster, readable alternative to lambda
from operator import itemgetter
print(sorted(students, key=itemgetter(1)))
# [('Bob', 85), ('Ann', 90), ('Cy', 90)]

# reverse() flips the current order (it does NOT sort)
r = [1, 3, 2]
r.reverse()
print(r)                            # [2, 3, 1]

# Mixed types cannot be compared
try:
    sorted([3, "a"])
except TypeError as e:
    print(type(e).__name__)         # TypeError

# Largest three values
scores = [55, 90, 72, 88, 61]
print(sorted(scores, reverse=True)[:3])     # [90, 88, 72]

# Facts
# - Sorting is STABLE: equal items keep their original order.
# - It takes O(n log n) time (Timsort).
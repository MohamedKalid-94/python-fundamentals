# LOOPS repeat a block.
#   for   : go through the items of a sequence (known number of items)
#   while : repeat as long as a condition is true (unknown number of repeats)

# Loop over a list
for fruit in ["apple", "banana", "cherry"]:
    print(fruit)
# apple
# banana
# cherry

# Loop over a string
for ch in "abc":
    print(ch, end=" ")
print()                         # a b c

# range(stop), range(start, stop), range(start, stop, step)
print(*range(5))                # 0 1 2 3 4
print(*range(1, 6))             # 1 2 3 4 5
print(*range(0, 10, 2))         # 0 2 4 6 8
print(*range(5, 0, -1))         # 5 4 3 2 1
print(list(range(3)))           # [0, 1, 2]   (range is lazy; list() builds it)

# Accumulator pattern
total = 0
for n in [1, 2, 3, 4]:
    total += n
print(total)                    # 10

# enumerate: index + value
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits, start=1):
    print(index, fruit)
# 1 apple
# 2 banana
# 3 cherry

# zip: loop over several sequences together
names = ["Ann", "Bob"]
scores = [90, 80]
for name, score in zip(names, scores):
    print(name, score)
# Ann 90
# Bob 80

# Dictionaries
d = {"a": 1, "b": 2}
for key in d:
    print(key, end=" ")
print()                         # a b
for key, value in d.items():
    print(key, value)
# a 1
# b 2

# reversed and sorted
print(*reversed([1, 2, 3]))     # 3 2 1
print(*sorted([3, 1, 2]))       # 1 2 3

# "_" means "I don't need the variable"
for _ in range(2):
    print("hi")
# hi
# hi

# The loop variable survives after the loop
for i in range(3):
    pass
print(i)                        # 2

# Do NOT change a list while looping over it. Loop over a copy instead.
nums = [1, 2, 3, 4]
for x in nums[:]:               # nums[:] is a copy
    if x % 2 == 0:
        nums.remove(x)
print(nums)                     # [1, 3]

# Style: prefer "for item in items" over "for i in range(len(items))"
fruits = ["apple", "banana", "cherry"]

# 1. Loop over the items (the idiomatic way)
for fruit in fruits:
    print(fruit)
# apple
# banana
# cherry

# 2. Loop with the index
for i in range(len(fruits)):
    print(i, fruits[i])
# 0 apple
# 1 banana
# 2 cherry

# 3. enumerate: index and item together
for i, fruit in enumerate(fruits, start=1):
    print(i, fruit)
# 1 apple
# 2 banana
# 3 cherry

# 4. while loop with a counter
i = 0
while i < len(fruits):
    print(fruits[i], end=" ")
    i += 1
print()                             # apple banana cherry

# 5. Two lists together
names = ["Ann", "Bob"]
ages = [30, 25]
for name, age in zip(names, ages):
    print(name, age)
# Ann 30
# Bob 25

# 6. Reversed and sorted views (the original list is unchanged)
for f in reversed(fruits):
    print(f, end=" ")
print()                             # cherry banana apple

for f in sorted(fruits, reverse=True):
    print(f, end=" ")
print()                             # cherry banana apple

# 7. Counting backwards over indexes
for i in range(len(fruits) - 1, -1, -1):
    print(i, end=" ")
print()                             # 2 1 0

# 8. Nested lists
matrix = [[1, 2, 3], [4, 5, 6]]
for row in matrix:
    print(*row)
# 1 2 3
# 4 5 6

# 9. A list of tuples, unpacked
pairs = [("a", 1), ("b", 2)]
for letter, number in pairs:
    print(letter, number)
# a 1
# b 2

# 10. Accumulate
total = 0
for n in [1, 2, 3, 4]:
    total += n
print(total)                        # 10

# 11. Change items through the index
for i, f in enumerate(fruits):
    fruits[i] = f.upper()
print(fruits)                       # ['APPLE', 'BANANA', 'CHERRY']

# Do not add or remove items from the list you are looping over.
# Loop over a copy (fruits[:]) or build a new list instead.
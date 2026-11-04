fruits = ("apple", "banana", "cherry")

# 1. Items
for f in fruits:
    print(f)
# apple
# banana
# cherry

# 2. Index
for i in range(len(fruits)):
    print(i, fruits[i])
# 0 apple
# 1 banana
# 2 cherry

# 3. enumerate
for i, f in enumerate(fruits, start=1):
    print(i, f)
# 1 apple
# 2 banana
# 3 cherry

# 4. while
i = 0
while i < len(fruits):
    print(fruits[i], end=" ")
    i += 1
print()                                 # apple banana cherry

# 5. Two tuples together
for n, a in zip(("Ann", "Bob"), (30, 25)):
    print(n, a)
# Ann 30
# Bob 25

# 6. Reversed and sorted (the tuple itself is unchanged)
for f in reversed(fruits):
    print(f, end=" ")
print()                                 # cherry banana apple

for f in sorted(fruits, reverse=True):
    print(f, end=" ")
print()                                 # cherry banana apple

# 7. Tuple of tuples
grid = ((1, 2, 3), (4, 5, 6))
for row in grid:
    print(*row)
# 1 2 3
# 4 5 6

# 8. Accumulate
total = 0
for v in (1, 2, 3, 4):
    total += v
print(total)                            # 10

# 9. A list of tuples, unpacked
points = [(1, 2), (3, 1), (2, 5)]
for x, y in points:
    print(f"x={x}, y={y}")
# x=1, y=2
# x=3, y=1
# x=2, y=5

print(max(points, key=lambda p: p[1]))  # (2, 5)
print(sorted(points))                   # [(1, 2), (2, 5), (3, 1)]   (compared item by item)
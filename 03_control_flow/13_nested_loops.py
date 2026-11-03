# A loop inside a loop: the inner loop runs fully for every outer step

# Multiplication table
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i * j:3}", end="")
    print()
#   1  2  3
#   2  4  6
#   3  6  9

# Star triangle
for i in range(1, 5):
    for j in range(i):
        print("*", end="")
    print()
# *
# **
# ***
# ****

# Pyramid
for i in range(1, 4):
    print(" " * (3 - i) + "*" * (2 * i - 1))
#   *
#  ***
# *****

# All pairs (i < j)
for i in range(3):
    for j in range(i + 1, 3):
        print(i, j)
# 0 1
# 0 2
# 1 2

# 2D data (list of lists)
matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]

total = 0
for row in matrix:
    for value in row:
        total += value
print(total)                    # 45

diagonal = 0
for i in range(3):
    diagonal += matrix[i][i]
print(diagonal)                 # 15

# Cost: the iterations MULTIPLY (this idea becomes "O(n^2)" in problem solving)
count = 0
for i in range(100):
    for j in range(100):
        count += 1
print(count)                    # 10000

# Remember: break and continue only affect the innermost loop.
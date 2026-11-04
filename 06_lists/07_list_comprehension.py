# Syntax:  [expression for item in iterable if condition]
# It builds a new list in one readable line.

squares = [n ** 2 for n in range(6)]
print(squares)                      # [0, 1, 4, 9, 16, 25]

# The same thing with a loop
squares = []
for n in range(6):
    squares.append(n ** 2)

# With a filter
evens = [n for n in range(10) if n % 2 == 0]
print(evens)                        # [0, 2, 4, 6, 8]

# Transform every item
print([w.upper() for w in ["a", "b"]])              # ['A', 'B']
print([len(w) for w in ["apple", "fig"]])           # [5, 3]
print([int(x) for x in "1 2 3".split()])            # [1, 2, 3]

# Filter AND transform
print([n * n for n in range(10) if n % 3 == 0])     # [0, 9, 36, 81]

# if-else INSIDE the expression goes BEFORE the "for"
print(["even" if n % 2 == 0 else "odd" for n in range(4)])
# ['even', 'odd', 'even', 'odd']

# A filter-only "if" goes AFTER the "for"
print([x for x in [3, None, 5] if x is not None])   # [3, 5]

# Characters
print([ch for ch in "hello" if ch not in "aeiou"])  # ['h', 'l', 'l']

# Two loops (read left to right, like nested for loops)
print([(x, y) for x in [1, 2] for y in "ab"])
# [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

# Flatten a matrix
matrix = [[1, 2, 3], [4, 5, 6]]
print([v for row in matrix for v in row])           # [1, 2, 3, 4, 5, 6]

# Transpose a matrix
print([[row[i] for row in matrix] for i in range(3)])
# [[1, 4], [2, 5], [3, 6]]

# A correct 2D grid (separate rows)
print([[0] * 3 for _ in range(2)])                  # [[0, 0, 0], [0, 0, 0]]

# The loop variable does not leak out of the comprehension
try:
    print(n)
except NameError as e:
    print(type(e).__name__)         # NameError

# Same idea for sets, dicts and generators (more in Modules 08, 09 and 17)
print({n % 3 for n in range(10)})                   # {0, 1, 2}
print({w: len(w) for w in ["a", "bb"]})             # {'a': 1, 'bb': 2}
print(sum(n * n for n in range(4)))                 # 14

# RULES
# - Use a comprehension for a simple "build a list" job.
# - If it needs more than one condition or two loops, a normal loop is clearer.
# - Do not use a comprehension only for its side effects (like print).
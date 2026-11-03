# Highest to lowest priority (operators on the same row have equal priority)
#
#  1  ()  []  {}                       grouping and literals
#  2  x[i]  x.attr  f()                indexing, attribute, call
#  3  await
#  4  **                               (right to left)
#  5  +x  -x  ~x                       unary
#  6  *  @  /  //  %
#  7  +  -
#  8  <<  >>
#  9  &
# 10  ^
# 11  |
# 12  in, not in, is, is not, <, <=, >, >=, !=, ==
# 13  not x
# 14  and
# 15  or
# 16  if - else                        (conditional expression)
# 17  lambda
# 18  :=                               (lowest)

print(2 + 3 * 4)           # 14
print((2 + 3) * 4)         # 20

# ** goes right to left
print(2 ** 3 ** 2)         # 512      2 ** (3 ** 2)
print((2 ** 3) ** 2)       # 64

# ** binds tighter than unary minus on its LEFT
print(-2 ** 2)             # -4       -(2 ** 2)
print((-2) ** 2)           # 4
print(2 ** -1)             # 0.5      unary on the right is fine

# Same level goes left to right
print(10 - 4 - 3)          # 3        (10 - 4) - 3
print(100 / 10 / 5)        # 2.0
print(2 * 3 % 4)           # 2        (2 * 3) % 4

# Arithmetic > shifts > bitwise > comparison > not > and > or
print(1 + 2 << 3)          # 24       (1 + 2) << 3
print(8 >> 1 + 1)          # 2        8 >> (1 + 1)
print(1 | 2 & 3)           # 3        1 | (2 & 3)
print(5 > 3 and 2 < 1 or 4 > 2)   # True    ((5 > 3) and (2 < 1)) or (4 > 2)
print(not 1 == 2)          # True     not (1 == 2)
print(1 or 0 and 0)        # 1        1 or (0 and 0)

# BEST PRACTICE: when in doubt, add parentheses
flags = 0b0110
print((flags & 0b0100) != 0)   # True   clear to every reader
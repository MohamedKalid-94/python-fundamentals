a, b = 17, 5

print(a + b)       # 22        addition
print(a - b)       # 12        subtraction
print(a * b)       # 85        multiplication
print(a / b)       # 3.4       true division (ALWAYS returns float)
print(a // b)      # 3         floor division
print(a % b)       # 2         remainder (modulo)
print(a ** b)      # 1419857   power
print(-a, +a)      # -17 17    unary minus / plus

# "/" always gives a float, even when the result is whole
print(10 / 2)      # 5.0
print(type(10 / 2))  # <class 'float'>

# Floor division rounds DOWN (toward negative infinity), not toward zero
print(17 // 5)     # 3
print(-17 // 5)    # -4
print(17 // -5)    # -4

# The sign of % follows the DIVISOR (right-hand side)
print(-17 % 5)     # 3
print(17 % -5)     # -3

# This rule always holds: a == (a // b) * b + (a % b)
print((-17 // 5) * 5 + (-17 % 5))   # -17

print(divmod(17, 5))   # (3, 2)    quotient and remainder together

# Powers and roots
print(2 ** 10)     # 1024
print(2 ** -1)     # 0.5
print(9 ** 0.5)    # 3.0       square root
print(2 ** 100)    # 1267650600228229401496703205376  (no overflow)

# Mixed int and float gives float
print(7.5 // 2)    # 3.0
print(7.5 % 2)     # 1.5
print(1 + 2.0)     # 3.0

# + and * also work on sequences
print("ab" * 3)        # ababab
print("Hi " + "there") # Hi there
print([1, 2] + [3])    # [1, 2, 3]
print([0] * 4)         # [0, 0, 0, 0]

# Division by zero raises an error
try:
    print(1 / 0)
except ZeroDivisionError as e:
    print(type(e).__name__)   # ZeroDivisionError
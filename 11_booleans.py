print(True, False, type(True))             # True False <class 'bool'>
print(True + True)                         # 2  (bool is a number)

# Falsy values: everything else is truthy
print(bool(0), bool(0.0), bool(0j), bool(""), bool([]), bool({}), bool(None))
# False False False False False False False
print(bool(1), bool(-1), bool("0"), bool(" "), bool([0]))
# True True True True True

# Comparisons
print(5 > 3, 5 == 5.0, "a" < "b")         # True True True

# Logical operators
print(True and False, True or False, not True)   # False True False

# 'and' / 'or' return one of their OPERANDS, and short-circuit
print("" or "default")                     # default
print("hi" and "there")                    # there
print(0 and 5)                             # 0
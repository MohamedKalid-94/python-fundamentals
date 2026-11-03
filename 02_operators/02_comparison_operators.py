x, y = 10, 20

print(x == y)      # False   equal
print(x != y)      # True    not equal
print(x > y)       # False
print(x < y)       # True
print(x >= 10)     # True
print(x <= 5)      # False

# Comparisons always return a bool

# CHAINING: a unique Python feature
print(1 < 5 < 10)      # True    same as (1 < 5) and (5 < 10)
print(10 < 5 < 20)     # False
print(1 < 5 > 3)       # True
print(1 == 1 == 1)     # True

age = 25
print(18 <= age <= 65)   # True   much cleaner than C's (age >= 18 && age <= 65)

# Different number types compare by value
print(5 == 5.0)        # True
print(1 == True)       # True    (bool is an int)

# Strings compare character by character using code points
print("apple" < "banana")   # True
print("abc" == "ABC")       # False
print("a" < "B")            # False   (97 is not less than 66)
print("Z" < "a")            # True    (90 < 97)

# Sequences compare element by element
print([1, 2, 3] < [1, 2, 4])   # True
print((1, 2) == (1, 2))        # True
print([1, 2] == (1, 2))        # False   (different types)

# Float trap
print(0.1 + 0.2 == 0.3)        # False

# Incompatible types cannot be ordered
try:
    print(5 < "5")
except TypeError as e:
    print(type(e).__name__)    # TypeError

# == on None works, but "is None" is preferred (see 07_identity_operators.py)
print(None == None)            # True
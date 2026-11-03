# Explicit casting
print(int("42"), int(3.99), int(-3.99), int(True))   # 42 3 -3 1
print(float("3.5"), float(2))                        # 3.5 2.0
print(str(100), str(3.0), str(None))                 # 100 3.0 None
print(int("101", 2), int("ff", 16), int("0x1f", 16)) # 5 255 31
print(bin(10), oct(10), hex(255))                    # 0b1010 0o12 0xff
print(list("abc"), tuple([1, 2]), set([1, 1, 2]))    # ['a', 'b', 'c'] (1, 2) {1, 2}
print(chr(65), ord("A"))                             # A 65
print(complex(1, 2))                                 # (1+2j)

# Truthiness casting
print(bool(0), bool(""), bool([]), bool("False"), bool(-1))
# False False False True True

# Implicit casting (Python widens automatically)
print(1 + 2.5)                        # 3.5   (int -> float)
print(True + 1)                       # 2     (bool -> int)

# Casting can fail. try/except is a preview, covered in Module 14
try:
    int("abc")
except ValueError as e:
    print("ValueError:", e)           # invalid literal for int() with base 10: 'abc'

try:
    int("3.5")                        # a float string cannot go straight to int
except ValueError as e:
    print("ValueError:", e)           # invalid literal for int() with base 10: '3.5'
print(int(float("3.5")))              # 3  (do it in two steps)
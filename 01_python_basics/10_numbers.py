import math
from fractions import Fraction

print(7 / 2, 7 // 2, 7 % 2, 2 ** 10)       # 3.5 3 1 1024
print(-7 // 2, -7 % 2)                     # -4 1  (floor division rounds DOWN)
print(divmod(17, 5))                       # (3, 2)

# int has unlimited size: no overflow (unlike C's int32/int64)
print(2 ** 100)                            # 1267650600228229401496703205376
print(type(2 ** 100))                      # <class 'int'>

print(abs(-5), pow(2, 3), pow(2, 3, 5))    # 5 8 3  (3-arg pow = modulo)
print(round(3.14159, 2), round(2.5), round(3.5))   # 3.14 2 4  (banker's rounding)

print(math.sqrt(16), math.floor(-2.5), math.ceil(2.1))   # 4.0 -3 3
print(math.pi)                             # 3.141592653589793

print(Fraction(1, 3) + Fraction(1, 6))     # 1/2
print(int(True) + int(False))              # 1
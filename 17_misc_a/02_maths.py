import cmath
import math
import random
import statistics
from decimal import Decimal
from fractions import Fraction

# ---------- 1. math: constants and common functions ----------
print(math.pi, math.e, math.tau)                # 3.141592653589793 2.718281828459045 6.283185307179586
print(math.inf, -math.inf, math.isnan(math.nan))                # inf -inf True
print(math.sqrt(16), math.pow(2, 10), math.exp(0), math.log(math.e),
      math.log10(1000), math.log2(8), math.log(8, 2))
# 4.0 1024.0 1.0 1.0 3.0 3.0 3.0

# Rounding: floor goes down, ceil goes up, trunc cuts, round goes to the EVEN neighbour on .5
print(math.floor(-2.5), math.ceil(-2.5), math.trunc(-2.5), round(-2.5))     # -3 -2 -2 -2
print(math.fabs(-3), math.copysign(5, -1))      # 3.0 -5.0

# Integer maths
print(math.factorial(5), math.gcd(12, 18), math.lcm(4, 6), math.comb(5, 2),
      math.perm(5, 2), math.isqrt(17), math.prod([1, 2, 3, 4]))
# 120 6 12 10 20 4 24

# Trigonometry works in RADIANS
print(math.sin(math.pi / 2), math.cos(0), math.degrees(math.pi), math.radians(180))
# 1.0 1.0 180.0 3.141592653589793
print(math.hypot(3, 4), math.dist((0, 0), (3, 4)), round(math.atan2(1, 1), 4))      # 5.0 5.0 0.7854

# Remainders: % follows the sign of the divisor, fmod() follows the sign of the dividend (like C)
print(math.fmod(-7, 3), -7 % 3, math.remainder(7, 3))           # -1.0 2 1.0

# Accurate sums and comparisons of floats
print(sum([0.1] * 10), math.fsum([0.1] * 10))   # 0.9999999999999999 1.0
print(math.isclose(0.1 + 0.2, 0.3), math.isclose(1.0, 1.1, rel_tol=0.2))    # True True

# Domain errors
for bad in (lambda: math.sqrt(-1), lambda: math.log(0)):
    try:
        bad()
    except ValueError as e:
        print(e)                                # math domain error   (printed twice)

# ---------- 2. cmath: complex numbers ----------
print(cmath.sqrt(-1), (1 + 2j) * (3 - 1j), abs(3 + 4j))         # 1j (5+5j) 5.0

# ---------- 3. Integer tools ----------
print(pow(2, 10, 1000), divmod(17, 5), (255).bit_length())      # 24 (3, 2) 8

# ---------- 4. random ----------
random.seed(42)                                 # a fixed seed gives the same sequence every time
print(random.random())                          # 0.6394267984578837

random.seed(1)
first = [random.randint(1, 100) for _ in range(3)]
random.seed(1)
second = [random.randint(1, 100) for _ in range(3)]
print(first == second)                          # True

items = ["a", "b", "c", "d"]
print(random.choice(items) in items, len(random.sample(items, 2)))      # True 2
print(1 <= random.randint(1, 6) <= 6, 5 <= random.uniform(5, 10) <= 10) # True True
shuffled = items[:]
random.shuffle(shuffled)                        # shuffles IN PLACE
print(sorted(shuffled) == items)                # True
# random is NOT secure. For passwords and tokens use the secrets module.

# ---------- 5. statistics ----------
data = [2, 4, 4, 4, 5, 5, 7, 9]
print(statistics.mean(data), statistics.median(data), statistics.mode(data))    # 5 4.5 4
print(statistics.pstdev(data), round(statistics.stdev(data), 3), statistics.pvariance(data))
# 2.0 2.138 4.0         (p = the whole population, no p = a sample)

# ---------- 6. Exact numbers: Decimal and Fraction ----------
print(Decimal("0.1") + Decimal("0.2"), Decimal("2.675").quantize(Decimal("0.01")), Decimal(1) / Decimal(4))
# 0.3 2.68 0.25
print(Fraction(1, 3) + Fraction(1, 6), Fraction(0.75), Fraction(3.14159).limit_denominator(10))
# 1/2 3/4 22/7

# ---------- 7. Embedded-style arithmetic ----------
print((200 + 100) & 0xFF)                       # 44       8-bit wrap-around, as in C

def saturate(value, low=0, high=255):
    return min(max(value, low), high)

print(saturate(300), saturate(-5))              # 255 0    saturating arithmetic

print(round(3.14159 * 256), 804 / 256)          # 804 3.140625     a Q8 fixed-point number
print(round(512 * 3.3 / 1023, 3))               # 1.652    a 10-bit ADC reading in volts
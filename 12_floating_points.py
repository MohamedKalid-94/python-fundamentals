import math
import sys
from decimal import Decimal

print(0.1 + 0.2)                           # 0.30000000000000004
print(0.1 + 0.2 == 0.3)                    # False
print(math.isclose(0.1 + 0.2, 0.3))        # True  (compare floats with this)
print(round(0.1 + 0.2, 2))                 # 0.3

# Exact decimal arithmetic (use for money)
print(Decimal("0.1") + Decimal("0.2"))                          # 0.3
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))        # True

# Why it happens: 0.1 is stored as a binary fraction
print((0.1).as_integer_ratio())            # (3602879701896397, 36028797018963968)

# Special values
print(float("inf"), float("-inf"), float("nan"))   # inf -inf nan
print(float("nan") == float("nan"))        # False  (use math.isnan)
print(math.isnan(float("nan")))            # True
print(1e308 * 10)                          # inf

# Limits
print(sys.float_info.max)                  # 1.7976931348623157e+308
print(sys.float_info.epsilon)              # 2.220446049250313e-16

# Formatting
print(f"{3.14159:.2f}")                    # 3.14
print(f"{1234567.891:,.2f}")               # 1,234,567.89
print(round(2.675, 2))                     # 2.67  (not 2.68, because of binary storage)
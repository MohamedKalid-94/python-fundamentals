a = 0b1100    # 12
b = 0b1010    # 10

print(f"a      = {a:08b}")        # a      = 00001100
print(f"b      = {b:08b}")        # b      = 00001010
print(f"a & b  = {a & b:08b}")    # a & b  = 00001000   AND
print(f"a | b  = {a | b:08b}")    # a | b  = 00001110   OR
print(f"a ^ b  = {a ^ b:08b}")    # a ^ b  = 00000110   XOR
print(f"a << 2 = {a << 2:08b}")   # a << 2 = 00110000   shift left
print(f"a >> 2 = {a >> 2:08b}")   # a >> 2 = 00000011   shift right

print(a & b, a | b, a ^ b)        # 8 14 6
print(a << 2, a >> 2)             # 48 3

# NOT (~): Python ints have infinite width, so ~x == -x - 1
print(~5)                         # -6
print(~0)                         # -1
print(~-1)                        # 0
print(f"{~a & 0xFF:08b}")         # 11110011   mask to 8 bits to see the "C result"

# Negative numbers: use a mask to see the two's complement bits
print(bin(-5))                    # -0b101   (bin() shows sign + magnitude)
print(-5 & 0xFF)                  # 251
print(f"{-5 & 0xFF:08b}")         # 11111011

# Shifts are multiplication / division by powers of 2
print(5 << 1, 20 >> 1)            # 10 10
print(1 << 10)                    # 1024
print(1 << 100)                   # 1267650600228229401496703205376   (no overflow)
print(-16 >> 2)                   # -4      (arithmetic shift keeps the sign)

# --- Register-style bit manipulation ---
reg = 0b0000_0000
reg |= (1 << 3)                   # SET bit 3
print(f"{reg:08b}")               # 00001000
reg |= (1 << 0)                   # SET bit 0
print(f"{reg:08b}")               # 00001001
reg &= ~(1 << 3)                  # CLEAR bit 3
print(f"{reg:08b}")               # 00000001
reg ^= (1 << 5)                   # TOGGLE bit 5
print(f"{reg:08b}")               # 00100001
print(bool(reg & (1 << 5)))       # True    TEST bit 5
print(bool(reg & (1 << 3)))       # False   TEST bit 3

# Useful helpers
print((255).bit_count())          # 8    number of 1 bits (Python 3.10+)
print((255).bit_length())         # 8
print((256).bit_length())         # 9

# Odd / even check
print(5 & 1, 4 & 1)               # 1 0

# GOTCHA 1: "&" is not "and"
print(5 and 3)                    # 3    logical: returns the last truthy operand
print(5 & 3)                      # 1    bitwise: 101 & 011 = 001

# GOTCHA 2 (differs from C): & binds TIGHTER than == in Python
print(5 & 1 == 0)                 # False    means (5 & 1) == 0
print(4 & 1 == 0)                 # True     In C this would parse as 4 & (1 == 0)
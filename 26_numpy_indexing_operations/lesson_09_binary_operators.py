import numpy as np

# BINARY (BITWISE) OPERATORS work on the BITS of integer arrays, element by element.
#   &  np.bitwise_and     |  np.bitwise_or      ^  np.bitwise_xor
#   ~  np.invert          << np.left_shift      >> np.right_shift
# They also work on bool arrays (as logical AND, OR, XOR, NOT): that is how masks are combined.
# Helpers: np.binary_repr, np.unpackbits, np.packbits, np.bitwise_count (number of 1 bits, NumPy 2).

a = np.array([0b1100, 0b1010], dtype=np.uint8)           # 12 and 10
print(a & 0b0110, a | 0b0001, a ^ 0b1111, ~a)
print(np.bitwise_and(a, 6), np.bitwise_or(a, 1), np.bitwise_xor(a, 15), np.invert(a))
print(a << 1, a >> 2, np.left_shift(a, 4), np.right_shift(a, 1))
print(1 << np.arange(8))                                 # the bit values 1, 2, 4 ... 128

# Looking at bits
print(np.binary_repr(10), np.binary_repr(10, width=8), np.binary_repr(-3, width=8))
print(np.unpackbits(np.array([5], dtype=np.uint8)))      # one byte to 8 bits, most significant bit first
print(np.packbits([1, 0, 1, 0, 0, 0, 0, 1]))             # 8 bits back to one byte
print(np.bitwise_count(np.array([0, 1, 7, 255], dtype=np.uint8)))     # how many bits are set

# A status register: test, set, clear and toggle bits in many readings at once
STATUS = np.array([0b10110001, 0b00000000, 0b10000001], dtype=np.uint8)
READY, ERROR, BUSY = 0b00000001, 0b00010000, 0b10000000
print((STATUS & READY) != 0)                             # is the READY bit set?
print((STATUS & BUSY).astype(bool))
print((STATUS & ERROR) == 0)
STATUS |= ERROR                                          # set the ERROR bit everywhere
print([format(int(v), "08b") for v in STATUS])
STATUS &= 0b11111110                                     # clear bit 0 (READY)
print([format(int(v), "08b") for v in STATUS])
STATUS ^= BUSY                                           # toggle the BUSY bit
print([format(int(v), "08b") for v in STATUS])

# Careful: Python's ~1 is -2, which does not fit in a uint8
try:
    STATUS & ~READY
except OverflowError as error:
    print("OverflowError:", error)
print(STATUS & np.uint8(~READY & 0xFF))                  # build the mask in 8 bits instead

# Extracting a bit field: bits 4 to 6 of every value
word = np.array([0b0101_1010, 0b0011_0000], dtype=np.uint8)
print((word >> 4) & 0b111)

# Shifts and multiplication: a left shift by n multiplies by 2**n, a right shift divides (floor)
print(np.array([3, 5]) << 2, np.array([-7, 7]) >> 1)

# EXPECTED OUTPUT
# [4 2] [13 11] [3 5] [243 245]
# [4 2] [13 11] [3 5] [243 245]
# [24 20] [3 2] [192 160] [6 5]
# [  1   2   4   8  16  32  64 128]
# 1010 00001010 11111101
# [0 0 0 0 0 1 0 1]
# [161]
# [0 1 3 8]
# [ True False  True]
# [ True False  True]
# [False  True  True]
# ['10110001', '00010000', '10010001']
# ['10110000', '00010000', '10010000']
# ['00110000', '10010000', '00010000']
# OverflowError: Python integer -2 out of bounds for uint8
# [ 48 144  16]
# [5 3]
# [12 20] [-4  3]
from array import array
import sys

# array(typecode, initializer)
nums = array("i", [1, 2, 3, 4])
print(nums)                                 # array('i', [1, 2, 3, 4])
print(type(nums), len(nums))                # <class 'array.array'> 4
print(nums.typecode, nums.itemsize)         # i 4

# Empty arrays, and other initializers
print(array("d"))                           # array('d')
print(array("B", range(5)))                 # array('B', [0, 1, 2, 3, 4])
print(array("B", b"AB"))                    # array('B', [65, 66])
print(array("f", [1, 2, 3]))                # array('f', [1.0, 2.0, 3.0])

# TYPE CODES (the C types)
#   'b' signed char      1 byte     -128 .. 127
#   'B' unsigned char    1 byte        0 .. 255
#   'h' signed short     2 bytes   -32768 .. 32767
#   'H' unsigned short   2 bytes       0 .. 65535
#   'i' signed int       2 or 4 bytes (4 on most machines)
#   'I' unsigned int     2 or 4 bytes
#   'l' / 'L' long       4 or 8 bytes (depends on the platform)
#   'q' / 'Q' long long  8 bytes
#   'f' float            4 bytes
#   'd' double           8 bytes
print({c: array(c).itemsize for c in "bBhHqQfd"})
# {'b': 1, 'B': 1, 'h': 2, 'H': 2, 'q': 8, 'Q': 8, 'f': 4, 'd': 8}

print(array("b", [-128, 127]))              # array('b', [-128, 127])

# The type is ENFORCED: wrong type or out-of-range values are rejected
for code, bad in [("i", [1, "two"]), ("i", [1.5]), ("B", [256]), ("B", [-1])]:
    try:
        array(code, bad)
    except (TypeError, OverflowError) as e:
        print(code, bad, "->", type(e).__name__)
# i [1, 'two'] -> TypeError
# i [1.5] -> TypeError
# B [256] -> OverflowError
# B [-1] -> OverflowError

# Equality compares the items, but an array is never equal to a list
print(array("i", [1, 2]) == array("i", [1, 2]))     # True
print(array("i", [1, 2]) == [1, 2])                 # False

# Arrays are mutable and have a truth value like other sequences
print(bool(array("i")), bool(array("i", [0])))      # False True

# Packed storage uses far less memory than a list of numbers
big_list = list(range(1000))
big_array = array("i", range(1000))
print(sys.getsizeof(big_array) < sys.getsizeof(big_list))   # True
x = 10
x += 5;   print(x)    # 15      x = x + 5
x -= 3;   print(x)    # 12
x *= 2;   print(x)    # 24
x /= 4;   print(x)    # 6.0     "/" makes it a float
x //= 4;  print(x)    # 1.0

x = 17
x %= 5;   print(x)    # 2
x **= 3;  print(x)    # 8

# Bitwise versions
x = 12
x &= 10;  print(x)    # 8       1100 & 1010 = 1000
x |= 3;   print(x)    # 11      1000 | 0011 = 1011
x ^= 5;   print(x)    # 14      1011 ^ 0101 = 1110
x <<= 1;  print(x)    # 28
x >>= 2;  print(x)    # 7

# Chained and multiple assignment
a = b = c = 0
print(a, b, c)         # 0 0 0
p, q = 1, 2
print(p, q)            # 1 2

# GOTCHA 1: += on a mutable object changes it IN PLACE
nums = [1, 2]
before = id(nums)
nums += [3]
print(nums, id(nums) == before)    # [1, 2, 3] True

# ...but on an immutable object it creates a NEW object
text = "hi"
before = id(text)
text += "!"
print(text, id(text) == before)    # hi! False

# GOTCHA 2: aliases see in-place changes
a = [1, 2]
b = a
b += [3]
print(a)               # [1, 2, 3]   (a changed too!)

c = a
c = c + [4]            # builds a NEW list, so a is untouched
print(a)               # [1, 2, 3]
print(c)               # [1, 2, 3, 4]

# GOTCHA 3: there is NO ++ or -- in Python
n = 5
print(++n, --n)        # 5 5    (just +(+n) and -(-n), n is unchanged)
n += 1                 # the Python way
print(n)               # 6
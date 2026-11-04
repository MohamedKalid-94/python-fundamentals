from array import array

a = array("i", [1, 2, 3, 4, 5])

# 1. Slicing: a NEW reversed array
b = a[::-1]
print(b, a)                                 # array('i', [5, 4, 3, 2, 1]) array('i', [1, 2, 3, 4, 5])

# 2. reverse(): in place
a.reverse()
print(a)                                    # array('i', [5, 4, 3, 2, 1])

# 3. reversed(): an iterator
print(array("i", reversed(a)))              # array('i', [1, 2, 3, 4, 5])
print(list(reversed(a)))                    # [1, 2, 3, 4, 5]

# 4. Two pointers, by hand (the way you would do it in C)
def reverse_in_place(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

data = array("i", [1, 2, 3, 4, 5, 6])
reverse_in_place(data)
print(data)                                 # array('i', [6, 5, 4, 3, 2, 1])

# 5. Reverse only a part
p = array("i", [1, 2, 3, 4, 5])
p[1:4] = p[1:4][::-1]
print(p)                                    # array('i', [1, 4, 3, 2, 5])

# 6. Palindrome check
q = array("i", [1, 2, 1])
print(q == q[::-1])                         # True

# 7. Rotate left by k
r = array("i", [1, 2, 3, 4, 5])
k = 2
print(r[k:] + r[:k])                        # array('i', [3, 4, 5, 1, 2])

# reverse() flips the ORDER of the items.
# byteswap() flips the BYTES inside each item (endianness change).
h = array("H", [1, 256])
h.byteswap()
print(h)                                    # array('H', [256, 1])
h.reverse()
print(h)                                    # array('H', [1, 256])
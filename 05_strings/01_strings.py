# Creating strings
s1 = 'single quotes'
s2 = "double quotes"
print(s1, "|", s2)              # single quotes | double quotes

# Use the other kind of quote inside a string
print("It's fine")              # It's fine
print('He said "hi"')           # He said "hi"

# Triple quotes: multi-line strings
note = """First line
Second line"""
print(note)
# First line
# Second line

# The empty string is falsy
print(bool(""), len(""))        # False 0

# A str is a SEQUENCE of characters
word = "Python"
print(len(word))                # 6
print(type(word))               # <class 'str'>

# Indexing
#   P  y  t  h  o  n
#   0  1  2  3  4  5
#  -6 -5 -4 -3 -2 -1
print(word[0], word[5])         # P n
print(word[-1], word[-6])       # n P

try:
    print(word[6])
except IndexError as e:
    print(e)                    # string index out of range

# Looping over characters
for ch in "abc":
    print(ch, end=" ")
print()                         # a b c

# Membership
print("tho" in word)            # True

# Strings are IMMUTABLE
try:
    word[0] = "J"
except TypeError as e:
    print(e)                    # 'str' object does not support item assignment

# Converting other types with str()
print(str(42) + "!", str(3.5), str(True), str([1, 2]), str(None))
# 42! 3.5 True [1, 2] None

# print() shows the text, repr() shows the exact value with escapes
print("a\tb")                   # a	b    (a tab between)
print(repr("a\tb"))             # 'a\tb'

# == compares CONTENT (in C you would need strcmp)
print("apple" == "apple", "apple" < "banana", "a" == "A")   # True True False

# Adjacent literals join automatically
print("abc" "def")              # abcdef

# Strings are objects with methods
print("hello".upper())          # HELLO
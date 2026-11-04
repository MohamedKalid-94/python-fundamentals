# Syntax: s[start:stop:step]   start is included, stop is EXCLUDED

s = "Hello, World!"
#  H  e  l  l  o  ,     W  o  r  l  d  !
#  0  1  2  3  4  5  6  7  8  9 10 11 12

print(s[0:5])           # Hello
print(s[7:12])          # World
print(s[:5])            # Hello          start defaults to 0
print(s[7:])            # World!         stop defaults to the end
print(s[:])             # Hello, World!  a full copy
print(s[-6:])           # World!
print(s[-6:-1])         # World

# Step
print(s[::2])           # Hlo ol!        every second character
print(s[::-1])          # !dlroW ,olleH  reversed
print(s[::-2])          # !lo olH        reversed, every second
print(s[1:8:2])         # el,W

# Slicing NEVER raises IndexError (indexing does)
print(s[5:100])         # , World!
print(repr(s[20:]))     # ''
print(repr(s[5:2]))     # ''             start after stop gives an empty string

# Last N characters, and removing the ends
print(s[-3:])           # ld!
print(s[1:-1])          # ello, World

# Rule: the two halves rejoin to the original
n = 4
print(s[:n] + s[n:] == s)   # True

# Slice objects can be named and reused
first_five = slice(0, 5)
print(s[first_five])    # Hello

# Practical examples
filename = "report.pdf"
print(filename[-3:], filename[:-4])     # pdf report

date = "2026-11-03"
print(date[:4], date[5:7], date[8:])    # 2026 11 03

print("level"[::-1] == "level")         # True   (palindrome check)

# A slice creates a NEW string; the original is unchanged
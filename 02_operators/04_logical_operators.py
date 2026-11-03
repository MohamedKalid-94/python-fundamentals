# Python uses WORDS: and, or, not   (no &&, ||, !)

# Truth table
for p in (True, False):
    for q in (True, False):
        print(p, q, "->", p and q, p or q)
# True True -> True True
# True False -> False True
# False True -> False True
# False False -> False False

print(not True, not 0, not "")    # False True True

# KEY IDEA: and / or return one of their OPERANDS, not just True/False
print(5 and 3)             # 3       both truthy, so the LAST is returned
print(0 and 3)             # 0       first falsy value is returned
print(5 or 3)              # 5       first truthy value is returned
print(0 or 3)              # 3
print("" or "default")     # default
print(None or [] or "x")   # x
print(1 and 0 and 2)       # 0

# Default value pattern
data = {}
value = data.get("key") or "fallback"
print(value)               # fallback

# Trap: 0 is falsy, so "or" replaces a valid 0
count = 0
print(count or 10)         # 10   (probably not what you wanted)

# SHORT-CIRCUIT: the right side runs only when needed
# (functions are covered in Module 04; just read this one for now)
def check(label, value):
    print("checking", label)
    return value

print(check("A", False) and check("B", True))
# checking A
# False
print(check("C", True) or check("D", False))
# checking C
# True

# Short-circuit as a safe guard
items = []
if items and items[0] == 1:
    print("first item is 1")
else:
    print("skipped, no crash")    # skipped, no crash

# Precedence: not > and > or
print(True or False and False)      # True    (and runs first)
print((True or False) and False)    # False
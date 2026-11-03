# "is" asks: are these the SAME OBJECT?   "==" asks: do they have EQUAL VALUES?

a = [1, 2, 3]
b = a              # b is another name for the same list
c = [1, 2, 3]      # a separate list with equal contents

print(a is b)          # True
print(a is c)          # False
print(a == c)          # True
print(a is not c)      # True
print(id(a) == id(b))  # True     "is" compares id()s

# Always test None with "is"
x = None
print(x is None)       # True
print(x is not None)   # False

# Other singletons: True, False, None
print(True is True)    # True
print(0 == False)      # True
print(0 is False)      # False

# Small integers are cached by CPython (an implementation detail, never rely on it!)
m = int("256"); n = int("256")
print(m is n)          # True
m = int("257"); n = int("257")
print(m is n)          # False    (always use == for numbers)

# Strings built at run time are usually new objects
s1 = "hello"
s3 = "".join(["hel", "lo"])
print(s1 == s3)        # True
print(s1 is s3)        # False    (usually)

# Real use of "is": a sentinel to detect "nothing passed"
# (functions are covered in Module 04; just read it for now)
MISSING = object()

def get(value=MISSING):
    if value is MISSING:
        return "no value given"
    return value

print(get())           # no value given
print(get(None))       # None
print(get(0))          # 0

# Writing "x is 5" gives a SyntaxWarning. Use "x == 5" for values.
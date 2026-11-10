from collections.abc import Iterable

# DYNAMIC TYPING: a variable is just a NAME. The TYPE belongs to the VALUE,
# and it is checked when the code RUNS.

x = 10
print(type(x))                              # <class 'int'>
x = "ten"
print(type(x))                              # <class 'str'>
x = [1]
print(type(x))                              # <class 'list'>

# Python is also STRONGLY typed: it does not silently mix incompatible types
try:
    "5" + 5
except TypeError:
    print("TypeError")                      # TypeError
print(int("5") + 5)                         # 10

# Annotations are hints, NOT checks
def add(a: int, b: int) -> int:
    return a + b

print(add("x", "y"))                        # xy

# One function, many types (this is polymorphism through dynamic typing)
def double(v):
    return v * 2

print(double(3), double("ab"), double([1]))         # 6 abab [1, 1]

# Mistakes appear only when the line RUNS
def shout(v):
    return v.upper()

try:
    shout(5)
except AttributeError:
    print("AttributeError")                 # AttributeError

# Checking types
print(isinstance(True, int), type(True) is int)     # True False   (bool is a subclass of int)
print(isinstance([1], Iterable), isinstance(5, Iterable))   # True False

# LBYL (look before you leap) and EAFP (easier to ask forgiveness than permission)
def safe_len_lbyl(v):
    return len(v) if hasattr(v, "__len__") else -1

def safe_len_eafp(v):
    try:
        return len(v)
    except TypeError:
        return -1

print(safe_len_lbyl([1, 2]), safe_len_lbyl(5))      # 2 -1
print(safe_len_eafp("abc"), safe_len_eafp(5))       # 3 -1

# Embedded-style: serial data arrives as text, so convert by trying
def to_number(raw):
    for convert in (int, float):
        try:
            return convert(raw)
        except ValueError:
            pass
    return None

print(to_number("42"), to_number("3.5"), to_number("abc"))      # 42 3.5 None

# Static typing (C) catches type errors at compile time.
# In Python you add tests, and optionally a checker such as mypy or Pyright that reads
# the annotations (Module 20).
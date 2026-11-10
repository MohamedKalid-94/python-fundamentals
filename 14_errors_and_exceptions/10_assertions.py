# assert condition, "message"
# If the condition is False, Python raises AssertionError.
# Use assert to catch BUGS in your own code (things that must never happen),
# not to check user input.

def average(values):
    assert len(values) > 0, "values must not be empty"
    return sum(values) / len(values)

print(average([1, 2, 3]))                       # 2.0

try:
    average([])
except AssertionError as e:
    print("AssertionError:", e)                 # AssertionError: values must not be empty

# Without a message
try:
    assert 1 > 2
except AssertionError as e:
    print(repr(e))                              # AssertionError()

# Check an invariant after a calculation
def insert_sorted(items, x):
    items = sorted(items + [x])
    assert items == sorted(items)               # this must always be true
    return items

print(insert_sorted([1, 3, 5], 4))              # [1, 3, 4, 5]

# Preconditions with a helpful message
def area(w, h):
    assert w > 0 and h > 0, f"bad size {w}x{h}"
    return w * h

print(area(2, 3))                               # 6
try:
    area(-1, 3)
except AssertionError as e:
    print(e)                                    # bad size -1x3

# Asserts can be REMOVED: python -O script.py skips every assert
print(__debug__)                                # True      (it is False when you run with -O)

# TRAP: the data from outside must be checked with if + raise, never with assert
def set_speed_wrong(speed):
    assert 0 <= speed <= 100                    # disappears with -O, the check is gone!
    return speed

def set_speed(speed):
    if not 0 <= speed <= 100:
        raise ValueError(f"speed out of range: {speed}")
    return speed

# TRAP: a tuple is always true, so this assert can never fail
#   assert (x > 0, "x must be positive")        # SyntaxWarning: assertion is always true
# Write it without the parentheses:
#   assert x > 0, "x must be positive"

# Where assert fits
#   - preconditions and postconditions of internal functions
#   - "this branch can never happen" (assert False, "unreachable")
#   - tests:  assert add(2, 3) == 5  (pytest, Module 20, is built on plain asserts)
# In C this is assert() from <assert.h>, and -O is like defining NDEBUG.
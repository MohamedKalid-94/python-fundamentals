# "in" and "not in" test whether a value is inside a container

# Lists, tuples, sets
print(3 in [1, 2, 3])          # True
print(5 in [1, 2, 3])          # False
print(5 not in [1, 2, 3])      # True
print("b" in ("a", "b"))       # True
print(2 in {1, 2, 3})          # True

# Strings: substring check (case-sensitive)
print("py" in "python")        # True
print("Py" in "python")        # False
print("a" in "banana")         # True
print("" in "abc")             # True    empty string is in every string

# Dictionaries: "in" checks KEYS
d = {"a": 1, "b": 2}
print("a" in d)                # True
print(1 in d)                  # False
print(1 in d.values())         # True
print(("a", 1) in d.items())   # True

# Ranges
print(5 in range(10))          # True
print(10 in range(10))         # False   (range(10) stops at 9)

# Equality is used, so 1.0 matches 1
print(1.0 in [1, 2])           # True
print(None in [None])          # True

# "in" does NOT look inside nested containers
print(2 in [[1, 2], [3]])      # False
print([1, 2] in [[1, 2], [3]]) # True

# "not in" and "not ... in" give the same result
print(not 3 in [1, 2, 3])      # False
print(3 not in [1, 2, 3])      # False   (preferred style)

# The left side must be a string when checking inside a string
try:
    print(1 in "abc")
except TypeError as e:
    print(type(e).__name__)    # TypeError

# Speed note: list search checks items one by one (slow for big data).
# set and dict use hashing (very fast). Use a set for repeated lookups.
allowed = {"admin", "editor", "viewer"}
print("editor" in allowed)     # True
import atexit
import contextlib
import importlib.util
import os
import sys
from contextlib import ExitStack, nullcontext
from functools import total_ordering
from typing import TypedDict

# 1. Ellipsis: the object written ...  (a placeholder, also used in NumPy slices and type hints)
print(..., type(...).__name__)                  # Ellipsis ellipsis

# 2. NotImplemented: "I do not know how to do this with that type, ask the other side"
class A:
    def __eq__(self, other):
        return NotImplemented

a = A()
print(a == A(), a == a)                         # False True         Python falls back to identity
print((1).__add__("a"))                         # NotImplemented
try:
    1 + "a"
except TypeError:
    print("TypeError")                          # TypeError

# 3. String interning: identical strings built at run time are different objects
s1 = "".join(["hello", " world"])
s2 = "".join(["hello", " world"])
print(s1 == s2, s1 is s2, sys.intern(s1) is sys.intern(s2))     # True False True
# Use == for text; "is" only for None, True and False.

# 4. __slots__: no per-object dictionary, so less memory and no accidental new attributes
class P:
    __slots__ = ("x", "y")

p = P()
p.x = 1
print(hasattr(p, "__dict__"))                   # False
try:
    p.z = 3
except AttributeError:
    print("AttributeError")                     # AttributeError

# 5. total_ordering: write __eq__ and ONE comparison, get the rest
@total_ordering
class V:
    def __init__(self, n):
        self.n = n

    def __eq__(self, other):
        return self.n == other.n

    def __lt__(self, other):
        return self.n < other.n

print(V(1) <= V(2), V(3) > V(2))                # True True

# 6. contextlib helpers
log = []
with ExitStack() as stack:                      # a stack of cleanups, run in REVERSE order
    stack.callback(log.append, "closed A")
    stack.callback(log.append, "closed B")
print(log)                                      # ['closed B', 'closed A']
with nullcontext(5) as value:                   # a "with" that does nothing (optional resources)
    print(value)                                # 5

# 7. zip(strict=True) catches lists of different length (Python 3.10+)
try:
    list(zip([1, 2], [1], strict=True))
except ValueError as e:
    print(e)                                    # zip() argument 2 is shorter than argument 1

# 8. Handy one-liners
print(list(zip(*[[1, 2, 3], [4, 5, 6]])))       # [(1, 4), (2, 5), (3, 6)]       transpose a matrix
first, *middle, last = range(5)
print(first, middle, last)                      # 0 [1, 2, 3] 4
print(True + True, 1_000 == 1000, 0b101 | 0o7)  # 2 True 7

# 9. TypedDict: a dictionary with known keys (for type checkers, no cost at run time)
class Movie(TypedDict):
    name: str
    year: int

movie: Movie = {"name": "Alien", "year": 1979}
print(movie, Movie.__annotations__)
# {'name': 'Alien', 'year': 1979} {'name': <class 'str'>, 'year': <class 'int'>}

# 10. The running program looks at itself
print("os" in globals(), callable(globals))     # True True
print(importlib.util.cache_from_source("a.py").endswith(".pyc"))    # True      compiled code lives in __pycache__
print(os.path.isdir(sys.path[0]))               # True     the folder of the script is searched first for imports

# 11. Run something when the program ends
atexit.register(print, "program finished")      # printed LAST, after everything else

# THE GOTCHAS TABLE (you have met most of these in earlier modules)
#   mutable default argument      def f(x, items=[])        use None and create the list inside
#   late-binding in loops         lambda: i                 lambda i=i: i
#   shallow copy                  b = a.copy()              copy.deepcopy(a) for nested data
#   sort() returns None           x = items.sort()          sorted(items) or items.sort() alone
#   "is" with numbers/strings     x is 256                  use ==
#   float equality               0.1 + 0.2 == 0.3          math.isclose
#   changing a list in a loop     for x in items: items.remove(x)     loop over a copy
#   bare except                   except:                   except Exception as e:  (and log it)
#   shadowing a built-in          list = [1, 2]; sum = 3    pick other names
#   circular imports              a imports b, b imports a  move shared code to a third module
#   integer division              7 / 2 gives 3.5           use // for whole numbers
#   modifying a dict in a loop    for k in d: del d[k]      loop over list(d)
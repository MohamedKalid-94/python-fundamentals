import math
from functools import total_ordering

# THE DATA MODEL: the special ("dunder") methods through which your objects plug into the language.
# len(x) calls type(x).__len__(x), "a + b" calls __add__, "with" calls __enter__, "for" calls __iter__ ...
# Implement the right ones and your class behaves like a built-in.

# 1. A complete example: a 2D vector
class Vector:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x, self.y = x, y

    # representation
    def __repr__(self):                         # for developers, ideally valid Python
        return f"Vector({self.x}, {self.y})"

    def __str__(self):                          # for people
        return f"({self.x}, {self.y})"

    def __format__(self, spec):                 # f"{v:.1f}"
        if not spec:
            return str(self)
        return f"({self.x:{spec}}, {self.y:{spec}})"

    # truth, number conversion, hashing, comparison
    def __bool__(self):
        return bool(self.x or self.y)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented               # "ask the other side", Python then falls back to False
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    # arithmetic: __add__, its reflected twin __radd__, __sub__, __mul__ ...
    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __radd__(self, other):                  # makes sum() work: sum starts with 0 + vector
        return self if other == 0 else NotImplemented

    def __sub__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        if not isinstance(k, (int, float)):
            return NotImplemented
        return Vector(self.x * k, self.y * k)

    __rmul__ = __mul__                          # 2 * v

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __matmul__(self, other):                # v @ w, the dot product
        return self.x * other.x + self.y * other.y

    # sequence behaviour: iteration, indexing, length
    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, index):
        return (self.x, self.y)[index]

    def __len__(self):
        return 2

v = Vector(3, 4)
print(v, repr(v), abs(v), bool(Vector(0, 0)))   # (3, 4) Vector(3, 4) 5.0 False
print(v + Vector(1, 1), v - Vector(1, 1), v * 2, 2 * v, -v)     # (4, 5) (2, 3) (6, 8) (6, 8) (-3, -4)
print(v @ Vector(1, 2))                         # 11
x, y = v                                        # unpacking uses __iter__
print(x, y, v[0], len(v), list(v))              # 3 4 3 2 [3, 4]
print(v == Vector(3, 4), v == (3, 4), {v: "a"}[Vector(3, 4)])   # True False a
print(f"{v:.1f}")                               # (3.0, 4.0)
print(sum([Vector(1, 1), Vector(2, 2)]))        # (3, 3)

# 2. In-place operators: += may change the object itself (the same object, new content)
class Bag:
    def __init__(self, items=()):
        self.items = list(items)

    def __iadd__(self, other):                  # b += x
        self.items.extend(other)
        return self

    def __add__(self, other):                   # b + x    (a NEW object)
        return Bag(self.items + list(other))

b = Bag([1])
alias = b
b += [2]
print(alias.items)                              # [1, 2]       the same object was changed
b = b + [3]
print(alias.items, b.items)                     # [1, 2] [1, 2, 3]

# 3. Container methods
class Grid:
    def __init__(self, rows, cols):
        self.rows, self.cols, self.cells = rows, cols, {}

    def __getitem__(self, key):                 # g[row, col]: the key is a tuple
        return self.cells.get(key, 0)

    def __setitem__(self, key, value):
        self.cells[key] = value

    def __len__(self):
        return self.rows

    def __contains__(self, key):
        return key in self.cells

g = Grid(2, 3)
g[0, 1] = 5
print(g[0, 1], g[1, 2], len(g), (0, 1) in g, (1, 1) in g)       # 5 0 2 True False

class Zeros(dict):
    def __missing__(self, key):                 # called by d[key] when the key is absent
        return 0

z = Zeros()
print(z["x"], z.get("x"), "x" in z)             # 0 None False      get() does NOT call __missing__

class OnlyIter:                                 # "in" falls back to iteration
    def __iter__(self):
        return iter([1, 2, 3])

print(2 in OnlyIter(), 5 in OnlyIter())         # True False

class Countdown:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return iter(range(self.n, 0, -1))

    def __reversed__(self):
        return iter(range(1, self.n + 1))

print(list(Countdown(3)), list(reversed(Countdown(3))))         # [3, 2, 1] [1, 2, 3]

# 4. Ordering: write __eq__ and one comparison, total_ordering supplies the others
@total_ordering
class Version:
    def __init__(self, text):
        self.parts = tuple(int(p) for p in text.split("."))

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):
        return self.parts < other.parts

print(Version("1.10") > Version("1.2"), sorted(["1.10", "1.2", "1.9"], key=Version))
# True ['1.2', '1.9', '1.10']

# 5. Making your object usable where an INTEGER index is needed
class Idx:
    def __index__(self):
        return 1

print([10, 20, 30][Idx()], hex(Idx()))          # 20 0x1

# 6. Class-level hooks
class Box:
    def __class_getitem__(cls, item):           # Box[int]  (this is how list[int] works)
        return f"Box of {item.__name__}"

print(Box[int])                                 # Box of int

class Dyn:
    def __dir__(self):                          # what dir() shows
        return ["a", "b"]

print(dir(Dyn()))                               # ['a', 'b']

# 7. Special methods are looked up on the TYPE, not on the object
class A:
    pass

a = A()
a.__len__ = lambda: 5                           # an instance attribute is ignored by len()
try:
    len(a)
except TypeError:
    print("TypeError")                          # TypeError

# WHICH OPERATOR CALLS WHAT
#   a + b __add__ (or b.__radd__)     a - b __sub__     a * b __mul__     a / b __truediv__    a // b __floordiv__
#   a % b __mod__     a ** b __pow__  a @ b __matmul__  a & b __and__       a | b __or__         a ^ b __xor__
#   a << b __lshift__ a >> b __rshift__   -a __neg__   +a __pos__   ~a __invert__   abs(a) __abs__
#   a == b __eq__     a != b __ne__   a < b __lt__      a <= b __le__      a > b __gt__         a >= b __ge__
#   a += b __iadd__ (and so on)       a[i] __getitem__  a[i] = v __setitem__  del a[i] __delitem__
#   len(a) __len__    x in a __contains__   iter(a) __iter__   next(a) __next__   reversed(a) __reversed__
#   a() __call__      with a: __enter__ / __exit__     bool(a) __bool__    hash(a) __hash__
#   int(a) __int__    float(a) __float__    a.__index__ for indexing   round(a) __round__
#   str(a) __str__    repr(a) __repr__      format(a, spec) __format__   copy.copy(a) __copy__
# RULES
#  - Return NotImplemented (not an exception) when you do not know the other type.
#  - __eq__ and __hash__ go together; equal objects must have equal hashes.
#  - Call len(x), str(x), x + y, not x.__len__(): the dunder methods are for DEFINING, not calling.
#  - Python calls this set of methods "protocols": iteration, sequence, mapping, context manager,
#    descriptor, callable ... if your class follows the protocol, every tool that uses it works.
from dataclasses import FrozenInstanceError, dataclass, replace
from functools import lru_cache
from types import MappingProxyType

# An IMMUTABLE object cannot change after it is created. To "change" it, you build a new one.
# Immutable built-ins: int, float, str, bytes, tuple, frozenset, bool, None.

# 1. The errors you get
for action in (lambda: (1, 2).__setitem__(0, 3), lambda: "abc".__setitem__(0, "x")):
    try:
        action()
    except (TypeError, AttributeError) as e:
        print(type(e).__name__)                 # AttributeError  then  AttributeError
try:
    frozenset({1}).add(2)
except AttributeError:
    print("frozenset has no add")               # frozenset has no add

# 2. A tuple is immutable, but what it CONTAINS may not be
t = ([1], 2)
t[0].append(9)
print(t)                                        # ([1, 9], 2)
try:
    hash(t)
except TypeError as e:
    print(e)                                    # unhashable type: 'list'

# 3. A read-only VIEW of a dictionary
base = {"a": 1}
view = MappingProxyType(base)
print(view["a"])                                # 1
try:
    view["b"] = 2
except TypeError:
    print("read-only")                          # read-only
base["b"] = 2                                   # the original can still change ...
print(dict(view))                               # {'a': 1, 'b': 2}    ... and the view follows it

class Settings:
    def __init__(self):
        self._defaults = {"baud": 9600}

    @property
    def defaults(self):
        return MappingProxyType(self._defaults)     # callers can look, not touch

try:
    Settings().defaults["baud"] = 1
except TypeError:
    print("callers cannot change the defaults")     # callers cannot change the defaults

# 4. A frozen dataclass: immutable, hashable, and replace() makes a modified copy
@dataclass(frozen=True)
class Point:
    x: int
    y: int

p = Point(1, 2)
p2 = replace(p, x=10)
print(p, p2)                                    # Point(x=1, y=2) Point(x=10, y=2)
try:
    p.x = 5
except FrozenInstanceError:
    print("FrozenInstanceError")                # FrozenInstanceError
print({p: "a"}[Point(1, 2)])                    # a      frozen dataclasses can be dictionary keys

# 5. Freeze nested data from the outside in
def freeze(obj):
    if isinstance(obj, dict):
        return MappingProxyType({k: freeze(v) for k, v in obj.items()})
    if isinstance(obj, (list, tuple)):
        return tuple(freeze(i) for i in obj)
    if isinstance(obj, set):
        return frozenset(freeze(i) for i in obj)
    return obj

config = freeze({"ports": [1, 2], "db": {"host": "x", "tags": {"a"}}})
print(config["ports"], config["db"]["host"], config["db"]["tags"])     # (1, 2) x frozenset({'a'})
try:
    config["db"]["host"] = "y"
except TypeError:
    print("config is read-only")                # config is read-only

# 6. A persistent (immutable) stack: new versions SHARE the old parts
def push(stack, value):
    return (value, stack)

def to_list(stack):
    items = []
    while stack:
        items.append(stack[0])
        stack = stack[1]
    return items

s1 = push(push(None, 1), 2)
s2 = push(s1, 3)
s3 = push(s1, 4)
print(to_list(s2), to_list(s3), s2[1] is s3[1])         # [3, 2, 1] [4, 2, 1] True
# nothing was copied: s2 and s3 point at the same s1

# 7. An immutable class written by hand
class Vec:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        object.__setattr__(self, "x", x)        # go around our own __setattr__
        object.__setattr__(self, "y", y)

    def __setattr__(self, name, value):
        raise AttributeError(f"{type(self).__name__} is immutable")

    def with_x(self, x):                        # "change" = make a new object
        return Vec(x, self.y)

    def __eq__(self, other):
        return isinstance(other, Vec) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Vec({self.x}, {self.y})"

v = Vec(1, 2)
print(v, v.with_x(9), v)                        # Vec(1, 2) Vec(9, 2) Vec(1, 2)
try:
    v.x = 5
except AttributeError as e:
    print(e)                                    # Vec is immutable
print(len({v, Vec(1, 2)}))                      # 1

# 8. Do not leak your internal list: return an immutable copy
class Inventory:
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)

    @property
    def items(self):
        return tuple(self._items)

inv = Inventory()
inv.add("pen")
snapshot = inv.items
inv.add("ink")
print(snapshot, inv.items)                      # ('pen',) ('pen', 'ink')

# 9. Immutable values are safe default arguments and safe cache keys
def tag_all(names, tags=()):                    # a tuple default cannot be changed by mistake
    return [(n, *tags) for n in names]

print(tag_all(["a"]), tag_all(["a"], ("x",)))   # [('a',)] [('a', 'x')]

@lru_cache(maxsize=None)
def total(numbers):
    return sum(numbers)

print(total((1, 2, 3)))                         # 6
try:
    total([1, 2, 3])
except TypeError:
    print("lists cannot be cache keys")         # lists cannot be cache keys

# 10. Read-only views of bytes
mv = memoryview(b"abc")
print(mv.readonly)                              # True
try:
    mv[0] = 1
except TypeError:
    print("TypeError")                          # TypeError
print(memoryview(bytearray(b"abc")).toreadonly().readonly)      # True

# WHY IMMUTABLE?                                        THE COST
#   hashable: dictionary keys, set members, cache keys   a changed copy must be built (use structural sharing,
#   safe to share between threads without locks          or build with a mutable local, then freeze at the boundary)
#   no surprise changes at a distance (aliasing bugs)
# MUTABLE vs IMMUTABLE PAIRS:  list/tuple  set/frozenset  bytearray/bytes  dict/MappingProxyType
#   dataclass / dataclass(frozen=True)  and  class / NamedTuple
# THIRD-PARTY: pyrsistent and immutables (persistent collections), frozendict, pydantic frozen models.
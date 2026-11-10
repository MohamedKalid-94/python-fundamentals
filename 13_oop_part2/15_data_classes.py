import json
from dataclasses import FrozenInstanceError, asdict, astuple, dataclass, field, fields, replace

# @dataclass writes __init__, __repr__ and __eq__ for you,
# from the annotated fields of the class.

@dataclass
class Point:
    x: int
    y: int = 0                              # a default value


p = Point(1, 2)
print(p)                                    # Point(x=1, y=2)
print(p == Point(1, 2), p == Point(1, 3))   # True False
print(Point(5))                             # Point(x=5, y=0)
p.x = 10                                    # mutable by default
print(p)                                    # Point(x=10, y=2)


# frozen=True: immutable (and hashable)
@dataclass(frozen=True)
class Coord:
    lat: float
    lon: float

c = Coord(1.0, 2.0)
try:
    c.lat = 5
except FrozenInstanceError:
    print("FrozenInstanceError")            # FrozenInstanceError
print({c: 1})                               # {Coord(lat=1.0, lon=2.0): 1}


# order=True: adds <, <=, >, >= (fields compared in order)
@dataclass(order=True)
class Version:
    major: int
    minor: int

print(sorted([Version(2, 0), Version(1, 10), Version(1, 2)]))
# [Version(major=1, minor=2), Version(major=1, minor=10), Version(major=2, minor=0)]


# Mutable defaults need default_factory
@dataclass
class Task:
    name: str
    tags: list = field(default_factory=list)

a, b = Task("x"), Task("y")
a.tags.append("t")
print(a, b)                                 # Task(name='x', tags=['t']) Task(name='y', tags=[])

try:
    @dataclass
    class BadTask:
        items: list = []
except ValueError:
    print("ValueError")                     # a plain mutable default is rejected


# __post_init__: runs after __init__ (validation, computed fields)
@dataclass
class Rect:
    w: float
    h: float
    area: float = field(init=False)

    def __post_init__(self):
        self.area = self.w * self.h

print(Rect(2, 3))                           # Rect(w=2, h=3, area=6)


# Hide a field from repr
@dataclass
class User:
    name: str
    password: str = field(repr=False)

print(User("ann", "secret"))                # User(name='ann')


# Helper functions
q = Point(10, 2)
print(asdict(q), astuple(q), replace(q, y=99))
# {'x': 10, 'y': 2} (10, 2) Point(x=10, y=99)
print([f.name for f in fields(q)])          # ['x', 'y']
print(json.dumps(asdict(q)))                # {"x": 10, "y": 2}


# Inheritance
@dataclass
class Point3D(Point):
    z: int = 0

print(Point3D(1, 2, 3))                     # Point3D(x=1, y=2, z=3)


# kw_only=True (Python 3.10+): every field must be given by name
@dataclass(kw_only=True)
class Opt:
    a: int
    b: int = 2

print(Opt(a=1))                             # Opt(a=1, b=2)
try:
    Opt(1)
except TypeError:
    print("TypeError")                      # TypeError


# A field without a default cannot come after one with a default
try:
    @dataclass
    class Wrong:
        a: int = 1
        b: int
except TypeError:
    print("TypeError")                      # TypeError


# Embedded-style packet with a computed checksum
@dataclass
class Packet:
    header: int
    payload: bytes
    checksum: int = field(init=False)

    def __post_init__(self):
        self.checksum = (self.header + sum(self.payload)) & 0xFF

print(Packet(0xAA, b"\x01\x02"))
# Packet(header=170, payload=b'\x01\x02', checksum=173)
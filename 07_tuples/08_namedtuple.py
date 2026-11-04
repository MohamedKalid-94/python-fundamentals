from collections import namedtuple

# A namedtuple is a tuple whose items also have NAMES.

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)

print(p)                                # Point(x=3, y=4)
print(p.x, p.y)                         # 3 4          access by name
print(p[0], p[1])                       # 3 4          still works by index
x, y = p
print(x, y)                             # 3 4          still unpacks
print(p == (3, 4), isinstance(p, tuple), len(p))        # True True 2

# Create with keywords, in any order
print(Point(y=2, x=1))                  # Point(x=1, y=2)

# Still IMMUTABLE
try:
    p.x = 10
except AttributeError as e:
    print(type(e).__name__)             # AttributeError

# Helpers
p2 = p._replace(x=10)                   # returns a NEW namedtuple
print(p2, p)                            # Point(x=10, y=4) Point(x=3, y=4)
print(p._asdict())                      # {'x': 3, 'y': 4}
print(Point._fields)                    # ('x', 'y')
print(Point._make([7, 8]))              # Point(x=7, y=8)

# Field names can be one string; defaults apply to the RIGHTMOST fields
Point3D = namedtuple("Point3D", "x y z", defaults=[0])
print(Point3D(1, 2))                    # Point3D(x=1, y=2, z=0)

Color = namedtuple("Color", "r g b")
c = Color(255, 128, 0)
print(c)                                # Color(r=255, g=128, b=0)

# Sort by a named field
Person = namedtuple("Person", "name age")
people = [Person("Ann", 30), Person("Bob", 25), Person("Cy", 35)]
print(sorted(people, key=lambda p: p.age)[0])           # Person(name='Bob', age=25)

# Class syntax with type hints (classes are explained in Module 12;
# for now read it as a record definition)
from typing import NamedTuple

class Employee(NamedTuple):
    name: str
    dept: str = "IT"
    salary: float = 0.0

e = Employee("Ann")
print(e)                                # Employee(name='Ann', dept='IT', salary=0.0)
print(e.name, e.dept)                   # Ann IT

# Embedded-style example: a sensor reading
Reading = namedtuple("Reading", "sensor value unit")
r = Reading("temp", 36.5, "C")
print(f"{r.sensor}: {r.value} {r.unit}")        # temp: 36.5 C

# WHEN TO USE WHAT
# namedtuple : small, fixed, read-only record (works wherever a tuple works)
# dict       : keys are not known in advance, or the record must change
# dataclass  : a record with behaviour or changing fields (Module 13)
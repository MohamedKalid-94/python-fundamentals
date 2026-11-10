from collections import UserList
from typing import NewType

# In Java, a "wrapper class" boxes a primitive (int -> Integer).
# In Python there are no primitives: int, float, str and bool are ALREADY objects.
# The word "wrapper" is used here for the classes that WRAP another value or object
# to change or extend it.

# 1. The built-in value types are objects with methods
print((5).__add__(3))                       # 8
print(int("7"), float(3), str(5) + "x", bool(0))        # 7 3.0 5x False


# 2. Wrap a primitive by subclassing it
class Positive(int):
    def __new__(cls, value):
        if value <= 0:
            raise ValueError("must be positive")
        return super().__new__(cls, value)

p = Positive(5)
print(p + 1, isinstance(p, int))            # 6 True
try:
    Positive(-1)
except ValueError:
    print("ValueError")                     # ValueError


class Meters(float):
    def __add__(self, other):
        return Meters(float(self) + float(other))

    def __repr__(self):
        return f"{float(self)}m"

    __str__ = __repr__


print(Meters(2) + Meters(3.5))              # 5.5m


# 3. A wrapper object that forwards unknown attributes to the wrapped object
class Wrapper:
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, name):            # called only when the normal lookup fails
        return getattr(self._obj, name)


w = Wrapper([3, 1, 2])
w.sort()                                    # forwarded to the list
print(w._obj, w.count(1))                   # [1, 2, 3] 1
try:
    len(w)                                  # special methods are NOT forwarded
except TypeError:
    print("TypeError")                      # TypeError


# 4. Extend a built-in container safely with UserList (and UserDict)
class History(UserList):
    def append(self, item):
        print("append", item)
        super().append(item)


h = History()
h.append(1)                                 # append 1
print(h, len(h))                            # [1] 1


# 5. The ADAPTER pattern: wrap an object so it fits the interface you need
class FahrenheitSensor:
    def read_f(self):
        return 212.0


class CelsiusAdapter:
    def __init__(self, sensor):
        self._sensor = sensor

    def read(self):
        return (self._sensor.read_f() - 32) * 5 / 9


print(CelsiusAdapter(FahrenheitSensor()).read())        # 100.0


# 6. NewType: a distinct type name for the type checker (no wrapper at run time!)
UserId = NewType("UserId", int)
print(UserId(5), type(UserId(5)))           # 5 <class 'int'>
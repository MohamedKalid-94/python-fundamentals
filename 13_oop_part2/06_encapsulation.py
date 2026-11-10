from functools import cached_property

# ENCAPSULATION: keep the data inside the object and give controlled access to it.
# In Python the controlled access is a PROPERTY: it looks like an attribute,
# but runs code when you read, write or delete it.

class Temperature:
    def __init__(self, celsius=0):
        self.celsius = celsius              # goes through the setter below

    @property
    def celsius(self):                      # getter
        return self._celsius

    @celsius.setter
    def celsius(self, value):               # setter with validation
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):                   # a computed property
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, f):
        self.celsius = (f - 32) * 5 / 9


t = Temperature(25)
print(t.celsius, t.fahrenheit)              # 25 77.0
t.celsius = 100
print(t.fahrenheit)                         # 212.0
t.fahrenheit = 32
print(t.celsius)                            # 0.0

try:
    t.celsius = -300
except ValueError as err:
    print(err)                              # below absolute zero


# A READ-ONLY property: no setter
class Circle:
    def __init__(self, r):
        self._r = r

    @property
    def area(self):
        return round(3.14159 * self._r ** 2, 2)

c = Circle(2)
print(c.area)                               # 12.57
try:
    c.area = 5
except AttributeError:
    print("AttributeError")                 # AttributeError


# A deleter
class Box:
    def __init__(self):
        self._value = 1

    @property
    def value(self):
        return self._value

    @value.deleter
    def value(self):
        print("deleting")
        del self._value

b = Box()
del b.value                                 # deleting
print(hasattr(b, "_value"))                 # False


# cached_property: computed once, then stored
class Data:
    def __init__(self, values):
        self.values = values

    @cached_property
    def total(self):
        print("computing")
        return sum(self.values)

d = Data([1, 2, 3])
print(d.total)
# computing
# 6
print(d.total)                              # 6       (no "computing" this time)


# Validation keeps the object always valid
class Rect:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("width must be positive")
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("height must be positive")
        self._height = value

    @property
    def area(self):
        return self._width * self._height

r = Rect(2, 3)
try:
    r.width = -1
except ValueError as err:
    print(err)                              # width must be positive
r.width = 5
print(r.area)                               # 15


# Private data with a read-only view
class Counter:
    def __init__(self):
        self.__count = 0

    def increment(self):
        self.__count += 1

    @property
    def count(self):
        return self.__count

k = Counter()
k.increment()
k.increment()
print(k.count)                              # 2
try:
    k.count = 10
except AttributeError:
    print("AttributeError")                 # AttributeError

# PYTHONIC ADVICE
# Start with a plain public attribute. If you later need validation or a computed value,
# turn it into a property: callers keep writing obj.value, so nothing breaks.
# Java-style get_value()/set_value() methods are not needed.
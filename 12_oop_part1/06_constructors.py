# __init__ is the INITIALIZER: it runs right after the object is created.
# (The real constructor is __new__, which you almost never write.)

class Student:
    def __init__(self, name, grade=1, *, school="Unknown"):
        self.name = name
        self.grade = grade
        self.school = school


s1 = Student("Ann")
s2 = Student("Bob", 5, school="ABC")
print(s1.name, s1.grade, s1.school)     # Ann 1 Unknown
print(s2.name, s2.grade, s2.school)     # Bob 5 ABC

try:
    Student()                           # the required argument is missing
except TypeError as err:
    print(type(err).__name__)           # TypeError


# Validate in the constructor, so a bad object can never exist
class Temperature:
    def __init__(self, celsius):
        if celsius < -273.15:
            raise ValueError("below absolute zero")
        self.celsius = celsius

try:
    Temperature(-300)
except ValueError as err:
    print(err)                          # below absolute zero


# __init__ must return None
class BadInit:
    def __init__(self):
        return 5

try:
    BadInit()
except TypeError as err:
    print(type(err).__name__)           # TypeError


# TRAP: a mutable default argument is shared by every object
class Bag:
    def __init__(self, items=[]):
        self.items = items

b1, b2 = Bag(), Bag()
b1.items.append(1)
print(b2.items)                         # [1]

class SafeBag:
    def __init__(self, items=None):
        self.items = [] if items is None else list(items)

c1, c2 = SafeBag(), SafeBag()
c1.items.append(1)
print(c2.items)                         # []


# A class without __init__ still works
class Empty:
    pass

print(Empty().__dict__)                 # {}


# Run other methods from the constructor
class Circle:
    def __init__(self, r):
        self.r = r
        self.area = self._calc_area()

    def _calc_area(self):
        return round(3.14159 * self.r ** 2, 2)

print(Circle(2).area)                   # 12.57


# An embedded-style constructor with defaults
class Uart:
    def __init__(self, port, baud=9600, parity="N", stop_bits=1):
        self.port = port
        self.baud = baud
        self.parity = parity
        self.stop_bits = stop_bits

u = Uart("COM3", 115200)
print(u.port, u.baud, u.parity, u.stop_bits)    # COM3 115200 N 1
print(vars(u))      # {'port': 'COM3', 'baud': 115200, 'parity': 'N', 'stop_bits': 1}


# __new__ creates the object, THEN __init__ fills it
class Foo:
    def __new__(cls):
        print("new")
        return object.__new__(cls)

    def __init__(self):
        print("init")

Foo()
# new
# init


# __del__ is the destructor: it runs when the object is destroyed.
# In CPython this happens as soon as the last reference is gone, but the timing is
# not guaranteed in general. Use "with" (context managers, Module 20) for cleanup.
class Resource:
    def __init__(self, name):
        self.name = name
        print("open", name)

    def __del__(self):
        print("close", self.name)

r = Resource("A")
del r
# open A
# close A
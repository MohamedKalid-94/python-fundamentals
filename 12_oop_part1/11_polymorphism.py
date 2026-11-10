import math

# POLYMORPHISM = "many forms": the same call works on different types of objects.

# 1. Through inheritance: the same method name, different behaviour
class Shape:
    def area(self):
        raise NotImplementedError("subclasses must implement area()")


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return math.pi * self.r ** 2


class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)


shapes = [Circle(2), Rectangle(3, 4), Square(5)]
for s in shapes:
    print(f"{type(s).__name__}: {s.area():.2f}")
# Circle: 12.57
# Rectangle: 12.00
# Square: 25.00

try:
    Shape().area()
except NotImplementedError:
    print("NotImplementedError")        # NotImplementedError


# 2. DUCK TYPING: "if it walks like a duck..." No common parent is needed
class Duck:
    def speak(self):
        return "Quack"

class Robot:
    def speak(self):
        return "Beep"

class Person:
    def speak(self):
        return "Hello"

def make_it_speak(thing):
    return thing.speak()

for obj in (Duck(), Robot(), Person()):
    print(make_it_speak(obj))
# Quack
# Beep
# Hello


# 3. Built-ins are polymorphic too
print(len("abc"), len([1, 2]), len({"a": 1}))       # 3 2 1
print(1 + 2, "a" + "b", [1] + [2])                  # 3 ab [1, 2]
print(max("abc"), max([1, 5, 2]))                   # c 5


# 4. Operator overloading: give your own class the + and == operators
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, k):
        return Vector(self.x * k, self.y * k)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


v1, v2 = Vector(1, 2), Vector(3, 4)
print(v1 + v2)                          # Vector(4, 6)
print(v1 * 3)                           # Vector(3, 6)
print(v1 == Vector(1, 2))               # True

# Defining __eq__ without __hash__ makes the objects unhashable
try:
    {v1}
except TypeError:
    print("unhashable")                 # unhashable


# 5. An embedded-style "driver" interface
class Temp:
    def read(self):
        return 36.5

class Pressure:
    def read(self):
        return 1013

for sensor in (Temp(), Pressure()):
    print(type(sensor).__name__, sensor.read())
# Temp 36.5
# Pressure 1013

# Method overriding and the NotImplementedError pattern are completed in Module 13
# (Abstraction and Interfaces).
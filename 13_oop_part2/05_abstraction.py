from abc import ABC, abstractmethod
import math

# ABSTRACTION: show WHAT an object does, hide HOW.
# An abstract class defines the required methods and cannot be used directly.

class Shape(ABC):
    @abstractmethod
    def area(self):
        ...

    @abstractmethod
    def perimeter(self):
        ...

    def describe(self):                     # a normal (concrete) method can use the abstract ones
        return f"{type(self).__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


try:
    Shape()
except TypeError:
    print("TypeError")                      # cannot instantiate an abstract class


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return math.pi * self.r ** 2

    def perimeter(self):
        return 2 * math.pi * self.r


class Rect(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h

    def perimeter(self):
        return 2 * (self.w + self.h)


print(Circle(1).describe())                 # Circle: area=3.14, perimeter=6.28
print(Rect(2, 3).describe())                # Rect: area=6.00, perimeter=10.00


# A subclass that implements only SOME abstract methods is still abstract
class Half(Shape):
    def area(self):
        return 0

try:
    Half()
except TypeError:
    print("TypeError")                      # TypeError

print(sorted(Shape.__abstractmethods__))    # ['area', 'perimeter']


# An abstract method may have a body that children reuse with super()
class Base(ABC):
    @abstractmethod
    def greet(self):
        return "base"

class Child(Base):
    def greet(self):
        return super().greet() + "+child"

print(Child().greet())                      # base+child


# Abstract properties (properties are explained in the next file)
class Device(ABC):
    @property
    @abstractmethod
    def name(self):
        ...

class Led(Device):
    @property
    def name(self):
        return "LED"

print(Led().name)                           # LED


# An embedded-style abstraction: the application only knows the Transport interface
class Transport(ABC):
    @abstractmethod
    def send(self, data: bytes) -> int:
        ...


class FakeUart(Transport):
    def __init__(self):
        self.sent = []

    def send(self, data):
        self.sent.append(data)
        return len(data)


def transmit(transport, message):
    return transport.send(message.encode())

print(transmit(FakeUart(), "hello"))        # 5

# Abstraction vs encapsulation
#   abstraction   = WHAT you may call (the interface; hide complexity)
#   encapsulation = WHERE the data lives (hide and protect the state), next file
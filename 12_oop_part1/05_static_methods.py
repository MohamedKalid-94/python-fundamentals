# @staticmethod receives NEITHER self NOR cls.
# It is a plain function that lives inside the class because it belongs to the topic.

class Demo:
    def instance_method(self):
        return "instance", type(self).__name__

    @classmethod
    def class_method(cls):
        return "class", cls.__name__

    @staticmethod
    def static_method():
        return "static"


d = Demo()
print(d.instance_method())              # ('instance', 'Demo')
print(d.class_method())                 # ('class', 'Demo')
print(Demo.class_method())              # ('class', 'Demo')
print(d.static_method(), Demo.static_method())      # static static

try:
    Demo.instance_method()
except TypeError as err:
    print(type(err).__name__)           # TypeError


# Utility functions grouped in a class
class MathUtil:
    @staticmethod
    def is_even(n):
        return n % 2 == 0

    @staticmethod
    def clamp(value, low, high):
        return max(low, min(value, high))

    @staticmethod
    def celsius_to_f(c):
        return c * 9 / 5 + 32


print(MathUtil.is_even(4), MathUtil.clamp(15, 0, 10), MathUtil.celsius_to_f(100))
# True 10 212.0


# A helper that belongs to a class
class Person:
    def __init__(self, name, age):
        if not Person.is_valid_age(age):
            raise ValueError("invalid age")
        self.name = name
        self.age = age

    @staticmethod
    def is_valid_age(age):
        return 0 <= age <= 130


print(Person.is_valid_age(30), Person.is_valid_age(-1))     # True False


# Embedded-style helpers: checksums
class Checksum:
    @staticmethod
    def xor_checksum(data):
        result = 0
        for byte in data:
            result ^= byte
        return result

    @staticmethod
    def crc8(data):
        """CRC-8, polynomial 0x07, initial value 0."""
        crc = 0
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = ((crc << 1) ^ 0x07) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
        return crc


print(Checksum.xor_checksum(b"\x01\x02\x04"))       # 7
print(hex(Checksum.crc8(b"123456789")))             # 0xf4     (the standard CRC-8 check value)

# WHICH ONE?
#   needs the object's data       -> instance method (self)
#   needs the class or subclasses -> class method (cls)
#   needs neither                 -> static method (or a plain function in a module)
from functools import singledispatch, singledispatchmethod
from typing import overload

# OVERLOADING (several methods with the same name and different parameters)
# does NOT exist in Python: the LAST definition replaces the earlier ones.

class Calc:
    def add(self, a, b):
        return a + b

    def add(self, a, b, c):                 # replaces the first add()
        return a + b + c


c = Calc()
try:
    c.add(1, 2)
except TypeError:
    print("TypeError")                      # TypeError
print(c.add(1, 2, 3))                       # 6


# WAY 1: default arguments
class Calc2:
    def add(self, a, b, c=0):
        return a + b + c

print(Calc2().add(1, 2), Calc2().add(1, 2, 3))      # 3 6


# WAY 2: *args for any number of arguments
def total(*nums):
    return sum(nums)

print(total(), total(1, 2), total(1, 2, 3))         # 0 3 6


# WAY 3: check the type inside the function
def to_text(value):
    if isinstance(value, (list, tuple)):
        return ", ".join(map(str, value))
    return str(value)

print(to_text([1, 2]), to_text(5))                  # 1, 2 5


# WAY 4: singledispatch picks the version by the TYPE of the first argument
@singledispatch
def describe(x):
    return f"object {x}"

@describe.register(int)
def _(x):
    return f"int {x}"

@describe.register(str)
def _(x):
    return f"str {x!r}"

@describe.register(list)
def _(x):
    return f"list of {len(x)}"

print(describe(5), describe("a"), describe([1, 2]), describe(2.5))
# int 5 str 'a' list of 2 object 2.5


# The same inside a class
class Formatter:
    @singledispatchmethod
    def fmt(self, x):
        return str(x)

    @fmt.register
    def _(self, x: int):
        return f"int:{x}"

    @fmt.register
    def _(self, x: list):
        return f"list:{len(x)}"

f = Formatter()
print(f.fmt(3), f.fmt([1, 2]), f.fmt(2.5))          # int:3 list:2 2.5


# WAY 5: typing.overload only DESCRIBES the variants for type checkers;
# one real function still does the work
@overload
def double(x: int) -> int: ...
@overload
def double(x: str) -> str: ...
def double(x):
    return x * 2

print(double(3), double("ab"))                      # 6 abab


# WAY 6: alternative constructors with class methods (Module 12) and keyword-only options
def connect(host, port=80, *, secure=False):
    return f"{host}:{port} secure={secure}"

print(connect("a.com"), connect("b.com", 443, secure=True))
# a.com:80 secure=False b.com:443 secure=True


# OPERATOR overloading is a different thing: you define what + means for YOUR class
class Money:
    def __init__(self, amount):
        self.amount = amount

    def __add__(self, other):
        if isinstance(other, Money):
            return Money(self.amount + other.amount)
        if isinstance(other, (int, float)):
            return Money(self.amount + other)
        return NotImplemented

    def __radd__(self, other):              # for  10 + Money(1)  and for sum()
        return self + other

    def __repr__(self):
        return f"Money({self.amount})"

print(Money(5) + Money(3), Money(5) + 2, 10 + Money(1))    # Money(8) Money(7) Money(11)
print(sum([Money(1), Money(2)]))                            # Money(3)
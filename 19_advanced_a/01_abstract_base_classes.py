import inspect
from abc import ABC, ABCMeta, abstractmethod
from collections.abc import (Callable, Container, Iterable, Iterator, Mapping, MutableMapping,
                             MutableSequence, Sequence, Sized)
from decimal import Decimal
from fractions import Fraction
from numbers import Integral, Number, Rational, Real

# Module 13 showed how to write an abstract class. Here you see what the standard library does
# with ABCs, and how to use them to get a lot of code for free.

# 1. The ABCs of the standard library describe WHAT an object can do
print(isinstance([], Sequence), isinstance({}, Mapping), isinstance("a", Sequence),
      isinstance({1}, Sequence), isinstance(range(3), Sequence))    # True True True False True
print(isinstance(5, Iterable), isinstance(iter([]), Iterator), isinstance(len, Callable))   # False True True
print(issubclass(list, MutableSequence), issubclass(tuple, MutableSequence), issubclass(dict, Mapping))
# True False True
#   Sized (__len__)  Iterable (__iter__)  Container (__contains__)  Callable (__call__)
#   Sequence, MutableSequence, Mapping, MutableMapping, Set, MutableSet, Iterator, Generator ...

# 2. Subclass an ABC, write a FEW methods, and receive the REST as mixin methods
class Playlist(Sequence):
    def __init__(self, songs):
        self._songs = list(songs)

    def __getitem__(self, index):               # abstract in Sequence
        return self._songs[index]

    def __len__(self):                          # abstract in Sequence
        return len(self._songs)

p = Playlist(["a", "b", "c", "b"])
print(len(p), p[1], p[-1], "b" in p, list(reversed(p)), p.index("b"), p.count("b"))
# 4 b b True ['b', 'c', 'b', 'a'] 1 2
print(list(p), list(p[1:3]))                    # ['a', 'b', 'c', 'b'] ['b', 'c']
# __contains__, __iter__, __reversed__, index() and count() all came from Sequence

class Incomplete(Sequence):
    def __len__(self):
        return 0

try:
    Incomplete()                                # __getitem__ is still abstract
except TypeError:
    print("TypeError")                          # TypeError

# 3. MutableMapping: write 5 methods, get get(), update(), pop(), setdefault(), items(), ==, ...
class LowerDict(MutableMapping):
    """A dictionary whose keys are not case-sensitive."""

    def __init__(self):
        self._data = {}

    def __getitem__(self, key):
        return self._data[key.lower()]

    def __setitem__(self, key, value):
        self._data[key.lower()] = value

    def __delitem__(self, key):
        del self._data[key.lower()]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

d = LowerDict()
d["Name"] = "Ann"
d.update({"CITY": "Pune"})                      # update() came for free
print(d["NAME"], d.get("city"), sorted(d), len(d))                  # Ann Pune ['city', 'name'] 2
print(d.pop("Name"), dict(d), "city" in d)      # Ann {'city': 'Pune'} True
d.setdefault("Zip", "411001")
print(sorted(d.items()))                        # [('city', 'Pune'), ('zip', '411001')]
print(d == {"city": "Pune", "zip": "411001"})   # True      Mapping provides __eq__ too

# 4. __subclasshook__: decide membership by STRUCTURE, with no inheritance and no register()
class Closeable(ABC):
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Closeable:
            if any("close" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented                   # "use the normal rules"

class File:
    def close(self):
        pass

class Socket:
    def close(self):
        pass

print(isinstance(File(), Closeable), isinstance(5, Closeable), issubclass(Socket, Closeable))
# True False True
# (collections.abc.Iterable, Sized and Callable work exactly like this)

# 5. register(): a VIRTUAL subclass (it is not in the MRO and inherits nothing)
class Plugin(ABC):
    @abstractmethod
    def run(self):
        ...

@Plugin.register
class External:
    def run(self):
        return "external"

print(issubclass(External, Plugin), isinstance(External(), Plugin), Plugin in External.__mro__)
# True True False

# 6. Abstract class methods, static methods and properties
class Codec(ABC):
    @classmethod
    @abstractmethod
    def create(cls):
        ...

    @staticmethod
    @abstractmethod
    def checksum(data):
        ...

class XorCodec(Codec):
    @classmethod
    def create(cls):
        return cls()

    @staticmethod
    def checksum(data):
        result = 0
        for byte in data:
            result ^= byte
        return result

print(type(XorCodec.create()).__name__, XorCodec.checksum(b"\x01\x02\x04"))    # XorCodec 7
print(Codec.create())                           # None     abstract means "cannot make an OBJECT", not "cannot call"

# 7. The template-method pattern: the base class fixes the steps, the children fill them in
class Report(ABC):
    def run(self):
        return self.render(self.transform(self.load()))

    @abstractmethod
    def load(self):
        ...

    @abstractmethod
    def transform(self, data):
        ...

    @abstractmethod
    def render(self, rows):
        ...

class CsvReport(Report):
    def load(self):
        return "a,1\nb,2"

    def transform(self, data):
        return [line.split(",") for line in data.splitlines()]

    def render(self, rows):
        return "; ".join(f"{k}={v}" for k, v in rows)

print(CsvReport().run())                        # a=1; b=2

# 8. Questions you can ask about abstractness
class Shape(ABC):
    @abstractmethod
    def area(self):
        ...

class Square(Shape):
    def area(self):
        return 4

print(inspect.isabstract(Shape), inspect.isabstract(Square), sorted(Shape.__abstractmethods__))
# True False ['area']

# 9. The numeric tower: Number > Complex > Real > Rational > Integral
print(isinstance(1, Integral), isinstance(1.5, Integral), isinstance(1.5, Real), isinstance(True, Integral))
# True False True True
print(isinstance(Fraction(1, 2), Rational), isinstance(Decimal("1"), Real), isinstance(Decimal("1"), Number))
# True False True

# 10. What ABC really is
print(type(ABC).__name__, ABC.__class__ is ABCMeta)             # ABCMeta True
# "class X(ABC)" is the same as "class X(metaclass=ABCMeta)" (metaclasses: file 06)

# 11. Abstract methods are checked ONLY when you create an object
class Calc(ABC):
    @abstractmethod
    def f(self):
        return "base"

print(Calc.f(None))                             # base       (a child may call it with super().f())

# ABC vs Protocol vs duck typing (Module 13)
#   ABC        you inherit (or register); errors appear when the object is created; gives mixin methods
#   Protocol   structural, checked by type checkers (and by isinstance with @runtime_checkable)
#   duck type  no declaration at all; errors appear when the call runs
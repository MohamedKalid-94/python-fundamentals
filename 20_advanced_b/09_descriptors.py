import gc
import weakref

# A DESCRIPTOR is an object, stored as a CLASS attribute, that has __get__, __set__ or __delete__.
# It controls what happens when you read, write or delete that attribute on an object.
# Functions, property, classmethod and staticmethod are all descriptors.

# 1. Data descriptor (has __set__) beats the instance dictionary. Non-data (only __get__) loses.
class Loud:
    def __get__(self, obj, owner=None):
        return "descriptor"

    def __set__(self, obj, value):
        pass

class Quiet:
    def __get__(self, obj, owner=None):
        return "non-data descriptor"

class T:
    loud = Loud()
    quiet = Quiet()

t = T()
t.__dict__["loud"] = "instance"
t.__dict__["quiet"] = "instance"
print(t.loud, t.quiet)                          # descriptor instance

def plain():
    pass

print(hasattr(plain, "__get__"), hasattr(plain, "__set__"))     # True False    functions are non-data
print(hasattr(property, "__set__"), hasattr(classmethod, "__set__"))   # True False

# 2. A validated field that can be reused in any class
class Positive:
    def __set_name__(self, owner, name):        # called when the class is created
        self.public, self.private = name, "_" + name

    def __get__(self, obj, owner=None):
        if obj is None:                         # accessed on the class: Product.price
            return self
        return getattr(obj, self.private)

    def __set__(self, obj, value):
        if value <= 0:
            raise ValueError(f"{self.public} must be positive, got {value}")
        setattr(obj, self.private, value)

class Typed:
    def __init__(self, type_):
        self.type = type_

    def __set_name__(self, owner, name):
        self.public, self.private = name, "_" + name

    def __get__(self, obj, owner=None):
        return self if obj is None else getattr(obj, self.private)

    def __set__(self, obj, value):
        if not isinstance(value, self.type):
            raise TypeError(f"{self.public} must be {self.type.__name__}, got {type(value).__name__}")
        setattr(obj, self.private, value)

class Product:
    price = Positive()
    qty = Typed(int)

    def __init__(self, price, qty):
        self.price = price                      # goes through Positive.__set__
        self.qty = qty

p = Product(9.5, 2)
print(p.price, p.qty, sorted(vars(p)))          # 9.5 2 ['_price', '_qty']
for args in ((-1, 2), (5, "x")):
    try:
        Product(*args)
    except (ValueError, TypeError) as e:
        print(e)
# price must be positive, got -1
# qty must be int, got str

# 3. A lazy attribute: computed once, then stored (a NON-data descriptor, like cached_property)
calls = []

class LazyProperty:
    def __init__(self, func):
        self.func = func

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        value = self.func(obj)
        obj.__dict__[self.name] = value         # the instance dictionary now wins over the descriptor
        return value

class Report:
    @LazyProperty
    def total(self):
        calls.append("computing")
        return 42

r = Report()
print(r.total, r.total, calls)                  # 42 42 ['computing']

# 4. Data that belongs to each object, kept in the descriptor
class PerInstance:
    def __init__(self, default=0):
        self.default = default
        self.data = weakref.WeakKeyDictionary()     # does not keep the objects alive

    def __get__(self, obj, owner=None):
        return self if obj is None else self.data.get(obj, self.default)

    def __set__(self, obj, value):
        self.data[obj] = value

class Counter:
    hits = PerInstance()

a, b = Counter(), Counter()
a.hits = 5
print(a.hits, b.hits, len(Counter.hits.data))   # 5 0 1
del a
gc.collect()
print(len(Counter.hits.data))                   # 0

# 5. __get__ also receives the OWNER class, and __delete__ handles "del obj.x"
class ClassName:
    def __get__(self, obj, owner=None):
        return owner.__name__

class Holder:
    who = ClassName()

print(Holder.who, Holder().who)                 # Holder Holder

log = []

class Tracked:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, owner=None):
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value
        log.append(f"set {self.name}")

    def __delete__(self, obj):
        obj.__dict__.pop(self.name, None)
        log.append(f"deleted {self.name}")

class Box:
    x = Tracked()

box = Box()
box.x = 1
del box.x
print(log, box.x)                               # ['set x', 'deleted x'] None

# 6. Your own property (this is almost exactly how the built-in works)
class MyProperty:
    def __init__(self, fget=None, fset=None):
        self.fget, self.fset = fget, fset

    def __get__(self, obj, owner=None):
        return self if obj is None else self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("read-only")
        self.fset(obj, value)

    def setter(self, fset):
        return type(self)(self.fget, fset)

class Circle:
    def __init__(self, r):
        self._r = r

    @MyProperty
    def radius(self):
        return self._r

    @radius.setter
    def radius(self, value):
        self._r = value

    @MyProperty
    def area(self):
        return round(3.14159 * self._r ** 2, 2)

c = Circle(2)
c.radius = 5
print(c.radius, c.area)                         # 5 78.54
try:
    c.area = 1
except AttributeError as e:
    print(e)                                    # read-only

# 7. An EMBEDDED example: bit fields of a hardware register
class BitField:
    def __init__(self, shift, width=1):
        self.shift, self.width = shift, width
        self.mask = (1 << width) - 1

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, owner=None):
        return self if obj is None else (obj.value >> self.shift) & self.mask

    def __set__(self, obj, new):
        if not 0 <= new <= self.mask:
            raise ValueError(f"{self.name} must be 0..{self.mask}")
        obj.value = (obj.value & ~(self.mask << self.shift)) | (new << self.shift)

class ControlReg:
    enable = BitField(0)                        # bit 0
    mode = BitField(1, 2)                       # bits 2..1
    speed = BitField(4, 4)                      # bits 7..4

    def __init__(self, value=0):
        self.value = value

reg = ControlReg()
reg.enable = 1
reg.mode = 2
reg.speed = 9
print(f"{reg.value:08b}", reg.enable, reg.mode, reg.speed)      # 10010101 1 2 9
try:
    reg.speed = 16
except ValueError as e:
    print(e)                                    # speed must be 0..15

# THE LOOKUP RULE for  obj.name
#   1. a DATA descriptor found on the class (or its parents)      -> its __get__
#   2. the instance __dict__
#   3. a NON-data descriptor or plain attribute on the class      -> its __get__ (bound methods!) or the value
#   4. __getattr__ if the class defines it
# WHERE DESCRIPTORS LIVE: property, methods, classmethod, staticmethod, __slots__ members, functools.cached_property,
#   Django model fields, SQLAlchemy columns, dataclass fields with defaults.
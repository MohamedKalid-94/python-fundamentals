import re
import sys
import types

# What is an object, really? Let us look inside.

# 1. Identity, type and class
a = [1]
b = a
print(id(a) == id(b), a is b, type(a), a.__class__ is list)     # True True <class 'list'> True
print(isinstance(id(a), int))                   # True       id() is a number that is unique while the object lives

# 2. Instance attributes live in a dictionary: __dict__
class P:
    def __init__(self):
        self.x = 1
        self.y = 2

p = P()
print(p.__dict__, vars(p) is p.__dict__)        # {'x': 1, 'y': 2} True
p.__dict__["z"] = 3                             # writing the dictionary creates an attribute
print(p.z)                                      # 3

class Q:
    kind = "q"

    def hello(self):
        return "hello"

print(sorted(k for k in Q.__dict__ if not k.startswith("__")))  # ['hello', 'kind']   methods live in the CLASS

# 3. The lookup order for  obj.name
#    1. a DATA descriptor on the class (a property)    2. the instance __dict__
#    3. the class and its parents (the MRO)             4. __getattr__, if the class has one
class A:
    x = "class"

obj = A()
print(obj.x)                                    # class
obj.x = "instance"
print(obj.x, A.x)                               # instance class
del obj.x
print(obj.x)                                    # class

class B:
    @property
    def v(self):
        return "property"

bb = B()
bb.__dict__["v"] = "dict"
print(bb.v)                                     # property     a property beats the instance dictionary

# 4. __getattribute__ runs for EVERY lookup; __getattr__ only when the normal lookup FAILS
log = []

class Spy:
    x = 1

    def __getattribute__(self, name):
        log.append(name)
        return super().__getattribute__(name)   # never use self.name here: infinite recursion

spy = Spy()
spy.x
spy.x
print(log)                                      # ['x', 'x']

class Defaults:
    def __getattr__(self, name):
        return f"<{name}>"

print(Defaults().foo, hasattr(Defaults(), "anything"))          # <foo> True

class Frozen:
    def __init__(self):
        object.__setattr__(self, "x", 1)        # go around our own __setattr__

    def __setattr__(self, name, value):
        raise AttributeError("frozen")

f = Frozen()
try:
    f.x = 2
except AttributeError as e:
    print(e, f.x)                               # frozen 1

# 5. Methods are plain functions stored in the class; "binding" happens at lookup time
class C:
    def m(self):
        return "m"

c = C()
print(type(C.m).__name__, type(c.m).__name__)   # function method
print(c.m.__self__ is c, c.m.__func__ is C.m)   # True True
print(C.m(c), types.MethodType(C.m, c)(), C.__dict__["m"].__get__(c, C)())       # m m m
# functions are DESCRIPTORS: their __get__ builds the bound method (more in Module 20)

# 6. A function is an object with a code object inside
def func(a, b=2, *args, c=3, **kwargs):
    return a

print(func.__name__, func.__defaults__, func.__kwdefaults__)    # func (2,) {'c': 3}
print(func.__code__.co_argcount, func.__code__.co_kwonlyargcount)               # 2 1
print(bool(func.__code__.co_flags & 0x04), bool(func.__code__.co_flags & 0x08)) # True True   has *args, **kwargs
print(func.__globals__ is globals(), func.__closure__)          # True None

def second(a, b=2):
    return b

second.__defaults__ = (9,)                      # defaults can be changed at run time
print(second(1))                                # 9

def answer():
    return 42

print(42 in answer.__code__.co_consts)          # True

def typed(a: int) -> str:
    return str(a)

print(typed.__annotations__)                    # {'a': <class 'int'>, 'return': <class 'str'>}

def where():
    return sys._getframe(1).f_code.co_name      # look at the CALLER's stack frame

def caller():
    return where()

print(caller())                                 # caller

# 7. Types are objects too
print(type(int) is type, type(type) is type, isinstance(int, object))           # True True True
print([c.__name__ for c in bool.__mro__])       # ['bool', 'int', 'object']
Dyn = type("Dyn", (), {"x": 1})                 # a class made with a function call
print(Dyn.x, Dyn().x)                           # 1 1

# 8. __eq__ and __hash__ go together
class Pt:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

print({Pt(1, 2): "a"}[Pt(1, 2)])                # a

class NoHash:
    def __eq__(self, other):
        return True

try:
    hash(NoHash())
except TypeError:
    print("TypeError")                          # TypeError     __eq__ without __hash__ removes hashing

# 9. Truth value: __bool__, otherwise __len__
class Empty:
    def __len__(self):
        return 0

class AlwaysFalse:
    def __bool__(self):
        return False

print(bool(Empty()), bool(AlwaysFalse()), bool(object()))       # False False True

# 10. Memory layout: __dict__ versus __slots__
class WithDict:
    def __init__(self):
        self.a, self.b, self.c = 1, 2, 3

class WithSlots:
    __slots__ = ("a", "b", "c")

    def __init__(self):
        self.a, self.b, self.c = 1, 2, 3

print(hasattr(WithSlots(), "__dict__"))         # False
print(sys.getsizeof(WithSlots()) < sys.getsizeof(WithDict()) + sys.getsizeof(WithDict().__dict__))   # True

# 11. The default repr shows the class and the address
print(bool(re.fullmatch(r"<__main__\.P object at 0x[0-9a-f]+>", repr(p))))      # True

# 12. A class can be changed: the object's __class__ can even be replaced
class One:
    def who(self):
        return "one"

class Two:
    def who(self):
        return "two"

o = One()
o.__class__ = Two
print(type(o).__name__, o.who())                # Two two

# 13. Callable or not
print(callable(P), callable(p), callable(len))  # True False True

# 14. __set_name__: a class attribute is told its own name when the class is created
class Field:
    def __set_name__(self, owner, name):
        self.name = name

class Model:
    first = Field()
    second = Field()

print(Model.first.name, Model.second.name)      # first second

# THE LIFE OF obj.method(arg)
#   1. find "method" in the type of obj (through the MRO)   2. call its __get__ to bind obj
#   3. call the bound method with arg                        so  obj.method(arg) == type(obj).method(obj, arg)
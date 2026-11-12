# EVERYTHING is an object, so a CLASS is an object too. Its type is its METACLASS.
#   an instance        is made by its class
#   a class            is made by its metaclass     (the default metaclass is "type")

class Foo:
    pass

print(type(Foo) is type, type(type) is type, type(Foo()) is Foo)    # True True True

# 1. "class" is a call to the metaclass: class Foo(Base): ...   ==   type("Foo", (Base,), namespace)
Dyn = type("Dyn", (object,), {"x": 1, "get": lambda self: self.x})
print(Dyn().get(), Dyn.__name__)                # 1 Dyn

# 2. A metaclass is a subclass of type. See when each method runs.
log = []

class Meta(type):
    def __new__(mcls, name, bases, namespace):  # creates the CLASS object
        log.append(f"new {name}")
        return super().__new__(mcls, name, bases, namespace)

    def __init__(cls, name, bases, namespace):  # initialises the CLASS object
        log.append(f"init {name}")
        super().__init__(name, bases, namespace)

    def __call__(cls, *args, **kwargs):         # runs when you CALL the class: A()
        log.append(f"call {cls.__name__}")
        return super().__call__(*args, **kwargs)

class A(metaclass=Meta):
    def __init__(self):
        log.append("A.__init__")

a = A()
print(log)                                      # ['new A', 'init A', 'call A', 'A.__init__']
print(type(A).__name__, type(a).__name__)       # Meta A

# 3. __prepare__ chooses the namespace in which the class body runs
class NoDupes(dict):
    def __setitem__(self, key, value):
        if key in self and not key.startswith("__"):
            raise TypeError(f"duplicate definition of {key!r}")
        super().__setitem__(key, value)

class NoDupeMeta(type):
    @classmethod
    def __prepare__(mcls, name, bases):
        return NoDupes()

try:
    class Bad(metaclass=NoDupeMeta):
        def run(self):
            pass

        def run(self):                          # the same name twice (normally the first is lost silently)
            pass
except TypeError as e:
    print(e)                                    # duplicate definition of 'run'

# 4. Check a class WHEN IT IS DEFINED, not when it is used
class InterfaceMeta(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if bases and not callable(getattr(cls, "run", None)):
            raise TypeError(f"{name} must define run()")

class Base(metaclass=InterfaceMeta):
    pass

class Good(Base):
    def run(self):
        return "ok"

try:
    class Broken(Base):
        pass
except TypeError as e:
    print(e)                                    # Broken must define run()
print(Good().run())                             # ok

# 5. A registry: every subclass is recorded automatically
class PluginMeta(type):
    registry = {}

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if bases:                               # skip the base class itself
            PluginMeta.registry[name.lower()] = cls

class Plugin(metaclass=PluginMeta):
    pass

class CsvPlugin(Plugin):
    def run(self):
        return "csv"

class JsonPlugin(Plugin):
    def run(self):
        return "json"

print(sorted(PluginMeta.registry), PluginMeta.registry["csvplugin"]().run())    # ['csvplugin', 'jsonplugin'] csv

# 6. Change the namespace before the class exists
class UpperAttrs(type):
    def __new__(mcls, name, bases, namespace):
        upper = {k if k.startswith("__") else k.upper(): v for k, v in namespace.items()}
        return super().__new__(mcls, name, bases, upper)

class Cfg(metaclass=UpperAttrs):
    host = "x"
    port = 80

print(Cfg.HOST, Cfg.PORT, hasattr(Cfg, "host"))                 # x 80 False

# 7. Methods of the METACLASS belong to the class, not to its instances
class DescribeMeta(type):
    def describe(cls):
        return f"class {cls.__name__}"

class C(metaclass=DescribeMeta):
    pass

print(C.describe())                             # class C
try:
    C().describe()
except AttributeError:
    print("AttributeError")                     # AttributeError

class CountingMeta(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        cls.instances = 0

    def __call__(cls, *args, **kwargs):
        cls.instances += 1
        return super().__call__(*args, **kwargs)

class X(metaclass=CountingMeta):
    pass

X()
X()
print(X.instances)                              # 2

# 8. Change what isinstance() means
class EvenMeta(type):
    def __instancecheck__(cls, obj):
        return isinstance(obj, int) and obj % 2 == 0

class Even(metaclass=EvenMeta):
    pass

print(isinstance(4, Even), isinstance(3, Even))                 # True False

# 9. Two parents with different metaclasses: a conflict
class M1(type):
    pass

class M2(type):
    pass

class P1(metaclass=M1):
    pass

class P2(metaclass=M2):
    pass

try:
    class Both(P1, P2):
        pass
except TypeError:
    print("TypeError")                          # TypeError   metaclass conflict

class M3(M1, M2):                               # the fix: a metaclass that inherits from both
    pass

class Both(P1, P2, metaclass=M3):
    pass

print(type(Both).__name__)                      # M3

# 10. Easier tools that cover most needs: try these BEFORE a metaclass
class Registry:
    items = []

    def __init_subclass__(cls, **kwargs):       # runs for every subclass (Python 3.6+)
        super().__init_subclass__(**kwargs)
        Registry.items.append(cls.__name__)

class One(Registry):
    pass

class Two(Registry):
    pass

print(Registry.items)                           # ['One', 'Two']

# WHERE METACLASSES LIVE IN PRACTICE
#   ABCMeta (abstract classes)   EnumMeta (Enum)   Django models   SQLAlchemy declarative classes
#   typing.Protocol              older versions of Pydantic
# RULE OF THUMB: use  1. a plain class / function   2. a class decorator   3. __init_subclass__
#   4. a descriptor   and only THEN a metaclass. Metaclasses are powerful, but hard to read and to combine.
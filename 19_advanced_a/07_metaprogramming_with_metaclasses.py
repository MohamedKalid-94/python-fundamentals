import functools
import inspect
import types

# METAPROGRAMMING: code that creates or changes code (classes, functions, attributes) at run time.
# Metaclasses are one tool. Here are the common, useful patterns.

# 1. A declarative "model": fields are declared in the class body, the metaclass collects them
class Field:
    def __init__(self, type_, default=None):
        self.type = type_
        self.default = default

    def __set_name__(self, owner, name):        # told its own name when the class is created
        self.name = name

    def __get__(self, obj, owner=None):
        if obj is None:
            return self                         # User.name gives the Field itself
        return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj, value):
        if not isinstance(value, self.type):
            raise TypeError(f"{self.name} must be {self.type.__name__}, got {type(value).__name__}")
        obj.__dict__[self.name] = value


class ModelMeta(type):
    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        fields = {}
        for base in bases:
            fields.update(getattr(base, "_fields", {}))             # inherit the fields of the parents
        fields.update({k: v for k, v in namespace.items() if isinstance(v, Field)})
        cls._fields = fields
        return cls


class Model(metaclass=ModelMeta):
    def __init__(self, **values):
        unknown = set(values) - set(self._fields)
        if unknown:
            raise TypeError(f"unknown fields: {sorted(unknown)}")
        for name, field in self._fields.items():
            if name in values:
                setattr(self, name, values[name])
            elif field.default is not None:
                setattr(self, name, field.default)

    def to_dict(self):
        return {name: getattr(self, name) for name in self._fields}

    def __repr__(self):
        inner = ", ".join(f"{n}={getattr(self, n)!r}" for n in self._fields)
        return f"{type(self).__name__}({inner})"


class User(Model):
    name = Field(str)
    age = Field(int, default=18)


class Admin(User):
    level = Field(int, default=1)


u = User(name="Ann")
print(u, u.to_dict())                           # User(name='Ann', age=18) {'name': 'Ann', 'age': 18}
print(Admin(name="Bo", level=3))                # Admin(name='Bo', age=18, level=3)
print(list(User._fields), list(Admin._fields))  # ['name', 'age'] ['name', 'age', 'level']
print(User.name is User._fields["name"])        # True
u.age = 30
print(u.age)                                    # 30
for bad in ({"name": "Ann", "age": "x"}, {"nick": "x"}):
    try:
        User(**bad)
    except TypeError as e:
        print(e)
# age must be int, got str
# unknown fields: ['nick']

# 2. A metaclass that wraps EVERY method (for example to trace calls)
calls = []

def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        calls.append(func.__name__)
        return func(*args, **kwargs)
    return wrapper

class TraceMeta(type):
    def __new__(mcls, name, bases, namespace):
        for key, value in namespace.items():
            if inspect.isfunction(value) and not key.startswith("__"):
                namespace[key] = trace(value)
        return super().__new__(mcls, name, bases, namespace)

class Robot(metaclass=TraceMeta):
    def move(self):
        return "moving"

    def turn(self):
        return "turning"

r = Robot()
r.move()
r.turn()
r.move()
print(calls)                                    # ['move', 'turn', 'move']

# 3. A plugin registry with __init_subclass__ (no metaclass needed), with a class keyword
class Plugin:
    registry = {}

    def __init_subclass__(cls, key=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if key:
            Plugin.registry[key] = cls

class Csv(Plugin, key="csv"):
    def run(self):
        return "csv!"

class Json(Plugin, key="json"):
    def run(self):
        return "json!"

print(sorted(Plugin.registry), Plugin.registry["json"]().run())    # ['csv', 'json'] json!

# 4. A class decorator that writes methods from the annotations
def auto_methods(cls):
    names = list(cls.__annotations__)

    def __repr__(self):
        inner = ", ".join(f"{n}={getattr(self, n)!r}" for n in names)
        return f"{type(self).__name__}({inner})"

    def __eq__(self, other):
        return type(self) is type(other) and all(getattr(self, n) == getattr(other, n) for n in names)

    cls.__repr__, cls.__eq__ = __repr__, __eq__
    return cls

@auto_methods
class P2:
    x: int
    y: int

    def __init__(self, x, y):
        self.x, self.y = x, y

print(P2(1, 2), P2(1, 2) == P2(1, 2), P2(1, 2) == P2(1, 3))     # P2(x=1, y=2) True False
# (this is the idea behind dataclasses, which also build source code with exec)

# 5. Build classes from DATA
Base = type("Base", (), {"kind": "base"})
Dyn2 = types.new_class("Dyn2", (Base,), {}, lambda ns: ns.update(x=1))
print(Dyn2.x, Dyn2.kind, Dyn2.__mro__[1].__name__)              # 1 base Base

def make_init(field_names):                     # generate SOURCE CODE and compile it
    if not all(n.isidentifier() for n in field_names):          # never exec names you did not check
        raise ValueError("bad field name")
    args = ", ".join(field_names)
    body = "\n".join(f"    self.{n} = {n}" for n in field_names)
    source = f"def __init__(self, {args}):\n{body}\n"
    namespace = {}
    exec(source, namespace)
    return source, namespace["__init__"]

source, init = make_init(["x", "y"])
print(source, end="")
# def __init__(self, x, y):
#     self.x = x
#     self.y = y
Point = type("Point", (), {"__init__": init})
pt = Point(3, 4)
print(pt.x, pt.y)                               # 3 4

# 6. Create properties in a loop
class Sensor:
    def __init__(self):
        self._temp, self._hum = 25.3, 40

for attribute in ("temp", "hum"):
    setattr(Sensor, attribute, property(lambda self, n=attribute: getattr(self, "_" + n)))

sensor = Sensor()
print(sensor.temp, sensor.hum)                  # 25.3 40

# 7. A proxy that records every method call (dynamic delegation with __getattr__)
class LoggingProxy:
    def __init__(self, target):
        self._target = target
        self.calls = []

    def __getattr__(self, name):                # only called when the normal lookup fails
        attr = getattr(self._target, name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                self.calls.append(name)
                return attr(*args, **kwargs)
            return wrapper
        return attr

proxy = LoggingProxy([])
proxy.append(1)
proxy.append(2)
print(proxy.calls, proxy._target)               # ['append', 'append'] [1, 2]

# 8. Use the function SIGNATURE to build a decorator that checks argument types
def enforce_types(func):
    sig = inspect.signature(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            annotation = func.__annotations__.get(name)
            if isinstance(annotation, type) and not isinstance(value, annotation):
                raise TypeError(f"{name} must be {annotation.__name__}")
        return func(*args, **kwargs)
    return wrapper

@enforce_types
def repeat(text: str, times: int):
    return text * times

print(repeat("ab", 2))                          # abab
try:
    repeat("ab", "2")
except TypeError as e:
    print(e)                                    # times must be int

# 9. compile / eval / exec: run code that is TEXT
code = compile("x * 2", "<expr>", "eval")
print(eval(code, {"x": 21}))                    # 42
# eval and exec run ANY code. Never pass them text from a user, a file you do not control,
# or the network. Passing a restricted globals dictionary is NOT a safe sandbox.
# For plain data use ast.literal_eval or json.loads.

# WHICH TOOL?
#   function decorator        wrap or register a function
#   class decorator           change a finished class (add methods, register it)
#   __init_subclass__         react when a subclass is created (registries, checks)
#   descriptor (__set_name__) a field with its own get/set logic (validation, lazy values)
#   metaclass                 change HOW the class is built (namespace, class-wide rules)
#   type() / types.new_class  build a class from data
#   exec / compile            generate source code (the last resort; validate every name)
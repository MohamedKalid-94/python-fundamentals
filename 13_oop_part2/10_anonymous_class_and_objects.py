import json
from types import SimpleNamespace

# Python has no "anonymous class" syntax like Java, but you can get the same result.

# 1. A class created on the fly with type(name, bases, attributes)
Anon = type("Anon", (), {"value": 42, "show": lambda self: f"value={self.value}"})
a = Anon()
print(a.show())                             # value=42
print(Anon.__name__, type(a))               # Anon <class '__main__.Anon'>

# Created and used in ONE expression
print(type("T", (), {"f": lambda self: 1})().f())       # 1

# 2. SimpleNamespace: an anonymous object with attributes
ns = SimpleNamespace(a=1, b=2)
print(ns)                                   # namespace(a=1, b=2)
ns.c = 3
print(ns.a, ns.c)                           # 1 3
print(vars(ns))                             # {'a': 1, 'b': 2, 'c': 3}
print(SimpleNamespace(a=1) == SimpleNamespace(a=1))     # True

# 3. object(): a plain, unique object (often used as a sentinel)
marker = object()
print(type(marker))                         # <class 'object'>

# 4. JSON straight into objects with attribute access
cfg = json.loads('{"host": "x", "port": 8080}', object_hook=lambda d: SimpleNamespace(**d))
print(cfg.host, cfg.port)                   # x 8080

# 5. Callable objects: anonymous behaviour with state
class Adder:
    def __init__(self, n):
        self.n = n

    def __call__(self, x):
        return x + self.n

print(Adder(5)(3))                          # 8        the object is created and used at once
print(list(map(Adder(10), [1, 2])))         # [11, 12]

# 6. An ANONYMOUS OBJECT is one with no name: it lives only as long as it is used
class Temp:
    def __del__(self):
        print("gone")

Temp()                                      # gone     (destroyed right after the statement)

# lambda is the anonymous FUNCTION: print((lambda x: x * 2)(4))  ->  8
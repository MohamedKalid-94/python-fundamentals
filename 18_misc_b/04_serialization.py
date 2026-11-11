import pickle
import shelve
import struct
import tempfile
import threading
import tomllib
from pathlib import Path

# SERIALIZATION turns objects into bytes or text (to save or send) and back again.

# 1. pickle: Python objects, with their exact types
data = {"name": "Ann", "scores": (90, 85), "tags": {"a", "b"}, "none": None}
restored = pickle.loads(pickle.dumps(data))
print(restored == data)                         # True
print(type(restored["scores"]).__name__, type(restored["tags"]).__name__)   # tuple set

# 2. Your own classes (the class must be importable when you load the data)
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

p = Point(1, 2)
p2 = pickle.loads(pickle.dumps(p))
print(p2.x, p2.y, p2 is p)                      # 1 2 False

# 3. Some things cannot be pickled
for thing in (lambda x: x, threading.Lock()):
    try:
        pickle.dumps(thing)
    except (pickle.PicklingError, TypeError):
        print("cannot pickle")
# cannot pickle
# cannot pickle

# 4. __getstate__ / __setstate__: leave out what cannot be pickled, rebuild it on load
class Service:
    def __init__(self, name):
        self.name = name
        self.lock = threading.Lock()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["lock"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.Lock()

clone = pickle.loads(pickle.dumps(Service("x")))
print(clone.name, hasattr(clone.lock, "acquire"))       # x True

# 5. SECURITY: unpickling RUNS CODE chosen by whoever made the data.
#    This harmless demonstration only prints, but it could do anything:
class Evil:
    def __reduce__(self):
        return (print, ("code ran during unpickling",))

result = pickle.loads(pickle.dumps(Evil()))
# code ran during unpickling
print(result)                                   # None
# NEVER unpickle data from the network, a file you did not create, or a user.

print(pickle.HIGHEST_PROTOCOL >= 5)             # True

# 6. shelve: a dictionary that lives in a file (values are pickled)
with tempfile.TemporaryDirectory() as tmp:
    path = str(Path(tmp) / "store")
    with shelve.open(path) as db:
        db["a"] = [1, 2]
        db["b"] = {"x": 1}
    with shelve.open(path) as db:
        print(sorted(db.keys()), db["a"])       # ['a', 'b'] [1, 2]

# 7. TOML: a readable format for configuration files (reading is built in since Python 3.11)
text = 'title = "x"\n[server]\nport = 8080\ntags = ["a", "b"]'
print(tomllib.loads(text))                      # {'title': 'x', 'server': {'port': 8080, 'tags': ['a', 'b']}}

# 8. struct: fixed binary layouts (see Module 16)
print(struct.unpack("<HB", struct.pack("<HB", 500, 7)))     # (500, 7)

# WHICH FORMAT?
#   JSON      text, any language, no code execution            web APIs, config, logs   (next file)
#   pickle    binary, Python only, NOT safe for untrusted data  caches between your own Python runs
#   TOML/YAML text, written by people                           configuration files
#   CSV       text tables                                       spreadsheets, simple data
#   struct    binary, fixed layout                              protocols, microcontroller data
#   msgpack / protobuf  compact binary, many languages (third-party)
#   sqlite    many records you want to query
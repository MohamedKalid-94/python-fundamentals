import json
import re
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path

# JSON = text that every language understands.
#   Python        JSON
#   dict          object  { }          list, tuple    array  [ ]
#   str           string               int, float     number
#   True / False  true / false         None           null

# 1. Python to JSON text
print(json.dumps({"a": 1, "b": [1, 2, None], "c": True}))   # {"a": 1, "b": [1, 2, null], "c": true}
print(json.dumps({"name": "Ann", "scores": [90, 85]}, indent=2))
# {
#   "name": "Ann",
#   "scores": [
#     90,
#     85
#   ]
# }
print(json.dumps({"b": 1, "a": 2}, sort_keys=True))         # {"a": 2, "b": 1}
print(json.dumps({"a": 1, "b": [1, 2]}, separators=(",", ":")))     # {"a":1,"b":[1,2]}
print(json.dumps("café"), json.dumps("café", ensure_ascii=False))   # "caf\u00e9" "café"

# 2. JSON text to Python
print(json.loads('{"x": [1, 2.5, "s", null, true]}'))       # {'x': [1, 2.5, 's', None, True]}
print(json.loads(b'{"a": 1}'), json.loads("12345678901234567890"))  # {'a': 1} 12345678901234567890

# 3. What does NOT survive the trip
print(json.loads(json.dumps((1, 2))), json.loads(json.dumps({1: "a"})))     # [1, 2] {'1': 'a'}
#    tuples become lists, and dictionary keys always become strings

print(json.dumps(float("nan")))                 # NaN       (not valid JSON, other tools may refuse it)
try:
    json.dumps(float("nan"), allow_nan=False)
except ValueError:
    print("ValueError")                         # ValueError

# 4. Types JSON does not know: tell it how to convert them with default=
try:
    json.dumps({"tags": {"a"}})
except TypeError as e:
    print(e)                                    # Object of type set is not JSON serializable

def encode(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, set):
        return sorted(obj)
    raise TypeError(f"cannot serialise {type(obj).__name__}")

print(json.dumps({"when": datetime(2026, 11, 10, 14, 30), "tags": {"b", "a"}}, default=encode))
# {"when": "2026-11-10T14:30:00", "tags": ["a", "b"]}

class Encoder(json.JSONEncoder):                # the same idea as a class
    def default(self, o):
        if isinstance(o, set):
            return sorted(o)
        return super().default(o)

print(json.dumps({"s": {3, 1, 2}}, cls=Encoder))            # {"s": [1, 2, 3]}

# 5. Decoding with hooks
print(json.loads('{"p": 9.99}', parse_float=Decimal))       # {'p': Decimal('9.99')}

@dataclass
class Person:
    name: str
    age: int

print(json.dumps(asdict(Person("Ann", 30))))                # {"name": "Ann", "age": 30}
print(Person(**json.loads('{"name": "Bob", "age": 25}')))   # Person(name='Bob', age=25)

# 6. Invalid JSON
try:
    json.loads("{'a': 1}")                      # single quotes are not JSON
except json.JSONDecodeError as e:
    print(type(e).__name__, isinstance(e, ValueError), e.pos)       # JSONDecodeError True 1
try:
    json.loads("[1,2,]")                        # a trailing comma is not JSON
except json.JSONDecodeError:
    print("JSONDecodeError")                    # JSONDecodeError

# 7. Files
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "data.json"
    settings = {"baud": 9600, "ports": ["COM1", "COM2"]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
    with open(path, encoding="utf-8") as f:
        print(json.load(f) == settings)         # True

# 8. JSON Lines: one JSON value per line (good for logs and big data sets)
lines = [json.dumps({"n": i}) for i in range(3)]
print(len(lines), [json.loads(line)["n"] for line in lines])    # 3 [0, 1, 2]

# 9. Clean up the answer of a language model before parsing (it often adds code fences)
reply = '```json\n{"ok": true}\n```'
cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", reply.strip())
print(json.loads(cleaned))                      # {'ok': True}
# Always wrap json.loads() on outside data in try/except json.JSONDecodeError.
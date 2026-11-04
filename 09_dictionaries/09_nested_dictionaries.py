import json

students = {
    "s1": {"name": "Ann", "marks": {"math": 90, "sci": 85}},
    "s2": {"name": "Bob", "marks": {"math": 70, "sci": 80}},
}

# Access: chain the keys
print(students["s1"]["marks"]["math"])      # 90

# A missing key at any level raises KeyError
try:
    print(students["s9"]["name"])
except KeyError as e:
    print(e)                                # 's9'

# Safe access with get() and an empty-dict default
print(students.get("s9", {}).get("name", "unknown"))    # unknown

# Change, add
students["s1"]["marks"]["math"] += 5
students["s2"]["marks"]["art"] = 95
students["s3"] = {"name": "Cy", "marks": {}}
print(students["s1"]["marks"])              # {'math': 95, 'sci': 85}

# Loop through the levels
for sid, info in students.items():
    print(sid, info["name"], sum(info["marks"].values()))
# s1 Ann 180
# s2 Bob 245
# s3 Cy 0

# Build a dictionary of lists
groups = {}
for word in ["apple", "avocado", "banana", "blueberry", "cherry"]:
    groups.setdefault(word[0], []).append(word)
print(groups)
# {'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry'], 'c': ['cherry']}

# Nested comprehension
print({w: {"len": len(w), "first": w[0]} for w in ["apple", "fig"]})
# {'apple': {'len': 5, 'first': 'a'}, 'fig': {'len': 3, 'first': 'f'}}

# A safe deep lookup helper
def deep_get(data, path, default=None):
    for key in path:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return default
    return data

print(deep_get(students, ["s1", "marks", "sci"]))           # 85
print(deep_get(students, ["s1", "x", "y"], "none"))         # none

# JSON is nested dictionaries and lists as text (used by APIs and LLMs)
print(json.dumps(students["s1"]))
# {"name": "Ann", "marks": {"math": 95, "sci": 85}}
print(json.dumps(students["s1"], indent=2))
# {
#   "name": "Ann",
#   "marks": {
#     "math": 95,
#     "sci": 85
#   }
# }

# TRAP: reusing one inner dictionary for several keys shares it
template = {"tags": []}
users = {"a": template, "b": template}
users["a"]["tags"].append("x")
print(users["b"])                           # {'tags': ['x']}

# FIX: build a separate inner dictionary for each key
users = {name: {"tags": []} for name in "ab"}
users["a"]["tags"].append("x")
print(users)                                # {'a': {'tags': ['x']}, 'b': {'tags': []}}

d = {"a": 1, "b": 2}

print(d.get("a"), d.get("z", 0))            # 1 0
print(d.keys(), d.values(), d.items())
# dict_keys(['a', 'b']) dict_values([1, 2]) dict_items([('a', 1), ('b', 2)])

print(d.setdefault("c", 3), d)              # 3 {'a': 1, 'b': 2, 'c': 3}
d.update({"d": 4})
print(d.pop("d"))                           # 4
print(d.popitem())                          # ('c', 3)

e = d.copy()
d.clear()
print(d, e)                                 # {} {'a': 1, 'b': 2}

# fromkeys(keys, value)
print(dict.fromkeys(["a", "b"]))            # {'a': None, 'b': None}

# TRAP: one mutable value is SHARED by every key
shared = dict.fromkeys(["a", "b"], [])
shared["a"].append(1)
print(shared)                               # {'a': [1], 'b': [1]}
# Use a comprehension for separate lists: {k: [] for k in ["a", "b"]}

# Operators (Python 3.9+)
print({"a": 1} | {"a": 2, "b": 3})          # {'a': 2, 'b': 3}
x = {"a": 1}
x |= {"c": 3}
print(x)                                    # {'a': 1, 'c': 3}

# Built-in functions
scores = {"Ann": 90, "Bob": 75, "Cy": 82}
print(len(scores), sorted(scores), min(scores), max(scores))
# 3 ['Ann', 'Bob', 'Cy'] Ann Cy
print(sum(scores.values()), max(scores.values()))       # 247 90
print(dict(sorted(scores.items(), key=lambda kv: kv[1])))
# {'Bob': 75, 'Cy': 82, 'Ann': 90}
print(any(v > 85 for v in scores.values()), all(v > 80 for v in scores.values()))
# True False
print(list(enumerate(scores)))              # [(0, 'Ann'), (1, 'Bob'), (2, 'Cy')]

# All the dictionary methods
print([m for m in dir(dict) if not m.startswith("_")])
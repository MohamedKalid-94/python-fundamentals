x = {}

# Assign to a NEW key to add it (new keys go to the END)
x["a"] = 1
print(x)                                    # {'a': 1}

# update(): add several, from a dict, keywords or pairs
x.update({"b": 2, "c": 3})
print(x)                                    # {'a': 1, 'b': 2, 'c': 3}
x.update(d=4)
print(x)                                    # {'a': 1, 'b': 2, 'c': 3, 'd': 4}
x.update([("e", 5)])
print(x)                                    # {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

# |= (Python 3.9+)
x |= {"f": 6}
print(x)                                    # {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}

# setdefault(): add ONLY if the key is missing
print(x.setdefault("g", 7), x.setdefault("a", 100))     # 7 1
print(len(x))                               # 7

# Assigning to an EXISTING key overwrites it (no new key)
x["a"] = 10
print(len(x), x["a"])                       # 7 10

# From two lists
print(dict(zip(["a", "b"], [1, 2])))        # {'a': 1, 'b': 2}

# Merge two dictionaries (the right side wins for shared keys)
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
print({**d1, **d2})                         # {'a': 1, 'b': 3, 'c': 4}
print(d1 | d2)                              # {'a': 1, 'b': 3, 'c': 4}

# Add only if missing
cfg = {"port": 80}
if "host" not in cfg:
    cfg["host"] = "localhost"
print(cfg)                                  # {'port': 80, 'host': 'localhost'}

# Group values: setdefault creates the list on first use
groups = {}
groups.setdefault("x", []).append(1)
groups.setdefault("x", []).append(2)
groups.setdefault("y", []).append(3)
print(groups)                               # {'x': [1, 2], 'y': [3]}

# defaultdict does the same automatically
from collections import defaultdict
dd = defaultdict(list)
dd["x"].append(1)
dd["x"].append(2)
print(dict(dd))                             # {'x': [1, 2]}
print(dd["new"])                            # []      (reading a missing key CREATES it)
print(dict(dd))                             # {'x': [1, 2], 'new': []}

# Keys must be hashable
try:
    x[["k"]] = 1
except TypeError as e:
    print(e)                                # unhashable type: 'list'
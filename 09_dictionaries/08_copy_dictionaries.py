import copy

# Assignment does NOT copy
a = {"x": 1, "y": 2}
b = a
b["z"] = 3
print(a)                                    # {'x': 1, 'y': 2, 'z': 3}
print(a is b)                               # True

# Shallow copies: a new dictionary object
c = a.copy()
print(c == a, c is a)                       # True False
c["x"] = 99
print(a["x"], c["x"])                       # 1 99

d = dict(a)
e = {**a}
f = copy.copy(a)
print(d == a, e == a, f == a)               # True True True

# TRAP: a shallow copy SHARES the nested objects
nested = {"scores": [1, 2]}
shallow = nested.copy()
shallow["scores"].append(3)
print(nested)                               # {'scores': [1, 2, 3]}

# DEEP copy: copies everything inside as well
original = {"scores": [1, 2]}
deep = copy.deepcopy(original)
deep["scores"].append(3)
print(original, deep)                       # {'scores': [1, 2]} {'scores': [1, 2, 3]}

# Protect the caller's dictionary inside a function
def with_key(d, k, v):
    d = d.copy()
    d[k] = v
    return d

orig = {"a": 1}
new = with_key(orig, "b", 2)
print(orig, new)                            # {'a': 1} {'a': 1, 'b': 2}

# Merge into a NEW dictionary (a common "settings + overrides" pattern)
base = {"debug": False, "port": 80}
override = {"port": 8080}
config = {**base, **override}
print(config)                               # {'debug': False, 'port': 8080}
print(base)                                 # {'debug': False, 'port': 80}

# Replace the contents IN PLACE (every name sees the change)
x = {"a": 1}
alias = x
x.clear()
x.update({"b": 2})
print(alias)                                # {'b': 2}
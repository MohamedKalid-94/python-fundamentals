d = {"a": 1, "b": 2, "c": 3, "d": 4}

# pop(key): remove and RETURN the value
print(d.pop("b"))                           # 2
print(d)                                    # {'a': 1, 'c': 3, 'd': 4}

# pop with a default: no error if the key is missing
print(d.pop("zzz", "not found"))            # not found

try:
    d.pop("zzz")
except KeyError as e:
    print(e)                                # 'zzz'

# popitem(): remove and return the LAST inserted pair (Python 3.7+)
print(d.popitem())                          # ('d', 4)
print(d)                                    # {'a': 1, 'c': 3}

# del: remove by key
del d["a"]
print(d)                                    # {'c': 3}

try:
    del d["nope"]
except KeyError as e:
    print(e)                                # 'nope'

# clear(): remove everything
d.clear()
print(d)                                    # {}

try:
    d.popitem()
except KeyError as e:
    print(e)                                # 'popitem(): dictionary is empty'

# Remove by condition: build a new dictionary
scores = {"a": 50, "b": 80, "c": 30}
print({k: v for k, v in scores.items() if v >= 50})     # {'a': 50, 'b': 80}

# Remove several keys safely
s = {"a": 1, "b": 2, "c": 3}
for key in ("a", "x"):
    s.pop(key, None)
print(s)                                    # {'b': 2, 'c': 3}

# TRAP: removing while looping over the dictionary
s = {"a": 1, "b": 2, "c": 3}
try:
    for k in s:
        if s[k] == 2:
            del s[k]
except RuntimeError as e:
    print(e)                                # dictionary changed size during iteration

# FIX: loop over a copy of the keys
s = {"a": 1, "b": 2, "c": 3}
for k in list(s):
    if s[k] == 2:
        del s[k]
print(s)                                    # {'a': 1, 'c': 3}

# del removes the NAME, not an item
del s
person = {"name": "Ann", "age": 30, "city": "Pune"}

# Change one value
person["age"] = 31
print(person)                               # {'name': 'Ann', 'age': 31, 'city': 'Pune'}

# update(): change several at once
person.update({"city": "Mumbai", "age": 32})
print(person)                               # {'name': 'Ann', 'age': 32, 'city': 'Mumbai'}
person.update(city="Delhi")                 # keyword form (keys must be valid names)
print(person)                               # {'name': 'Ann', 'age': 32, 'city': 'Delhi'}

# Change every value in a loop (changing VALUES while looping is safe)
prices = {"a": 10, "b": 20}
for key in prices:
    prices[key] *= 2
print(prices)                               # {'a': 20, 'b': 40}

# Or build a new dictionary
prices = {"a": 10, "b": 20}
print({k: v + 5 for k, v in prices.items()})            # {'a': 15, 'b': 25}

# Change values by condition
temps = {"x": -5, "y": 20, "z": -1}
for k, v in temps.items():
    if v < 0:
        temps[k] = 0
print(temps)                                # {'x': 0, 'y': 20, 'z': 0}

# Counting pattern
counts = {}
for ch in "hello":
    counts[ch] = counts.get(ch, 0) + 1
print(counts)                               # {'h': 1, 'e': 1, 'l': 2, 'o': 1}

# Changing a value keeps the key's POSITION
d = {"a": 1, "b": 2, "c": 3}
d["a"] = 100
print(d)                                    # {'a': 100, 'b': 2, 'c': 3}

# Swap two values
d["a"], d["c"] = d["c"], d["a"]
print(d)                                    # {'a': 3, 'b': 2, 'c': 100}

# Rename a key: pop + assign moves it to the END
r = {"old": 1, "b": 2}
r["new"] = r.pop("old")
print(r)                                    # {'b': 2, 'new': 1}

# Rename a key and keep its position: rebuild
r = {"old": 1, "b": 2}
print({("new" if k == "old" else k): v for k, v in r.items()})     # {'new': 1, 'b': 2}

# A mutable value changes in place
t = {"tags": ["a"]}
t["tags"].append("b")
print(t)                                    # {'tags': ['a', 'b']}

# | builds a NEW dictionary (Python 3.9+); the right side wins
base = {"a": 1}
new = base | {"a": 9}
print(base, new)                            # {'a': 1} {'a': 9}
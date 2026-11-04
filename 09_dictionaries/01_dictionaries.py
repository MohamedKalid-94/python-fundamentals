# A dictionary maps UNIQUE, HASHABLE keys to values of any type.
# It is MUTABLE and keeps INSERTION ORDER (Python 3.7+).

person = {"name": "Ann", "age": 30, "city": "Pune"}
print(person)                               # {'name': 'Ann', 'age': 30, 'city': 'Pune'}
print(type(person), len(person))            # <class 'dict'> 3

# Other ways to create one
print(dict(name="Ann", age=30))                         # {'name': 'Ann', 'age': 30}
print(dict([("a", 1), ("b", 2)]))                       # {'a': 1, 'b': 2}
print(dict(zip(["x", "y"], [1, 2])))                    # {'x': 1, 'y': 2}
print(dict.fromkeys(["a", "b"], 0))                     # {'a': 0, 'b': 0}
print({}, dict())                                       # {} {}

# A repeated key keeps the LAST value
print({"a": 1, "a": 2})                                 # {'a': 2}

# Keys can be any hashable value; values can be anything
print({1: "one", (1, 2): "pair", "s": [1, 2]})          # {1: 'one', (1, 2): 'pair', 's': [1, 2]}

try:
    {[1]: "x"}
except TypeError as e:
    print(e)                                            # unhashable type: 'list'

# Keys that compare equal are the SAME key
print({1: "a", 1.0: "b", True: "c"})                    # {1: 'c'}

# Order is the insertion order
print(list({"z": 1, "a": 2}))                           # ['z', 'a']

# Equality ignores the order
print({"a": 1, "b": 2} == {"b": 2, "a": 1})             # True

# "in" checks KEYS, not values
print("name" in person, "Ann" in person)                # True False

# Truthiness
print(bool({}), bool({"a": 0}))                         # False True

# Dictionary comprehension
print({n: n * n for n in range(4)})                     # {0: 0, 1: 1, 2: 4, 3: 9}

# Mutable: the same object is changed in place
before = id(person)
person["age"] = 31
print(person["age"], id(person) == before)              # 31 True

# WHEN TO USE A DICTIONARY
# - look something up by a name or an ID (very fast, O(1) on average)
# - records with named fields
# - counting and grouping
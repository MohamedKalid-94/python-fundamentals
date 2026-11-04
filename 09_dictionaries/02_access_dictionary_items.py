person = {"name": "Ann", "age": 30, "city": "Pune"}

# [key]: raises KeyError if the key is missing
print(person["name"])                       # Ann

try:
    print(person["email"])
except KeyError as e:
    print(e)                                # 'email'

# Keys are case-sensitive
try:
    print(person["Name"])
except KeyError as e:
    print(e)                                # 'Name'

# get(key, default): no error, returns the default (None if you give none)
print(person.get("age"))                    # 30
print(person.get("email"))                  # None
print(person.get("email", "n/a"))           # n/a

# Check first with "in"
print("email" in person)                    # False

# setdefault(key, default): return the value, and ADD the key if it was missing
print(person.setdefault("country", "IN"))   # IN
print(person.setdefault("name", "X"))       # Ann      (existing value is kept)
print(person)                               # {'name': 'Ann', 'age': 30, 'city': 'Pune', 'country': 'IN'}

# Access by position (the dictionary has no index, so convert first)
print(list(person))                         # ['name', 'age', 'city', 'country']
print(list(person.values())[1])             # 30
print(next(iter(person)))                   # name       (the first key)
print(len(person))                          # 4

# Built-in functions on dictionaries
scores = {"Ann": 90, "Bob": 85, "Cy": 70}
print(max(scores, key=scores.get))          # Ann        (the KEY with the highest value)
print(min(scores.values()), sum(scores.values()))       # 70 245

# get() cannot tell "missing" from "stored None": use "in" for that
d = {"a": None}
print(d.get("a"), d.get("b"))               # None None
print("a" in d, "b" in d)                   # True False

# Nested access
data = {"user": {"name": "Ann"}}
print(data["user"]["name"])                 # Ann
print(data.get("admin", {}).get("name"))    # None    (safe chain, no KeyError)
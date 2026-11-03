def describe(name, age, city):
    print(f"{name}, {age}, from {city}")

# Pass by NAME: order no longer matters
describe(city="Pune", name="Ann", age=30)     # Ann, 30, from Pune

# Mix: positional first, then keyword
describe("Ann", city="Pune", age=30)          # Ann, 30, from Pune

# A positional argument AFTER a keyword argument is a SyntaxError:
# describe(name="Ann", 30, "Pune")

# The same parameter twice is a TypeError
try:
    describe("Ann", name="Bob", age=1, city="x")
except TypeError as e:
    print(e)        # describe() got multiple values for argument 'name'

# An unknown name is a TypeError
try:
    describe(name="Ann", age=1, city="x", country="IN")
except TypeError as e:
    print(e)        # describe() got an unexpected keyword argument 'country'

# Built-in functions use keywords too
print("a", "b", sep="-", end="!\n")            # a-b!
print(sorted(["b", "a", "c"], reverse=True))   # ['c', 'b', 'a']

# Why use keywords: the call explains itself
# connect("db.local", 5432, True, False)                       <- unclear
# connect("db.local", port=5432, ssl=True, verbose=False)      <- clear
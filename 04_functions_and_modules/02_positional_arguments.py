def describe(name, age, city):
    print(f"{name}, {age}, from {city}")

describe("Ann", 30, "Pune")     # Ann, 30, from Pune

# POSITION decides which parameter gets which value
describe(30, "Ann", "Pune")     # 30, Ann, from Pune   (wrong order, no error!)

def subtract(a, b):
    return a - b

print(subtract(10, 3))          # 7
print(subtract(3, 10))          # -7

# Wrong number of arguments raises TypeError
try:
    describe("Ann", 30)
except TypeError as e:
    print(e)    # describe() missing 1 required positional argument: 'city'

try:
    describe("Ann", 30, "Pune", "extra")
except TypeError as e:
    print(e)    # describe() takes 3 positional arguments but 4 were given
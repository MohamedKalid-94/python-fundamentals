# + joins strings
print("Hello" + " " + "World")           # Hello World

# + needs BOTH sides to be strings
try:
    print("Age: " + 5)
except TypeError as e:
    print(e)                # can only concatenate str (not "int") to str

print("Age: " + str(5))     # Age: 5

# * repeats
print("ab" * 3)             # ababab
print("-" * 10)             # ----------
print(repr("x" * 0))        # ''

# Adjacent literals (only literals, not variables)
print("Hello" " " "World")  # Hello World

# += builds a new string each time
s = "a"
s += "b"
print(s)                    # ab

# join(): the best way to combine many strings
print(", ".join(["a", "b", "c"]))               # a, b, c
print(", ".join(map(str, [1, 2, 3])))           # 1, 2, 3

try:
    print(", ".join([1, 2]))                    # items must already be strings
except TypeError as e:
    print(e)                # sequence item 0: expected str instance, int found

# Building in a loop: collect in a list, then join once
parts = []
for i in range(5):
    parts.append(str(i))
print("".join(parts))       # 01234

# Splitting a long literal over several lines with parentheses
message = ("This is a long "
           "message split over "
           "three lines")
print(message)              # This is a long message split over three lines

# print() can join with sep
print("a", "b", sep="")     # ab

# Ways to combine text and values (details in 05_string_formatting.py)
name, age = "Ann", 30
print("Name: " + name + ", age: " + str(age))   # Name: Ann, age: 30
print(f"Name: {name}, age: {age}")              # Name: Ann, age: 30   (preferred)
# A function is a named, reusable block of code.
# Terms: a PARAMETER is the name in the definition, an ARGUMENT is the value you pass.

def greet():
    print("Hello!")

greet()                         # Hello!

def add(a, b):                  # a, b are parameters
    return a + b

result = add(3, 4)              # 3, 4 are arguments
print(result)                   # 7

# No return statement means the function returns None
def show(x):
    print(x)

r = show(5)                     # 5
print(r)                        # None

# Returning several values really returns ONE tuple
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([4, 9, 1, 7])
print(low, high)                # 1 9
print(min_max([2, 3]))          # (2, 3)

# return ends the function immediately
def first_negative(nums):
    for n in nums:
        if n < 0:
            return n
    return None

print(first_negative([3, -2, -5]))   # -2
print(first_negative([1, 2]))        # None

# Guard clauses keep code flat (instead of nested if-else from Module 03)
def classify(age):
    if age < 0:
        return "invalid"
    if age < 18:
        return "minor"
    return "adult"

print(classify(-1), classify(10), classify(30))   # invalid minor adult

# Docstring: documentation stored in __doc__
def square(n):
    """Return n squared."""
    return n * n

print(square.__doc__)           # Return n squared.

# FUNCTIONS ARE OBJECTS: they can be stored, passed and returned
f = square
print(f(5))                     # 25
print(type(square))             # <class 'function'>
print(square.__name__)          # square

def apply(func, value):
    return func(value)

print(apply(square, 6))         # 36

# "square" is the function object, "square(6)" is a CALL
print(square)                   # <function square at 0x...>   (address varies)

# A function must be defined BEFORE the line that calls it runs
# (the def statement itself runs when Python reaches it)
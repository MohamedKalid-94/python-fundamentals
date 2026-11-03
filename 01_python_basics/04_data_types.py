# =====================================================
# PYTHON DATA TYPES
# A data type tells Python what KIND of value something is
# and what you are allowed to do with it.
# =====================================================


# -----------------------------------------------------
# PART 1: Two tools to inspect any value
# -----------------------------------------------------
# type()       -> tells you the type
# isinstance() -> asks "is this value of this type?" (True/False)

print(type(42))                   # <class 'int'>
print(isinstance(42, int))        # True
print(isinstance(42, str))        # False


# -----------------------------------------------------
# PART 2: Numbers
# -----------------------------------------------------
whole = 42                        # int     -> whole numbers, any size
decimal = 3.14                    # float   -> numbers with a decimal point
complex_num = 2 + 3j              # complex -> real + imaginary (rare, scientific use)

print(type(whole))                # <class 'int'>
print(type(decimal))              # <class 'float'>
print(type(complex_num))          # <class 'complex'>


# -----------------------------------------------------
# PART 3: Text (str)
# -----------------------------------------------------
word = "Python"                   # single or double quotes both work
print(type(word))                 # <class 'str'>
print(len(word))                  # 6
print(word[0])                    # P   (counting starts at 0)


# -----------------------------------------------------
# PART 4: True / False (bool)
# -----------------------------------------------------
is_ready = True
print(type(is_ready))             # <class 'bool'>
print(True + True)                # 2   (bool is a kind of int: True=1, False=0)


# -----------------------------------------------------
# PART 5: "No value" (None)
# -----------------------------------------------------
# None means "nothing here yet". It is NOT 0 and NOT an empty string.
result = None
print(type(result))               # <class 'NoneType'>
print(result is None)             # True   (use 'is' to check for None)


# -----------------------------------------------------
# PART 6: Collections (many values in one variable)
# -----------------------------------------------------
my_list = [1, 2, 3]               # list  -> ordered, changeable
my_tuple = (1, 2, 3)              # tuple -> ordered, NOT changeable
my_set = {1, 2, 3}                # set   -> unordered, no duplicates
my_dict = {"name": "Sam"}         # dict  -> key: value pairs

print(type(my_list))              # <class 'list'>
print(type(my_tuple))             # <class 'tuple'>
print(type(my_set))               # <class 'set'>
print(type(my_dict))              # <class 'dict'>

# Bonus sequence types
print(type(range(3)))             # <class 'range'>    (a sequence of numbers)
print(type(b"ab"))                # <class 'bytes'>    (raw binary data)


# -----------------------------------------------------
# PART 7: Mutable vs Immutable (the most important idea)
# -----------------------------------------------------
# Mutable   = can be changed IN PLACE (same object, new contents)
# Immutable = can NEVER change; "changing" makes a brand-new object

# Mutable example: list
numbers = [1, 2, 3]
before = id(numbers)              # id() = the object's identity
numbers.append(4)
print(numbers)                    # [1, 2, 3, 4]
print(id(numbers) == before)      # True   -> same object, just modified

# Immutable example: str
text = "hi"
before = id(text)
text = text + "!"
print(text)                       # hi!
print(id(text) == before)         # False  -> a NEW object was created

# Immutable types refuse in-place changes
point = (10, 20)
try:
    point[0] = 99
except TypeError as error:
    print("Error:", error)        # Error: 'tuple' object does not support item assignment


# -----------------------------------------------------
# PART 8: bool is a special case of int
# -----------------------------------------------------
print(isinstance(True, int))      # True   -> bool IS an int underneath
print(type(True) == int)          # False  -> but its exact type is bool


# -----------------------------------------------------
# PART 9: See everything together
# -----------------------------------------------------
samples = [42, 3.14, 2 + 3j, "text", True, None,
           [1, 2], (1, 2), {1, 2}, {"a": 1}, b"ab"]

for item in samples:
    print(f"{item!r:<14} -> {type(item).__name__}")
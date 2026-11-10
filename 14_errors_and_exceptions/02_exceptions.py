import traceback

# An EXCEPTION is an error that happens while the program runs.
# If nobody handles it, the program stops and prints a TRACEBACK.

# 1. The common ones, and their messages
def message(func):
    try:
        func()
    except Exception as e:
        return f"{type(e).__name__}: {e}"

tests = [
    lambda: 1 / 0,
    lambda: int("abc"),
    lambda: [1][5],
    lambda: {}["k"],
    lambda: undefined_name,
    lambda: None.upper(),
    lambda: "a" + 1,
    lambda: len(5),
    lambda: iter(5),
    lambda: (1, 2).append(3),
    lambda: int(float("inf")),
    lambda: __import__("nonexistent_mod"),
]
for t in tests:
    print(message(t))
# ZeroDivisionError: division by zero
# ValueError: invalid literal for int() with base 10: 'abc'
# IndexError: list index out of range
# KeyError: 'k'
# NameError: name 'undefined_name' is not defined
# AttributeError: 'NoneType' object has no attribute 'upper'
# TypeError: can only concatenate str (not "int") to str
# TypeError: object of type 'int' has no len()
# TypeError: 'int' object is not iterable
# AttributeError: 'tuple' object has no attribute 'append'
# OverflowError: cannot convert float infinity to integer
# ModuleNotFoundError: No module named 'nonexistent_mod'

# 2. HOW TO READ A TRACEBACK (read it from the BOTTOM up)
#
#   Traceback (most recent call last):
#     File "script.py", line 9, in <module>        <- where the call chain started
#       result = divide(10, 0)
#     File "script.py", line 5, in divide          <- where it failed
#       return a / b
#   ZeroDivisionError: division by zero            <- WHAT went wrong (type and message)

try:
    1 / 0
except ZeroDivisionError:
    print(traceback.format_exc().splitlines()[-1])      # ZeroDivisionError: division by zero

# 3. An exception travels UP the call stack until somebody catches it
def a():
    b()

def b():
    c()

def c():
    return 1 / 0

try:
    a()
except ZeroDivisionError as e:
    print("caught in the caller")                       # caught in the caller
    names, tb = [], e.__traceback__
    while tb:
        names.append(tb.tb_frame.f_code.co_name)
        tb = tb.tb_next
    print(names)                                        # ['<module>', 'a', 'b', 'c']

# 4. Exceptions are objects in a CLASS HIERARCHY
print([c.__name__ for c in ZeroDivisionError.__mro__])
# ['ZeroDivisionError', 'ArithmeticError', 'Exception', 'BaseException', 'object']
print([c.__name__ for c in KeyError.__mro__])
# ['KeyError', 'LookupError', 'Exception', 'BaseException', 'object']
print([c.__name__ for c in FileNotFoundError.__mro__])
# ['FileNotFoundError', 'OSError', 'Exception', 'BaseException', 'object']

# 5. What an exception object holds
e = ValueError("bad", 42)
print(e.args, str(e))                           # ('bad', 42) ('bad', 42)
e = ValueError("bad")
print(e.args, str(e), repr(e))                  # ('bad',) bad ValueError('bad')

# 6. An unhandled exception ends the program with a traceback and exit code 1.
#    That is fine for a bug you want to see, but not for an expected problem
#    (a missing file, bad user input, a lost connection): handle those (next file).
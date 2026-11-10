import sys

# raise ExceptionClass("message")   signals that something went wrong

# 1. Raise an instance, catch it
try:
    raise ValueError("invalid value")
except ValueError as e:
    print("caught:", e)                         # caught: invalid value

# 2. Raise a class without a message
try:
    raise ValueError
except ValueError as e:
    print(repr(e), repr(str(e)))                # ValueError() ''

# 3. Validate arguments and raise the RIGHT type
def set_age(age):
    if not isinstance(age, int):
        raise TypeError("age must be an int")
    if not 0 <= age <= 130:
        raise ValueError(f"age out of range: {age}")
    return age

for v in (30, "x", -5):
    try:
        print("ok", set_age(v))
    except (TypeError, ValueError) as e:
        print(type(e).__name__ + ":", e)
# ok 30
# TypeError: age must be an int
# ValueError: age out of range: -5

# 4. Raise early (guard clauses) to keep the rest of the function simple
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("b must not be zero")
    return a / b

try:
    divide(1, 0)
except ZeroDivisionError as e:
    print(e)                                    # b must not be zero

# 5. A bare "raise" with nothing to re-raise
try:
    raise
except RuntimeError as e:
    print(e)                                    # No active exception to reraise

# 6. Only exceptions can be raised
try:
    raise "just text"
except TypeError as e:
    print(e)                                    # exceptions must derive from BaseException

# 7. Exceptions can carry data
e = OSError(5, "I/O error")
print(e.errno, e.strerror, e)                   # 5 I/O error [Errno 5] I/O error
print(ValueError("a", 1).args)                  # ('a', 1)

# 8. NotImplementedError marks a method that children must write
class Base:
    def run(self):
        raise NotImplementedError("subclasses must implement run()")

try:
    Base().run()
except NotImplementedError as e:
    print(e)                                    # subclasses must implement run()

# 9. An embedded-style example
try:
    raise TimeoutError("sensor did not answer in 100 ms")
except TimeoutError as e:
    print(e)                                    # sensor did not answer in 100 ms

# 10. sys.exit() raises SystemExit
try:
    sys.exit(3)
except SystemExit as e:
    print("exit code", e.code)                  # exit code 3

# 11. Several errors at once (Python 3.11+): ExceptionGroup and except*
try:
    raise ExceptionGroup("batch", [ValueError("a"), TypeError("b")])
except* ValueError as eg:
    print("value errors:", [str(x) for x in eg.exceptions])
except* TypeError as eg:
    print("type errors:", [str(x) for x in eg.exceptions])
# value errors: ['a']
# type errors: ['b']

# WHICH TYPE TO RAISE
#   ValueError           right type, wrong value          int("abc"), age = -5
#   TypeError            wrong type                       "a" + 1
#   KeyError / IndexError  missing key / position
#   FileNotFoundError, PermissionError, TimeoutError   (OSError family) for the outside world
#   RuntimeError         a general failure with no better type
#   NotImplementedError  a method that must be overridden
#   your own class       when callers must tell your errors apart (file 08)
# Write messages that say WHAT was wrong and WHICH value: "age out of range: -5".
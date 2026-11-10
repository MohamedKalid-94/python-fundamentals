import os
from contextlib import suppress

# try:      the code that might fail
# except:   what to do if it does
# else:     runs only if the try block raised NOTHING
# (finally: runs always, see the next file)

# 1. Basic form, with else
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("cannot divide by zero")
        return None
    else:
        print("division ok")
        return result

print(divide(10, 2))
# division ok
# 5.0
print(divide(1, 0))
# cannot divide by zero
# None

# 2. Several except blocks: the FIRST matching one runs
def parse(text):
    try:
        return 10 / int(text)
    except ValueError:
        return "not a number"
    except ZeroDivisionError:
        return "zero"

print(parse("5"), parse("abc"), parse("0"))     # 2.0 not a number zero

# 3. One block for several types
for value in ("12", None):
    try:
        print(int(value))
    except (ValueError, TypeError) as e:
        print(type(e).__name__)
# 12
# TypeError

# 4. A parent class catches all its children
for container, key in ([1], 5), ({}, "a"):
    try:
        container[key]
    except LookupError as e:                    # IndexError and KeyError are both LookupErrors
        print(type(e).__name__)
# IndexError
# KeyError

# 5. ORDER MATTERS: put the specific types BEFORE the general one
try:
    int("x")
except Exception:                               # catches everything first
    print("generic")                            # generic
except ValueError:
    print("never reached")

# 6. "as e" gives you the exception object
try:
    int("x")
except ValueError as e:
    print(f"{type(e).__name__}: {e}")           # ValueError: invalid literal for int() with base 10: 'x'

# 7. Do NOT use a bare "except:" (it also catches Ctrl+C and sys.exit()).
#    Use "except Exception:" when you really want a catch-all, and log the error.

# 8. Re-raise: handle part of it, then let it continue
try:
    try:
        int("x")
    except ValueError:
        print("inner: logging the problem")
        raise                                   # the same exception continues upward
except ValueError:
    print("outer: caught it")
# inner: logging the problem
# outer: caught it

# 9. A retry loop
attempts = 0

def flaky():
    global attempts
    attempts += 1
    if attempts < 3:
        raise ConnectionError("no link")
    return "connected"

for attempt in range(1, 5):
    try:
        print(flaky())
        break
    except ConnectionError as e:
        print(f"attempt {attempt} failed: {e}")
else:
    print("gave up")
# attempt 1 failed: no link
# attempt 2 failed: no link
# connected

# 10. Skip bad items and keep going
total = 0
for v in ["1", "x", "3"]:
    try:
        total += int(v)
    except ValueError:
        continue
print(total)                                    # 4

# 11. Validate input until it is good (answers come from a list so the file runs by itself)
answers = iter(["abc", "-5", "42"])
while True:
    raw = next(answers)
    try:
        n = int(raw)
        if n < 0:
            raise ValueError("must be positive")
    except ValueError as e:
        print(f"invalid {raw!r}: {e}")
    else:
        print("accepted", n)
        break
# invalid 'abc': invalid literal for int() with base 10: 'abc'
# invalid '-5': must be positive
# accepted 42

# 12. EAFP: "easier to ask forgiveness than permission"
settings = {"port": 8080}
try:
    host = settings["host"]
except KeyError:
    host = "localhost"
print(host)                                     # localhost

# 13. Ignore one specific error on purpose
with suppress(FileNotFoundError):
    os.remove("no_such_file.txt")
print("still running")                          # still running

# KEEP THE try BLOCK SMALL: only the line that can fail, so you do not hide other bugs.
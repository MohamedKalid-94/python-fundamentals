from contextlib import contextmanager
import os

# finally: runs ALWAYS: after success, after an error, even after return, break or continue.
# Use it for CLEANUP: closing files, releasing locks, deselecting a chip.

# 1. finally runs even when the function returns inside try
def test():
    try:
        print("try")
        return "from try"
    finally:
        print("finally")

print(test())
# try
# finally
# from try

# 2. finally runs while an exception travels upward
try:
    try:
        1 / 0
    finally:
        print("cleanup")
except ZeroDivisionError:
    print("caught outside")
# cleanup
# caught outside

# 3. All four parts together
def run(value):
    try:
        result = 10 / value
    except ZeroDivisionError:
        print("except")
    else:
        print("else", result)
    finally:
        print("finally")

run(2)
# else 5.0
# finally
run(0)
# except
# finally

# 4. finally inside a loop (with continue)
for i in range(3):
    try:
        if i == 1:
            continue
        print("body", i)
    finally:
        print("finally", i)
# body 0
# finally 0
# finally 1
# body 2
# finally 2

# 5. Cleanup of a resource
class Port:
    def open(self):
        print("open")

    def close(self):
        print("close")

p = Port()
try:
    p.open()
    raise RuntimeError("boom")
except RuntimeError:
    print("handled")
finally:
    p.close()
# open
# handled
# close

# 6. TRAP: a return inside finally replaces the real result and SWALLOWS exceptions
def bad_return():
    try:
        return 1
    finally:
        return 2

def swallow():
    try:
        raise ValueError("lost")
    finally:
        return "swallowed"

print(bad_return(), swallow())                  # 2 swallowed
# (Never return, break or continue inside finally.)

# 7. try/finally without except: the exception is NOT handled, only cleaned up after
# 8. The "with" statement does the same job with less code
f = open("tmp.txt", "w", encoding="utf-8")
try:
    f.write("data")
finally:
    f.close()
print(f.closed)                                 # True

with open("tmp.txt", encoding="utf-8") as g:    # closes the file for you, even on errors
    text = g.read()
print(text, g.closed)                           # data True
os.remove("tmp.txt")

# 9. Your own "with" blocks with contextlib (generators are explained in Module 17)
@contextmanager
def chip_select(name):
    print("select", name)
    try:
        yield
    finally:
        print("deselect", name)

with chip_select("CS0"):
    print("transfer")
# select CS0
# transfer
# deselect CS0

try:
    with chip_select("CS1"):
        raise OSError("bus error")
except OSError:
    print("handled")
# select CS1
# deselect CS1          the chip is released even though the transfer failed
# handled
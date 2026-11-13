import math
import sys
import time
import types
from contextlib import contextmanager
from unittest.mock import patch

# MONKEY PATCHING: change a class, module or object while the program runs.
# Useful for tests, hot fixes and compatibility shims. Dangerous everywhere else.

# 1. Add a method to a class: it works even for objects that already exist
class Dog:
    pass

def speak(self):
    return "woof"

early = Dog()
Dog.speak = speak
print(early.speak(), Dog().speak())             # woof woof

# 2. Replace a method (keep the original so you can put it back)
original = Dog.speak
Dog.speak = lambda self: "WOOF"
print(Dog().speak())                            # WOOF
Dog.speak = original

# 3. Patch ONE object only
d = Dog()
d.speak = types.MethodType(lambda self: "instance", d)
print(d.speak(), Dog().speak())                 # instance woof

# 4. Wrap a function of a module
calls = []
original_sqrt = math.sqrt

def logged_sqrt(x):
    calls.append(x)
    return original_sqrt(x)

math.sqrt = logged_sqrt
print(math.sqrt(16))                            # 4.0
math.sqrt = original_sqrt
print(calls)                                    # [16]

# 5. Built-in types cannot be patched
try:
    str.shout = lambda s: s.upper()
except TypeError as e:
    print(type(e).__name__)                     # TypeError   (subclass str instead)

# 6. A safe way to patch: always restore, even after an error
_MISSING = object()

@contextmanager
def patched(obj, name, value):
    previous = getattr(obj, name, _MISSING)
    setattr(obj, name, value)
    try:
        yield
    finally:
        if previous is _MISSING:
            delattr(obj, name)
        else:
            setattr(obj, name, previous)

with patched(Dog, "speak", lambda self: "temp"):
    print(Dog().speak())                        # temp
print(Dog().speak())                            # woof
with patched(Dog, "extra", 1):
    print(Dog.extra)                            # 1
print(hasattr(Dog, "extra"))                    # False

# 7. THE BIG TRAP: patch the name where it is USED, not where it is defined
lib = types.ModuleType("lib")
lib.helper = lambda: "real"
sys.modules["lib"] = lib

consumer = types.ModuleType("consumer")
exec(
    "import lib\n"
    "from lib import helper\n"
    "def via_attribute():\n"
    "    return lib.helper()\n"
    "def via_name():\n"
    "    return helper()\n",
    consumer.__dict__,
)

lib.helper = lambda: "patched"                  # replace the function in the library module
print(consumer.via_attribute(), consumer.via_name())    # patched real
#   "import lib; lib.helper()" looks the name up in lib at CALL time, so it sees the patch.
#   "from lib import helper" copied the reference into consumer, so patch "consumer.helper" instead.
del sys.modules["lib"]

# 8. Patch the clock so a test does not wait
with patch("time.sleep") as fake_sleep:
    time.sleep(10)
    print(fake_sleep.call_args)                 # call(10)

# 9. Patch every method of a class afterwards (tracing)
class Robot:
    def move(self):
        return "moving"

    def turn(self):
        return "turning"

traced = []
for name, func in list(vars(Robot).items()):
    if callable(func) and not name.startswith("__"):
        def make_wrapper(name=name, func=func):
            def wrapper(*args, **kwargs):
                traced.append(name)
                return func(*args, **kwargs)
            return wrapper
        setattr(Robot, name, make_wrapper())

robot = Robot()
robot.move()
robot.turn()
print(traced)                                   # ['move', 'turn']

# WHEN IT IS OK
#   tests (use unittest.mock.patch or pytest's monkeypatch: they restore automatically)
#   a compatibility shim:  if not hasattr(module, "new_function"): module.new_function = fallback
#   a quick hot fix for a bug in a library you cannot change yet (leave a comment and a link to the bug)
# WHEN IT IS NOT
#   changing other people's code permanently; the result depends on import order and is invisible
# BETTER OPTIONS
#   subclassing, composition, dependency injection, a decorator, an adapter, a plugin hook
# DANGERS   hard to debug, breaks on library upgrades, thread-unsafe, invisible to type checkers and readers
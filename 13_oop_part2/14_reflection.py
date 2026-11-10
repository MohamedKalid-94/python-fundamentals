import inspect
import math

# REFLECTION (introspection): a program examines and changes ITSELF while it runs.

class Robot:
    """A simple robot."""
    wheels = 2

    def __init__(self, name):
        self.name = name
        self.battery = 100

    def move(self, steps: int = 1) -> str:
        return f"{self.name} moves {steps}"


r = Robot("R2")

# 1. What is this object?
print(type(r).__name__, r.__class__ is Robot)           # Robot True
print(Robot.__doc__)                                    # A simple robot.
print(vars(r))                                          # {'name': 'R2', 'battery': 100}
print([n for n in dir(r) if not n.startswith("_")])     # ['battery', 'move', 'name', 'wheels']

# 2. Read, write, test and delete attributes by NAME
print(getattr(r, "name"), getattr(r, "color", "none"))  # R2 none
setattr(r, "color", "red")
print(r.color)                                          # red
print(hasattr(r, "move"), hasattr(r, "fly"))            # True False
delattr(r, "color")
print(hasattr(r, "color"))                              # False

# 3. Call a method by its name
method = getattr(r, "move")
print(method(3))                                        # R2 moves 3
print(callable(method), callable(r.name))               # True False

# 4. The inspect module: signatures and members
sig = inspect.signature(Robot.move)
print(sig)                                              # (self, steps: int = 1) -> str
print(list(sig.parameters), sig.parameters["steps"].default)    # ['self', 'steps'] 1
print([n for n, _ in inspect.getmembers(Robot, inspect.isfunction)])   # ['__init__', 'move']
print(Robot.move.__annotations__)                       # {'steps': <class 'int'>, 'return': <class 'str'>}

# 5. A command dispatcher built on getattr
class Shell:
    def do_hello(self):
        return "hello!"

    def do_bye(self):
        return "bye!"

    def run(self, cmd):
        handler = getattr(self, f"do_{cmd}", None)
        return handler() if handler else "unknown"

sh = Shell()
print(sh.run("hello"), sh.run("bye"), sh.run("fly"))    # hello! bye! unknown

# 6. Build an object from a dictionary, without calling __init__
data = {"name": "Copy", "battery": 50}
clone = Robot.__new__(Robot)
clone.__dict__.update(data)
print(clone.move(2))                                    # Copy moves 2

# 7. Change a class while the program runs
setattr(Robot, "speed", 5)
print(r.speed)                                          # 5

# 8. Classes and modules are objects too
print(globals()["Robot"] is Robot, isinstance(Robot, type))     # True True
print(hasattr(math, "sqrt"), math.__name__)             # True math

# 9. The class hierarchy
class Sub(Robot):
    pass

print([c.__name__ for c in Sub.__mro__])                # ['Sub', 'Robot', 'object']
print([c.__name__ for c in Robot.__subclasses__()])     # ['Sub']

# WARNING: never pass text from users to getattr(), eval() or exec() without checking it.
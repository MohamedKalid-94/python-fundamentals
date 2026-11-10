# An INNER (nested) class is a class defined inside another class.
# Use it when the helper class makes sense ONLY inside the outer class.

class Car:
    class Engine:
        def __init__(self, hp):
            self.hp = hp

        def start(self):
            return f"Engine {self.hp}hp started"

    def __init__(self, name, hp):
        self.name = name
        self.engine = Car.Engine(hp)        # the outer class builds the inner object

    def start(self):
        return f"{self.name}: {self.engine.start()}"


c = Car("Zed", 150)
print(c.start())                            # Zed: Engine 150hp started

e = Car.Engine(90)                          # the inner class is reachable through the outer one
print(e.start())                            # Engine 90hp started

print(Car.Engine.__name__, Car.Engine.__qualname__)     # Engine Car.Engine
print(type(c.engine))                       # <class '__main__.Car.Engine'>


# An inner class does NOT see the outer object automatically: pass it in
class Outer:
    def __init__(self, name):
        self.name = name

    class Inner:
        def __init__(self, outer):
            self.outer = outer

        def show(self):
            return f"inner of {self.outer.name}"

    def make_inner(self):
        return Outer.Inner(self)


o = Outer("O1")
print(o.make_inner().show())                # inner of O1


# A private helper class (a leading underscore says "internal")
class Stack:
    class _Node:
        def __init__(self, value, below):
            self.value = value
            self.below = below

    def __init__(self):
        self._top = None

    def push(self, value):
        self._top = Stack._Node(value, self._top)

    def pop(self):
        node = self._top
        self._top = node.below
        return node.value


s = Stack()
s.push(1)
s.push(2)
print(s.pop(), s.pop())                     # 2 1


# A class defined inside a FUNCTION can use the function's variables
def make_multiplier(factor):
    class Multiplier:
        def apply(self, x):
            return x * factor
    return Multiplier

Triple = make_multiplier(3)
print(Triple().apply(7))                    # 21

# STYLE: many Python programmers define helper classes at module level
# (with an underscore) instead of nesting them. Nest only when it reads better.
import json


# A class can have SEVERAL parents: class C(A, B)

class Flyer:
    def move(self):
        return "flying"

    def fly(self):
        return "flap"


class Swimmer:
    def move(self):
        return "swimming"

    def swim(self):
        return "paddle"


class Duck(Flyer, Swimmer):
    pass


d = Duck()
print(d.move())                         # flying      (Flyer is listed first, so it wins)
print(d.fly(), d.swim())                # flap paddle
print(Duck.__bases__)
# (<class '__main__.Flyer'>, <class '__main__.Swimmer'>)

# The MRO (Method Resolution Order) is the order Python searches the classes
print([c.__name__ for c in Duck.__mro__])       # ['Duck', 'Flyer', 'Swimmer', 'object']

# Call a specific parent explicitly
print(Flyer.move(d), Swimmer.move(d))   # flying swimming


# THE DIAMOND: B and C both inherit from A, and D inherits from B and C
class A:
    def hello(self):
        print("A")

class B(A):
    def hello(self):
        print("B")
        super().hello()

class C(A):
    def hello(self):
        print("C")
        super().hello()

class D(B, C):
    def hello(self):
        print("D")
        super().hello()

D().hello()
# D
# B
# C
# A             A runs ONCE, because super() follows the MRO
print([c.__name__ for c in D.__mro__])  # ['D', 'B', 'C', 'A', 'object']


# MIXINS: small classes that add one ability to any class
class JsonMixin:
    def to_json(self):
        return json.dumps(self.__dict__)

class LogMixin:
    def log(self, message):
        print(f"[{type(self).__name__}] {message}")

class Robot(LogMixin, JsonMixin):
    def __init__(self, name):
        self.name = name

r = Robot("R2")
r.log("started")                        # [Robot] started
print(r.to_json())                      # {"name": "R2"}


# An impossible order raises an error when the class is created
try:
    class Bad(A, B):                    # B is a subclass of A, so A cannot come first
        pass
except TypeError:
    print("TypeError")                  # TypeError

# ADVICE
# - Use multiple inheritance mainly for small, stateless mixins.
# - For "has-a" relationships, prefer composition: put an object inside another object.
# DYNAMIC (late) BINDING: which method runs is decided WHEN THE CALL HAPPENS,
# from the real type of the object, not from the name of the variable.

class Shape:
    def area(self):
        return 0

    def describe(self):
        return f"{type(self).__name__} area={self.area()}"


class Sq(Shape):
    def __init__(self, s):
        self.s = s

    def area(self):
        return self.s ** 2


shape = Shape()
print(shape.describe())                     # Shape area=0
shape = Sq(3)                               # the same variable now holds another type
print(shape.describe())                     # Sq area=9

for obj in (Shape(), Sq(1), Sq(4)):
    print(obj.describe())
# Shape area=0
# Sq area=1
# Sq area=16

# The method NAME can be chosen at run time
name = "area"
print(getattr(shape, name)())               # 9

# Methods can be added to a class while the program runs, and old objects see them
Sq.perimeter = lambda self: 4 * self.s
print(shape.perimeter())                    # 12

# An instance attribute is looked up BEFORE the class, so it can hide a method
tweaked = Sq(2)
tweaked.area = lambda: 100
print(tweaked.describe())                   # Sq area=100
print(Sq(3).area())                         # 9       other objects are unchanged

# A bound method remembers its object
m = shape.describe
print(type(m).__name__)                     # method
print(m.__self__ is shape, m.__func__ is Shape.describe)    # True True

# Binding of names: Python looks up everything at the moment of the call.
# That is why a missing method is found only when you run that line:
try:
    shape.fly()
except AttributeError:
    print("AttributeError")                 # AttributeError

# In C you get the same effect with a table of function pointers (a "vtable");
# in C++ it needs the keyword "virtual". In Python every method call works like that.
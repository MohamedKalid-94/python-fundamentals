# A class with nothing in it (pass is a placeholder)
class Empty:
    pass

e = Empty()
print(type(e), isinstance(e, Empty))    # <class '__main__.Empty'> True


# A real class
class Dog:
    def __init__(self, name, age):      # runs when you create an object
        self.name = name                # instance attributes belong to ONE object
        self.age = age

    def bark(self):
        return f"{self.name} says woof"

    def birthday(self):
        self.age += 1


rex = Dog("Rex", 3)                     # create an object (an "instance")
print(rex.name, rex.age)                # Rex 3
print(rex.bark())                       # Rex says woof
rex.birthday()
print(rex.age)                          # 4

# rex.bark() is a shortcut for Dog.bark(rex): that is what "self" is
print(Dog.bark(rex))                    # Rex says woof

# Each object has its OWN data
a = Dog("A", 1)
b = Dog("B", 2)
a.age = 10
print(a.age, b.age)                     # 10 2

# Attributes can be added to one object later (legal, but avoid it)
rex.color = "brown"
print(rex.color)                        # brown
print(rex.__dict__)                     # {'name': 'Rex', 'age': 4, 'color': 'brown'}

# Delete an attribute, and check for one
del rex.color
print(hasattr(rex, "color"))            # False

try:
    print(rex.weight)
except AttributeError as err:
    print(type(err).__name__)           # AttributeError

# Default == compares IDENTITY (the same object), not the contents
x1, x2 = Dog("X", 1), Dog("X", 1)
print(x1 == x2, x1 is x2)               # False False


# __str__ (for people) and __repr__ (for developers)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"


p = Point(1, 2)
print(p)                                # (1, 2)
print(repr(p))                          # Point(1, 2)
print([p])                              # [Point(1, 2)]      (containers show repr)

# Objects are passed by reference: a function can change them
def grow(dog):
    dog.age += 1

grow(rex)
print(rex.age)                          # 5

# Objects in collections
dogs = [Dog("A", 1), Dog("B", 5)]
print([d.name for d in dogs])           # ['A', 'B']
print(max(dogs, key=lambda d: d.age).name)      # B

# A class is an object too
print(type(Dog), Dog.__name__)          # <class 'type'> Dog

# Calling an instance method on the CLASS without an object
try:
    Dog.bark()
except TypeError as err:
    print(type(err).__name__)           # TypeError

# Naming: ClassNames use CapWords; attributes and methods use snake_case
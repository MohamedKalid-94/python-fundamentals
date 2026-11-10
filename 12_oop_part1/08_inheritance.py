# A child class INHERITS the attributes and methods of its parent class.

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

    def eat(self):
        return f"{self.name} is eating"


class Dog(Animal):                      # Dog(Animal): Animal is the parent (base) class
    def __init__(self, name, breed):
        super().__init__(name)          # run the parent's __init__
        self.breed = breed

    def speak(self):                    # OVERRIDE: replace the parent's version
        return f"{self.name} says woof"


class Cat(Animal):                      # inherits everything, adds nothing
    pass


d = Dog("Rex", "Lab")
print(d.speak())                        # Rex says woof       (overridden)
print(d.eat())                          # Rex is eating       (inherited)
print(d.breed)                          # Lab
print(Cat("Tom").speak())               # Tom makes a sound

# Checking relationships
print(isinstance(d, Dog), isinstance(d, Animal), isinstance(Animal("x"), Dog))
# True True False
print(issubclass(Dog, Animal), issubclass(Animal, Dog))     # True False
print(type(d) is Dog, type(d) is Animal)                    # True False

print(Dog.__bases__)                    # (<class '__main__.Animal'>,)
print([c.__name__ for c in Dog.__mro__])        # ['Dog', 'Animal', 'object']
print(Animal.__bases__)                 # (<class 'object'>,)    every class inherits from object

# Extend a parent's method instead of replacing it
class Puppy(Dog):
    def speak(self):
        return super().speak() + " (squeaky)"

print(Puppy("Bit", "Pug").speak())      # Bit says woof (squeaky)

# TRAP: forgetting super().__init__() leaves the parent's attributes unset
class Broken(Animal):
    def __init__(self):
        pass

try:
    Broken().speak()
except AttributeError:
    print("AttributeError")             # AttributeError

# Attribute lookup order: the object, then its class, then the parents
class Parent:
    x = "parent"

class Child(Parent):
    pass

print(Child.x, Child().x)               # parent parent
Child.x = "child"
print(Child.x, Parent.x)                # child parent

# Method overriding is covered fully in Module 13.
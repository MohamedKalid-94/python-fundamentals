# INSTANCE attribute: set on self, belongs to ONE object
# CLASS attribute: set in the class body, SHARED by all objects

class Dog:
    species = "Canis familiaris"        # class attribute
    count = 0                           # class attribute used as a counter

    def __init__(self, name):
        self.name = name                # instance attribute
        Dog.count += 1


a = Dog("A")
b = Dog("B")
print(a.species, "|", b.species, "|", Dog.species)
# Canis familiaris | Canis familiaris | Canis familiaris
print(Dog.count, a.count)               # 2 2

# Changing the class attribute changes it for every object
Dog.species = "Canis lupus"
print(a.species, b.species)             # Canis lupus Canis lupus

# Assigning through an OBJECT creates a new INSTANCE attribute that hides the class one
a.species = "Custom"
print(a.species, b.species, Dog.species)    # Custom Canis lupus Canis lupus
print("species" in a.__dict__, "species" in b.__dict__, "species" in Dog.__dict__)
# True False True

del a.species                           # remove the hiding attribute
print(a.species)                        # Canis lupus

print(sorted(k for k in vars(Dog) if not k.startswith("__")))   # ['count', 'species']

# TRAP 1: += on a class attribute through an object
class C:
    n = 0

c = C()
c.n += 1                                # reads C.n (0), then creates c.n = 1
print(c.n, C.n)                         # 1 0

# TRAP 2: a MUTABLE class attribute is shared by all objects
class Bad:
    items = []

    def add(self, x):
        self.items.append(x)

x1, x2 = Bad(), Bad()
x1.add(1)
print(x2.items)                         # [1]      x2 sees the item of x1!

class Good:
    def __init__(self):
        self.items = []                 # one list per object

    def add(self, x):
        self.items.append(x)

g1, g2 = Good(), Good()
g1.add(1)
print(g2.items)                         # []

# Class attributes are good for constants and shared settings
class Uart:
    BAUD_RATES = (9600, 19200, 115200)
    DEFAULT_BAUD = 9600

print(Uart.DEFAULT_BAUD, 115200 in Uart.BAUD_RATES)     # 9600 True

# type(self).count keeps a separate counter for each subclass
class Base:
    count = 0

    def __init__(self):
        type(self).count += 1

class Sub(Base):
    pass

Sub()
Sub()
Base()
print(Base.count, Sub.count)            # 1 2
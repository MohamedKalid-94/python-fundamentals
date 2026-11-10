# OVERRIDING: a child class defines a method with the SAME NAME as its parent's,
# and the child's version is used for child objects.

class Animal:
    sound = "..."

    def speak(self):
        return f"{type(self).__name__}: {self.sound}"

    def describe(self):
        return f"I am {self.speak()}"       # calls speak() of the REAL object


class Dog(Animal):
    sound = "woof"                          # overriding a class attribute


class Cat(Animal):
    def speak(self):                        # replaces the parent's method completely
        return "Cat: meow"


class Bird(Animal):
    def speak(self):                        # extends the parent's method with super()
        return super().speak() + " tweet"


print(Animal().speak())                     # Animal: ...
print(Dog().speak())                        # Dog: woof
print(Cat().speak())                        # Cat: meow
print(Bird().speak())                       # Bird: ... tweet
print(Cat().describe())                     # I am Cat: meow     (inherited describe, overridden speak)

# Which function does each class really use?
print(Cat.speak is Animal.speak, Dog.speak is Animal.speak)     # False True


# Overriding a method of a built-in class
class LoudList(list):
    def append(self, item):
        print("adding", item)
        super().append(item)


ll = LoudList()
ll.append(1)                                # adding 1
print(ll)                                   # [1]


# The template idea: the parent calls methods that children replace
class Report:
    def header(self):
        return "HEADER"

    def body(self):
        return "generic body"

    def render(self):
        return f"{self.header()} | {self.body()}"


class SalesReport(Report):
    def body(self):
        return "sales body"


print(SalesReport().render())               # HEADER | sales body


# RULE: keep the same signature, or callers written for the parent will break
class Base:
    def run(self, x):
        return x

class Bad(Base):
    def run(self):                          # a different signature
        return 0

try:
    Bad().run(5)
except TypeError:
    print("TypeError")                      # TypeError

# Overriding constants
class Limits:
    MAX = 10

class BigLimits(Limits):
    MAX = 20

print(Limits().MAX, BigLimits().MAX)        # 10 20

# Python has no "final" keyword. A method can always be overridden
# (typing.final only warns type checkers).
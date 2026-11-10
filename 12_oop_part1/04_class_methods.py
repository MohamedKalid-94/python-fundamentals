# @classmethod receives the CLASS (cls) instead of an object (self).
# Typical uses: alternative constructors, and work with class-level data.

class Person:
    population = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Person.population += 1

    @classmethod
    def from_birth_year(cls, name, birth_year, current_year=2026):
        return cls(name, current_year - birth_year)

    @classmethod
    def from_string(cls, text):
        name, age = text.split("-")
        return cls(name, int(age))

    @classmethod
    def get_population(cls):
        return cls.population


p1 = Person("Ann", 30)
p2 = Person.from_string("Bob-25")
p3 = Person.from_birth_year("Cy", 2000)
print(p2.name, p2.age)                  # Bob 25
print(p3.name, p3.age)                  # Cy 26
print(Person.get_population())          # 3


# cls is the class that was called, so subclasses work automatically
class Student(Person):
    pass

s = Student.from_string("Di-20")
print(type(s).__name__, s.age)          # Student 20

# A class method can also be called through an object
print(p1.get_population())              # 4


# A class method that changes the class state
class Config:
    debug = False

    @classmethod
    def enable_debug(cls):
        cls.debug = True

Config.enable_debug()
print(Config.debug)                     # True


# Another alternative constructor
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @classmethod
    def from_fahrenheit(cls, f):
        return cls((f - 32) * 5 / 9)

    @classmethod
    def from_kelvin(cls, k):
        return cls(k - 273.15)

print(round(Temperature.from_fahrenheit(212).celsius, 1))   # 100.0
print(round(Temperature.from_kelvin(273.15).celsius, 1))    # 0.0
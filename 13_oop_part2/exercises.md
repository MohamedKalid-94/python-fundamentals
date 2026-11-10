Write the questions as # comments and your solutions as code below each one.

Create Employee, Manager and Intern classes where each overrides pay(). Use super() in Manager, then print the total payroll of a mixed list.
Override __str__ and __eq__ in a Money class (amount and currency). Show that two equal objects compare equal, and explain why you must also think about __hash__.
Show that two methods with the same name in one class keep only the last one. Then write area(*args) that works for a circle (1 argument) and a rectangle (2 arguments), and a version with singledispatch that works on a Circle and a Rect object.
Implement Vector with +, -, * (number), ==, abs(), __repr__, and __radd__ so sum(vectors) works.
Demonstrate dynamic binding: put 4 different shapes in a list, call area() on each, then add a perimeter() method to one class after the objects already exist and call it.
Write a function to_number(text) that tries int, then float, then returns None, and test it on 6 inputs. Explain in a comment how this differs from isinstance checks.
Create an abstract Device with connect(), read() and a concrete report(). Implement TempSensor and PressureSensor, show the error when you forget a method, and use an abstract property unit.
Write a BankAccount with a private balance and a read-only balance property, a validated deposit, withdraw, and a history property that returns a copy of the list (so callers cannot change it).
Write a Temperature class with celsius, fahrenheit and kelvin properties where setting any one updates the others, and a ValueError below absolute zero.
Define a Protocol called Sensor with read(). Write three unrelated classes that match it, and a function average_reading(sensors). Add a fake sensor for testing.
Create a package shapes with __init__.py, circle.py, rectangle.py and a sub-package tools that has units.py. Import from it in 4 different ways, and use a relative import inside the package.
Write a Car class with an inner Engine class and an inner Wheel class, and a car with 4 wheels. Print the engine’s power and the number of wheels.
Use type() to create a class Dynamic with two attributes and one method, create an object, and call the method. Then convert a JSON string into an object with SimpleNamespace.
Write a thread-safe Logger singleton (use threading.Lock) in two ways: with __new__, and with a module-level instance. Start 5 threads that each log one line, and print the total number of lines.
Write Celsius(float) and Percent(int) wrapper subclasses with validation (Percent must be between 0 and 100) and show that arithmetic returns plain numbers unless you override the operators.
Write a Proxy wrapper class that logs every attribute access and method call of the wrapped object, using __getattr__. Test it on a list and on a custom object.
Define an Enum for traffic-light states, with a method next() that returns the following state and a property seconds. Run the cycle 6 times. Then define an IntFlag for 8 hardware status bits and test, set and clear them.
Use reflection to write describe(obj) that prints the class name, the module, the public attributes with their values, and the public methods with their signatures.
Write a command-line style dispatcher: run("add 2 3"), run("mul 4 5"), run("help"), using getattr, with an error message for unknown commands and for the wrong number of arguments.
Rewrite the Packet example as a @dataclass(frozen=True) with from_bytes (class method) and to_bytes methods and a checksum check that raises ValueError. Test a good and a corrupted packet.
Create a @dataclass(order=True) called Task with priority and name, sort 5 tasks, convert one to a dictionary and to JSON, and show what replace() does.
Predict first, then run, and explain each result in a comment:
python
from enum import Enum
from dataclasses import dataclass

class Color(Enum):
    RED = 1
    GREEN = 1
    BLUE = 2

print(Color.GREEN is Color.RED, len(Color), Color(1).name, Color.BLUE.value)

@dataclass
class P:
    x: int
    y: int = 0

p, q = P(1), P(1, 0)
print(p == q, p is q, p)

class Base:
    def hello(self):
        return "base"
    def run(self):
        return self.hello()

class Child(Base):
    def hello(self):
        return "child+" + super().hello()

print(Child().run(), Base().run())
print(isinstance(True, int), getattr(p, "z", "none"), hasattr(Child, "hello"))
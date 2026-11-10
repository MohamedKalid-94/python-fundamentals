exercises.py

Write the questions as # comments and your solutions as code below each one.

Create a Book class with title, author and pages, a method describe() that returns a sentence, and __str__ and __repr__. Create 3 books and print them in a list.
Create a Rectangle class with width, height, area(), perimeter() and is_square(). Add __eq__ so two rectangles with the same size compare equal.
Create a Counter class with a class attribute that counts how many objects were created, and a class method how_many(). Delete one object and explain why the counter does not go down (unless you handle __del__).
Show the shared-mutable-class-attribute trap with a Team class that has members = [], then fix it.
Add class methods from_string("Ann,30,Pune") and from_dict({...}) to a Person class, and a static method is_adult(age).
Write a Temperature class with from_fahrenheit, from_kelvin and static conversion helpers, and test round trips (C to F to C).
Write BankAccount with a private balance, deposit, withdraw (no overdraft), transfer(other, amount) and a transaction history. Then show that account.__balance fails and account._BankAccount__balance works.
Create Animal, Dog and Cat classes with an speak() method. Put 5 animals in a list and call speak() on each. Add a Cow class that has no parent but still works (duck typing).
Build Vehicle -> Car -> SportsCar with super().__init__ at each level and an info() method that adds to the parent’s text. Print the MRO.
Create Flyer, Swimmer and Walker mixins and a Duck class that uses all three. Print the MRO and show which move() wins, then change the order of the parents.
Reproduce the diamond problem with A, B, C, D and show the order of the super() calls. Then try to create a class with an impossible MRO and catch the error.
Create a Vector2D class with +, -, * (by a number), ==, abs() (length), __repr__ and __bool__ (false for the zero vector).
Create a Shape base class with area() that raises NotImplementedError, then Circle, Rectangle and Triangle. Write total_area(shapes) and print the shape with the largest area.
Create a Stack and a Queue class (with a list or collections.deque). Use the stack to check balanced brackets and the queue to simulate a printer with jobs arriving in order.
Write a LinkedList class with append, prepend, remove(value), __len__, __iter__ and __repr__. Test it with 5 values.
Embedded: write a Register class that stores an 8-bit value, with set_bit(n), clear_bit(n), toggle_bit(n), test_bit(n) and __repr__ that prints the value in binary (0b00001010). Validate that n is between 0 and 7.
Embedded: write a Packet class with a header, payload and a static checksum(data); a to_bytes() method that returns the whole packet as bytes; and a class method from_bytes(data) that rebuilds it and verifies the checksum (raise ValueError if it does not match).
Embedded: write a Device -> Sensor -> (TempSensor, PressureSensor) hierarchy, put 4 sensors in a list, connect them all, and print a report for each. Add a LogMixin to log every read.
Show that isinstance accepts a tuple of classes and that issubclass(bool, int) is true. Then write a function that behaves differently for int, str and list, and explain why duck typing is usually better than isinstance checks.
Predict first, then run, and explain each result in a comment:
python
class A:
    x = 1
    def __init__(self):
        self.y = 2
    def who(self):
        return "A"

class B(A):
    def who(self):
        return "B+" + super().who()

class C(A):
    def who(self):
        return "C+" + super().who()

class D(B, C):
    pass

d = D()
print(d.who(), [k.__name__ for k in D.__mro__])
d.x = 10
print(d.x, A.x, D.x)
A.x = 99
print(d.x, B.x, C().x)
print(vars(d), isinstance(d, C), issubclass(B, C))
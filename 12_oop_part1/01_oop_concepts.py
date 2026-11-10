# OOP = organise a program around OBJECTS that bundle DATA and the FUNCTIONS that work on it.
#
#   class      a blueprint (like a C struct type plus its functions)
#   object     one thing built from the blueprint (also called an INSTANCE)
#   attribute  a variable that belongs to an object or a class
#   method     a function that belongs to a class
#   self       the object a method is working on (like the "this" pointer)
#
# THE FOUR PILLARS
#   Encapsulation   keep data and the code that uses it together; hide the details
#   Abstraction     show a simple interface, hide the complicated inside
#   Inheritance     a new class reuses and extends an existing class
#   Polymorphism    different classes respond to the same call in their own way

# --- 1. The procedural way: a dictionary plus functions ---
account = {"owner": "Ann", "balance": 100}

def deposit(acc, amount):
    acc["balance"] += amount

deposit(account, 50)
print(account)                          # {'owner': 'Ann', 'balance': 150}

# --- 2. The object way: data and behaviour in one place ---
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

acc = Account("Ann", 100)
acc.deposit(50)
print(acc.balance)                      # 150

# --- 3. An embedded-style example ---
# In C:  led_on(&led);        In Python:  led.on()
class Led:
    def __init__(self, pin):
        self.pin = pin
        self.state = "OFF"

    def on(self):
        self.state = "ON"

    def off(self):
        self.state = "OFF"

led = Led(13)
print(led.state)                        # OFF
led.on()
print(led.state)                        # ON

# --- 4. In Python EVERYTHING is an object ---
print(type(5), type("a"), type(len), type(int))
# <class 'int'> <class 'str'> <class 'builtin_function_or_method'> <class 'type'>
print(isinstance(5, object))            # True
print((5).bit_length(), "abc".upper())  # 3 ABC
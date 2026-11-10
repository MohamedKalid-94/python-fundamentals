# Python has NO real private or protected members. It uses NAMING CONVENTIONS.
#
#   name       public      use it freely
#   _name      "protected" internal: please do not use it from outside the class
#   __name     "private"   name mangling: stored as _ClassName__name
#   __name__   special     reserved for Python (not mangled)

class Account:
    def __init__(self, owner, balance):
        self.owner = owner              # public
        self._bank = "ABC"              # protected (convention)
        self.__balance = balance        # private (name-mangled)

    def get_balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.__balance += amount


acc = Account("Ann", 100)
print(acc.owner, acc._bank)             # Ann ABC          _bank still works

try:
    print(acc.__balance)
except AttributeError as err:
    print(type(err).__name__)           # AttributeError

print(acc.get_balance())                # 100
print(acc._Account__balance)            # 100       the mangled name: reachable, but a bad idea
print(sorted(vars(acc)))                # ['_Account__balance', '_bank', 'owner']

try:
    acc.deposit(-5)
except ValueError as err:
    print(err)                          # amount must be positive

# Mangling only happens INSIDE the class body, so this creates a NEW attribute
acc.__balance = 999
print(acc.__balance, acc.get_balance()) # 999 100


# Private methods
class Safe:
    def __code(self):
        return "1234"

    def open(self, guess):
        return guess == self.__code()

s = Safe()
print(s.open("1234"))                   # True
try:
    s.__code()
except AttributeError as err:
    print(type(err).__name__)           # AttributeError
print(s._Safe__code())                  # 1234


# Why mangling exists: a subclass cannot accidentally clash with a parent's private name
class A:
    def __init__(self):
        self.__x = 1

class B(A):
    def set_x(self):
        self.__x = 2                    # becomes _B__x, not _A__x

b = B()
b.set_x()
print(sorted(vars(b)))                  # ['_A__x', '_B__x']

# SUMMARY
# - Use _name for "internal, hands off" (the normal Python choice).
# - Use __name only when you really need to avoid clashes with subclasses.
# - Neither is security: Python trusts the programmer ("we are all consenting adults").
# - Controlled access with @property is in Module 13 (Encapsulation).
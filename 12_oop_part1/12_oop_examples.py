# 1. A bank account: private balance, validation, history, class attribute
class BankAccount:
    bank_name = "PyBank"

    def __init__(self, owner, balance=0):
        if balance < 0:
            raise ValueError("opening balance cannot be negative")
        self.owner = owner
        self.__balance = balance
        self.history = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.__balance += amount
        self.history.append(("deposit", amount))

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("insufficient funds")
        self.__balance -= amount
        self.history.append(("withdraw", amount))

    def get_balance(self):
        return self.__balance

    def __str__(self):
        return f"{self.owner}: {self.__balance}"


acc = BankAccount("Ann", 100)
acc.deposit(50)
acc.withdraw(30)
print(acc.get_balance())                # 120
try:
    acc.withdraw(500)
except ValueError as err:
    print(err)                          # insufficient funds
print(acc.history)                      # [('deposit', 50), ('withdraw', 30)]
print(acc, BankAccount.bank_name)       # Ann: 120 PyBank


# 2. A stack class built on a list
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"


s = Stack()
for n in (1, 2, 3):
    s.push(n)
print(s.pop())                          # 3
print(s.peek())                         # 2
print(len(s), s, s.is_empty())          # 2 Stack([1, 2]) False
s.pop()
s.pop()
try:
    s.pop()
except IndexError as err:
    print(err)                          # pop from empty stack


# 3. Payroll: inheritance and polymorphism
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def pay(self):
        return self.salary


class Manager(Employee):
    def __init__(self, name, salary, bonus):
        super().__init__(name, salary)
        self.bonus = bonus

    def pay(self):
        return super().pay() + self.bonus


class Intern(Employee):
    def pay(self):
        return self.salary // 2


staff = [Employee("Ann", 3000), Manager("Bob", 5000, 1000), Intern("Cy", 2000)]
for e in staff:
    print(f"{e.name}: {e.pay()}")
# Ann: 3000
# Bob: 6000
# Cy: 1000
print("Total:", sum(e.pay() for e in staff))        # Total: 10000


# 4. An embedded-style device hierarchy
class Device:
    def __init__(self, name):
        self.name = name
        self.connected = False

    def connect(self):
        self.connected = True
        return f"{self.name} connected"


class Sensor(Device):
    def __init__(self, name, unit):
        super().__init__(name)
        self.unit = unit

    def read(self):
        raise NotImplementedError("subclasses must implement read()")

    def report(self):
        return f"{self.name}: {self.read()} {self.unit}"


class TempSensor(Sensor):
    SCALE = 10                          # raw counts per degree

    def __init__(self, name, raw):
        super().__init__(name, "C")
        self._raw = raw

    @staticmethod
    def raw_to_celsius(raw):
        return round(raw / TempSensor.SCALE, 1)

    def read(self):
        return self.raw_to_celsius(self._raw)


class PressureSensor(Sensor):
    def __init__(self, name, hpa):
        super().__init__(name, "hPa")
        self._hpa = hpa

    def read(self):
        return self._hpa


for sensor in [TempSensor("t1", 253), PressureSensor("p1", 1013)]:
    print(sensor.connect())
    print(sensor.report())
# t1 connected
# t1: 25.3 C
# p1 connected
# p1: 1013 hPa

try:
    Sensor("x", "u").read()
except NotImplementedError:
    print("NotImplementedError")        # NotImplementedError


# 5. A linked list (two classes working together)
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        node = Node(value)
        if self.head is None:
            self.head = node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = node

    def to_list(self):
        result, current = [], self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

    def contains(self, value):
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False


ll = LinkedList()
for v in (1, 2, 3):
    ll.append(v)
print(ll.to_list(), ll.contains(2), ll.contains(9))     # [1, 2, 3] True False


# 6. A mixin that adds logging to any class
class LogMixin:
    def log(self, message):
        print(f"[{type(self).__name__}] {message}")


class Motor(LogMixin):
    def __init__(self):
        self.rpm = 0

    def set_rpm(self, rpm):
        self.rpm = rpm
        self.log(f"rpm set to {rpm}")


Motor().set_rpm(1500)                   # [Motor] rpm set to 1500
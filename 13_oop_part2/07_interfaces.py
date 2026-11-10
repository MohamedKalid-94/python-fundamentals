from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

# Python has no "interface" keyword. You get the same result in three ways:
#   1. an abstract class with only abstract methods (ABC)    - declared, enforced
#   2. a Protocol                                           - structural, checked by type checkers
#   3. plain duck typing                                    - no declaration at all

# --- 1. ABC interfaces (a class may implement several) ---
class Readable(ABC):
    @abstractmethod
    def read(self):
        ...


class Writable(ABC):
    @abstractmethod
    def write(self, data):
        ...


class File(Readable, Writable):
    def __init__(self):
        self.data = []

    def read(self):
        return list(self.data)

    def write(self, data):
        self.data.append(data)


f = File()
f.write("a")
f.write("b")
print(f.read())                             # ['a', 'b']
print(isinstance(f, Readable), isinstance(f, Writable))     # True True

class Incomplete(Readable):
    pass

try:
    Incomplete()
except TypeError:
    print("TypeError")                      # the interface is not fully implemented


# --- 2. Protocol: a class matches by HAVING the methods, with no inheritance ---
@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...


class Resource:
    def close(self):
        print("closed")


class NoClose:
    pass


print(isinstance(Resource(), Closeable), isinstance(NoClose(), Closeable))     # True False

def shutdown(items):
    for item in items:
        if isinstance(item, Closeable):
            item.close()

shutdown([Resource(), NoClose(), Resource()])
# closed
# closed


# --- 3. Registering a class that you cannot change ---
class Plugin(ABC):
    @abstractmethod
    def run(self):
        ...

class External:
    def run(self):
        return "run"

Plugin.register(External)                   # External becomes a "virtual subclass"
print(isinstance(External(), Plugin), issubclass(External, Plugin))     # True True


# --- The standard library uses this idea everywhere ---
from collections.abc import Iterable, Sized
print(isinstance([1], Iterable), isinstance("ab", Sized), isinstance(5, Sized))
# True True False


# --- A testing benefit: a fake that fits the same interface ---
class RealSensor:
    def read(self):
        return 90

class FakeSensor:
    def read(self):
        return 20

def monitor(sensor, limit):
    return "ALARM" if sensor.read() > limit else "ok"

print(monitor(RealSensor(), 80), monitor(FakeSensor(), 80))     # ALARM ok
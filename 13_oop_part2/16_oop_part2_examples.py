import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, IntFlag, auto


# 1. A factory: ABC + dataclass + Enum
class Shape(ABC):
    @abstractmethod
    def area(self):
        ...


@dataclass
class Circle(Shape):
    r: float

    def area(self):
        return round(math.pi * self.r ** 2, 2)


@dataclass
class Rect(Shape):
    w: float
    h: float

    def area(self):
        return self.w * self.h


class Kind(Enum):
    CIRCLE = auto()
    RECT = auto()


def make(kind, *args):
    return {Kind.CIRCLE: Circle, Kind.RECT: Rect}[kind](*args)


shapes = [make(Kind.CIRCLE, 1), make(Kind.RECT, 2, 3)]
print(shapes)                               # [Circle(r=1), Rect(w=2, h=3)]
print([s.area() for s in shapes])           # [3.14, 6]


# 2. A thermostat state machine: dataclass + Enum
class State(Enum):
    IDLE = auto()
    HEATING = auto()
    COOLING = auto()


@dataclass
class Thermostat:
    target: float
    state: State = State.IDLE

    def update(self, current):
        if current < self.target - 1:
            self.state = State.HEATING
        elif current > self.target + 1:
            self.state = State.COOLING
        else:
            self.state = State.IDLE
        return self.state


t = Thermostat(21.0)
for temp in (18.0, 21.5, 24.0):
    print(temp, t.update(temp).name)
# 18.0 HEATING
# 21.5 IDLE
# 24.0 COOLING


# 3. A hardware register: properties + IntFlag
class Ctrl(IntFlag):
    ENABLE = 1
    IRQ = 2
    DMA = 4


class Register:
    def __init__(self):
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if not 0 <= v <= 0xFF:
            raise ValueError("8-bit value required")
        self._value = v

    def set(self, flag):
        self.value = self._value | int(flag)

    def clear(self, flag):
        self.value = self._value & ~int(flag) & 0xFF

    def has(self, flag):
        return bool(self._value & int(flag))

    def __repr__(self):
        return f"Register({self._value:#010b})"


reg = Register()
reg.set(Ctrl.ENABLE)
reg.set(Ctrl.DMA)
print(reg)                                  # Register(0b00000101)
print(reg.has(Ctrl.IRQ), reg.has(Ctrl.DMA)) # False True
reg.clear(Ctrl.ENABLE)
print(reg)                                  # Register(0b00000100)
try:
    reg.value = 300
except ValueError as err:
    print(err)                              # 8-bit value required


# 4. An adapter that makes a legacy sensor fit a new interface
class LegacySensor:
    def read_raw(self):
        return 2530                         # tenths of a degree


class SensorAdapter:
    def __init__(self, legacy):
        self._legacy = legacy

    def read(self):
        return self._legacy.read_raw() / 10


def report(sensor):
    return f"{sensor.read():.1f} C"

print(report(SensorAdapter(LegacySensor())))        # 253.0 C


# 5. A command dispatcher with reflection
class Shell:
    def do_hello(self, name="world"):
        return f"hello {name}"

    def do_add(self, a, b):
        return int(a) + int(b)

    def run(self, line):
        cmd, *args = line.split()
        handler = getattr(self, f"do_{cmd}", None)
        return handler(*args) if handler else f"unknown command: {cmd}"


sh = Shell()
print(sh.run("hello Ann"))                  # hello Ann
print(sh.run("add 2 3"))                    # 5
print(sh.run("fly"))                        # unknown command: fly


# 6. A singleton event bus with callable subscribers
class EventBus:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.handlers = {}
        return cls._instance

    def subscribe(self, event, handler):
        self.handlers.setdefault(event, []).append(handler)

    def publish(self, event, data):
        return [h(data) for h in self.handlers.get(event, [])]


EventBus().subscribe("temp", lambda v: f"display {v}")
EventBus().subscribe("temp", lambda v: f"log {v}")
print(EventBus().publish("temp", 25))       # ['display 25', 'log 25']
print(EventBus().publish("none", 0))        # []
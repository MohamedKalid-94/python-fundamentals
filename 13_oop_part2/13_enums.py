from enum import Enum, IntEnum, IntFlag, StrEnum, auto, unique

# An ENUM is a fixed set of named constants.

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


print(Color.RED)                            # Color.RED
print(Color.RED.name, Color.RED.value)      # RED 1
print(Color(2), Color["BLUE"])              # Color.GREEN Color.BLUE   (by value, by name)
print(list(Color))                          # [<Color.RED: 1>, <Color.GREEN: 2>, <Color.BLUE: 3>]
print(len(Color), list(Color.__members__))  # 3 ['RED', 'GREEN', 'BLUE']

for c in Color:
    print(c.name, c.value)
# RED 1
# GREEN 2
# BLUE 3

# Members are singletons: compare with == or "is"
print(Color.RED == Color.RED, Color.RED is Color.RED, Color.RED == 1)   # True True False
print(isinstance(Color.RED, Color))         # True

try:
    Color(9)
except ValueError as err:
    print(err)                              # 9 is not a valid Color

try:
    Color.RED = 5                           # members are constants
except AttributeError:
    print("AttributeError")                 # AttributeError

try:
    Color.RED < Color.GREEN                 # plain enums have no order
except TypeError:
    print("TypeError")                      # TypeError

# Members as dictionary keys
speeds = {Color.RED: "stop", Color.GREEN: "go"}
print(speeds[Color.GREEN])                  # go

# Two names for one value make an ALIAS
class Dup(Enum):
    A = 1
    B = 1

print(Dup.B is Dup.A, list(Dup))            # True [<Dup.A: 1>]

# @unique forbids aliases
try:
    @unique
    class Bad(Enum):
        X = 1
        Y = 1
except ValueError:
    print("ValueError")                     # ValueError

# auto(): let Python choose the values
class Dir(Enum):
    UP = auto()
    DOWN = auto()

print(Dir.UP.value, Dir.DOWN.value)         # 1 2


# IntEnum: members ARE integers
class Level(IntEnum):
    LOW = 1
    HIGH = 3

print(Level.LOW < Level.HIGH, Level.HIGH == 3, Level.HIGH + 1)      # True True 4


# IntFlag: bit flags (register bits!)
class Status(IntFlag):
    READY = 1
    ERROR = 2
    BUSY = 4

s = Status.READY | Status.BUSY
print(int(s), Status.BUSY in s, bool(s & Status.ERROR))             # 5 True False


# Enums can have methods
class Op(Enum):
    ADD = "+"
    SUB = "-"

    def apply(self, a, b):
        return a + b if self is Op.ADD else a - b

print(Op.ADD.apply(2, 3), Op("-").apply(5, 2))      # 5 3


# Enums with several values per member
class Pin(Enum):
    LED = (13, "output")
    BTN = (2, "input")

    def __init__(self, number, mode):
        self.number = number
        self.mode = mode

print(Pin.LED.number, Pin.BTN.mode, Pin.LED.name)   # 13 input LED


# Enums in match-case (dotted names compare, as you saw in Module 03)
class State(Enum):
    IDLE = auto()
    RUNNING = auto()

def describe(state):
    match state:
        case State.IDLE:
            return "idle"
        case State.RUNNING:
            return "running"

print(describe(State.IDLE), describe(State.RUNNING))    # idle running


# StrEnum (Python 3.11+): members ARE strings
class Mode(StrEnum):
    READ = "r"
    WRITE = "w"

print(Mode.READ == "r", f"{Mode.READ}", Mode("w").name)     # True r WRITE
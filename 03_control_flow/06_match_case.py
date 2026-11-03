# match-case compares a value against patterns (Python 3.10+)

command = "start"
match command:
    case "start":
        print("Starting")           # Starting
    case "stop":
        print("Stopping")
    case _:                         # _ is the default (like "default:" in C)
        print("Unknown command")

# OR patterns with |
action = "exit"
match action:
    case "quit" | "exit" | "q":
        print("Leaving")            # Leaving
    case _:
        print("Staying")

# Numbers
code = 404
match code:
    case 200:
        print("OK")
    case 301 | 302:
        print("Redirect")
    case 404:
        print("Not Found")          # Not Found
    case 500:
        print("Server Error")
    case _:
        print("Other")

# Guards: add "if" to a case
n = 15
match n:
    case 0:
        print("zero")
    case x if x < 0:
        print("negative")
    case x if x % 2 == 0:
        print("positive even")
    case _:
        print("positive odd")       # positive odd

# Sequence patterns: match shape AND capture values
point = (0, 5)
match point:
    case (0, 0):
        print("origin")
    case (0, y):
        print(f"on y-axis at {y}")  # on y-axis at 5
    case (x, 0):
        print(f"on x-axis at {x}")
    case (x, y):
        print(f"point at {x}, {y}")

# Star pattern captures the rest
cmd = ["go", "north", "fast"]
match cmd:
    case ["quit"]:
        print("quit")
    case ["go", direction]:
        print("go", direction)
    case ["go", direction, *extra]:
        print("go", direction, "with", extra)   # go north with ['fast']

# Dictionary patterns
event = {"type": "click", "x": 10, "y": 20}
match event:
    case {"type": "click", "x": x, "y": y}:
        print(f"click at {x},{y}")              # click at 10,20
    case {"type": "key", "key": k}:
        print("key", k)

# RULES
# - There is NO fall-through and NO break needed (unlike C switch).
# - A bare name like "case RED:" is a CAPTURE (it matches anything and assigns it).
#   To compare with a constant, use a literal or a dotted name (Enums, Module 13).
# - Class patterns exist too; they come after classes (Module 12).
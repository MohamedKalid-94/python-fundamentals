import functools
import inspect
import types
from typing import (Annotated, Any, Callable, ClassVar, Final, Literal, NewType, NotRequired,
                    Optional, Self, TypedDict, TypeGuard, Union, assert_never, cast, get_args,
                    get_origin, get_type_hints)

# Type hints describe the expected types. Python IGNORES them while running.
# They are read by editors (Pylance), checkers (mypy, Pyright), and by libraries at run time
# (FastAPI, Pydantic, dataclasses).

# 1. Where hints are stored
def f(a: int, b: str = "x") -> bool:
    return True

print(f.__annotations__)                        # {'a': <class 'int'>, 'b': <class 'str'>, 'return': <class 'bool'>}
print(f("not an int"))                          # True       nothing is checked at run time

class C:
    a: int
    b: str = "x"

print(C.__annotations__)                        # {'a': <class 'int'>, 'b': <class 'str'>}

# 2. Optional, Union and the | syntax (3.10+)
print(Optional[int] == Union[int, None], (int | None) == Optional[int], get_args(int | str))
# True True (<class 'int'>, <class 'str'>)

# 3. Literal: only these exact values
Mode = Literal["r", "w"]
print(get_args(Mode))                           # ('r', 'w')

# 4. Final (a constant) and ClassVar (belongs to the class, not the objects)
MAX_SPEED: Final = 100

class K:
    count: ClassVar[int] = 0

print(K.__annotations__)                        # {'count': typing.ClassVar[int]}

# 5. TypedDict: a dictionary with known keys
class Movie(TypedDict):
    name: str
    year: NotRequired[int]

movie: Movie = {"name": "Alien"}
print(movie, sorted(Movie.__required_keys__), sorted(Movie.__optional_keys__))
# {'name': 'Alien'} ['name'] ['year']

# 6. Callable, aliases, NewType, Annotated
def apply(func: Callable[[int], str], value: int) -> str:
    return func(value)

print(apply(str, 5))                            # 5

Vector = list[float]                            # an alias

def scale(v: Vector, k: float) -> Vector:
    return [x * k for x in v]

print(scale([1.0, 2.0], 2))                     # [2.0, 4.0]

UserId = NewType("UserId", int)
print(UserId(5) + 1, type(UserId(5)).__name__)  # 6 int       at run time it is a plain int

print(get_args(Annotated[int, "meters"]))       # (<class 'int'>, 'meters')   extra data for libraries

# 7. Self: methods that return the same class (method chaining)
class Builder:
    def __init__(self) -> None:
        self.items: list[int] = []

    def add(self, x: int) -> Self:
        self.items.append(x)
        return self

print(Builder().add(1).add(2).items)            # [1, 2]

# 8. TypeGuard, cast, Any
def is_str_list(values: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(v, str) for v in values)

print(is_str_list(["a", "b"]), is_str_list([1]))        # True False
print(cast(int, "x"))                           # x        cast changes nothing at run time

# 9. Exhaustive checks with assert_never
def describe(x: int | str) -> str:
    if isinstance(x, int):
        return "int"
    if isinstance(x, str):
        return "str"
    assert_never(x)                             # a checker complains if a case is missing

print(describe(1), describe("a"))               # int str
try:
    describe(1.5)
except AssertionError:
    print("AssertionError")                     # AssertionError

# 10. get_type_hints resolves string ("forward") references
class Node:
    value: int
    next: "Node | None"

hints = get_type_hints(Node)
print(hints["value"], hints["next"] == (Node | None))   # <class 'int'> True

# 11. USING HINTS AT RUN TIME: a small validator (the idea behind FastAPI and Pydantic)
def type_name(tp):
    return str(tp) if get_origin(tp) or not isinstance(tp, type) else tp.__name__

def check(value, expected):
    if expected is Any:
        return True
    origin = get_origin(expected)
    if origin is None:
        return isinstance(value, expected)
    args = get_args(expected)
    if origin in (Union, types.UnionType):
        return any(check(value, a) for a in args)
    if origin is list:
        return isinstance(value, list) and all(check(v, args[0]) for v in value)
    if origin is dict:
        return isinstance(value, dict) and all(
            check(k, args[0]) and check(v, args[1]) for k, v in value.items())
    return isinstance(value, origin)

def validate(func):
    hints = get_type_hints(func)
    sig = inspect.signature(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        for name, value in bound.arguments.items():
            expected = hints.get(name)
            if expected is not None and not check(value, expected):
                raise TypeError(f"{name}: expected {type_name(expected)}, got {type(value).__name__}")
        return func(*args, **kwargs)
    return wrapper

@validate
def add_all(numbers: list[int], scale: float = 1.0, label: str | None = None) -> float:
    return sum(numbers) * scale

print(add_all([1, 2, 3]))                       # 6.0
for bad in ({"numbers": [1, "2"]}, {"numbers": [1], "scale": 2}, {"numbers": [1], "label": 5}):
    try:
        add_all(**bad)
    except TypeError as e:
        print(e)
# numbers: expected list[int], got list
# scale: expected float, got int
# label: expected str | None, got int
# (a type CHECKER accepts an int where a float is expected; isinstance does not)

# USING A TYPE CHECKER (from the terminal)
#   pip install mypy          then       mypy your_file.py        or   mypy --strict src/
#   Pylance (VS Code) and Pyright show the same errors as you type.
#   Example of what it reports:
#       x: int = "hello"      error: Incompatible types in assignment (expression has type "str", variable has type "int")
#   Silence one line:  # type: ignore[assignment]      Ask the checker:  reveal_type(x)
#   Types may be added step by step ("gradual typing"): start with function signatures.
#   A "py.typed" file in a package tells checkers that its hints can be trusted.
# TIP: put annotations on public functions; let the checker infer local variables.
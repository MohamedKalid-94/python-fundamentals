from typing import (Any, Callable, Generic, Iterable, Protocol, TypeVar,
                    get_args, get_origin)

# GENERICS: write a function or class ONCE and keep the TYPE information for every use.
# Python does not enforce them while running. Editors and checkers (mypy, Pyright) use them,
# and so do libraries such as FastAPI and Pydantic.

T = TypeVar("T")                                # "some type, the same everywhere in this signature"
K = TypeVar("K")
V = TypeVar("V")

# 1. A generic function: the result has the same type as the list items
def first(items: list[T]) -> T:
    return items[0]

print(first([1, 2, 3]), first(["a", "b"]))      # 1 a
# A checker knows first([1, 2, 3]) is an int and first(["a"]) is a str.


# 2. A generic class
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def __len__(self) -> int:
        return len(self._items)


s: Stack[int] = Stack()
s.push(1)
s.push(2)
print(s.pop(), len(s))                          # 2 1

names = Stack[str]()                            # you can also write the type at creation
names.push("a")
print(names.pop())                              # a

# Type hints are NOT checked at run time. A checker would flag the next line, Python does not:
s.push("oops")
print(len(s))                                   # 2


# 3. Several type variables
class Pair(Generic[K, V]):
    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value

    def swap(self) -> "Pair[V, K]":
        return Pair(self.value, self.key)


print(Pair("a", 1).swap().key)                  # 1

# 4. A type variable limited to some types ...
Number = TypeVar("Number", int, float)

def add(a: Number, b: Number) -> Number:
    return a + b

print(add(1, 2), add(1.5, 2.5))                 # 3 4.0


# ... or to anything that supports a certain operation (a Protocol, explained in Module 13)
class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool: ...

C = TypeVar("C", bound=Comparable)

def biggest(items: list[C]) -> C:
    return max(items)

print(biggest([3, 9, 2]), biggest(["b", "a"]))  # 9 b

# 5. Functions as parameters
def apply(func: Callable[[T], V], value: T) -> V:
    return func(value)

print(apply(len, "abc"), apply(str.upper, "a"))     # 3 A

# 6. Accept any iterable, return a list of the same item type
def to_list(items: Iterable[T]) -> list[T]:
    return list(items)

print(to_list(range(3)))                        # [0, 1, 2]

# 7. A generic container with a typed lookup
class Repo(Generic[T]):
    def __init__(self) -> None:
        self._data: dict[int, T] = {}

    def add(self, ident: int, item: T) -> None:
        self._data[ident] = item

    def get(self, ident: int) -> T | None:
        return self._data.get(ident)


repo: Repo[str] = Repo()
repo.add(1, "x")
print(repo.get(1), repo.get(2))                 # x None

# 8. The built-in containers are generic too
#    list[int]   dict[str, int]   tuple[int, str]   tuple[int, ...]   set[str]
#    int | None   (Optional[int])      int | str   (Union[int, str])
print(get_origin(list[int]).__name__, [a.__name__ for a in get_args(list[int])])
# list ['int']
print([a.__name__ for a in get_args(dict[str, int])], [a.__name__ for a in get_args(Stack[int])])
# ['str', 'int'] ['int']

# WHY GENERICS
#  - one Stack class instead of IntStack, StrStack, ...
#  - the editor knows what pop() returns, so autocomplete and error messages are exact
#  - a checker finds the mistake (a str pushed on a Stack[int]) before the program runs
#
# Run the checker yourself (Module 20):   pip install mypy    then   mypy 04_generics.py
#
# IN C you would use  void *  (no type safety) or macros; C++ uses templates.
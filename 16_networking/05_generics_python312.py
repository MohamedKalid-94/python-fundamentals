# Python 3.12+: no TypeVar and no Generic[...] needed.

# 1. A generic class: the type variable goes in [ ] after the name
class Box[T]:
    def __init__(self, item: T) -> None:
        self.item = item

    def get(self) -> T:
        return self.item


print(Box(5).get())                             # 5

# 2. A generic function
def last[T](items: list[T]) -> T:
    return items[-1]


print(last(["a", "b"]))                         # b

# 3. Limit the type variable to some types (constraints) ...
def add[N: (int, float)](a: N, b: N) -> N:
    return a + b


print(add(1, 2), add(1.5, 2.5))                 # 3 4.0


# ... or to a class and its subclasses (a bound)
class Square:
    def __init__(self, s: int) -> None:
        self.s = s

    def area(self) -> int:
        return self.s ** 2


def biggest[S: Square](items: list[S]) -> S:
    return max(items, key=lambda item: item.area())


print(biggest([Square(2), Square(3)]).s)        # 3

# 4. A named type alias with the "type" statement
type Pairs[K, V] = list[tuple[K, V]]

p: Pairs[str, int] = [("a", 1)]
print(p)                                        # [('a', 1)]
print(Pairs.__name__)                           # Pairs

# 5. The type parameters are stored on the class
print(Box.__type_params__[0].__name__)          # T
import inspect
import statistics
from functools import cmp_to_key, partial, partialmethod, reduce
from itertools import accumulate
from operator import attrgetter, itemgetter, methodcaller

# A HIGHER-ORDER FUNCTION takes a function as an argument, or returns a function (or both).
# Functions are ordinary objects: you can store them, pass them and return them.

# 1. Pass a function
def apply(func, value):
    return func(value)

print(apply(len, "abc"), apply(str.upper, "a"), apply(lambda x: x * 2, 4))      # 3 A 8

# 2. Return a function
def make_adder(n):
    return lambda x: x + n

add5 = make_adder(5)
print(add5(10))                                 # 15

# 3. Compose functions: build a new function out of smaller ones
def compose(*funcs):                            # compose(f, g)(x) is f(g(x))
    def composed(x):
        for f in reversed(funcs):
            x = f(x)
        return x
    return composed

def pipe(value, *funcs):                        # pipe(x, f, g) is g(f(x)), reads left to right
    return reduce(lambda acc, f: f(acc), funcs, value)

inc = lambda x: x + 1
double = lambda x: x * 2
print(compose(inc, double)(5), compose(double, inc)(5), pipe(5, double, inc))   # 11 12 11

# 4. map, filter, reduce
print(list(map(lambda a, b: a + b, [1, 2, 3], [10, 20, 30])))   # [11, 22, 33]    map with TWO lists
print(list(filter(None, [0, 1, "", "a", None, [], [0]])))       # [1, 'a', [0]]   None keeps the truthy items
print(reduce(lambda a, b: a + b, [1, 2, 3, 4], 100))            # 110     100 is the starting value
print(reduce(lambda a, b: {**a, **b}, [{"a": 1}, {"b": 2}, {"a": 3}]))      # {'a': 3, 'b': 2}
print(reduce(lambda a, b: a if a > b else b, [3, 9, 2]))        # 9
print(list(accumulate([1, 2, 3, 4], lambda a, b: a * b)))       # [1, 2, 6, 24]  reduce, keeping every step

# 5. partial: fix some arguments of a function
int_from_binary = partial(int, base=2)
print(int_from_binary("1010"), partial(pow, 2)(10))             # 10 1024

def log(level, message):
    return f"[{level}] {message}"

warn = partial(log, "WARN")
print(warn("disk"))                             # [WARN] disk
print(warn.func is log, warn.args, warn.keywords)               # True ('WARN',) {}

class Switch:
    def _set(self, state):
        self.state = state

    on = partialmethod(_set, True)              # partial for METHODS
    off = partialmethod(_set, False)

s = Switch()
s.on()
print(s.state)                                  # True
s.off()
print(s.state)                                  # False

# 6. Sorting with an old-style two-argument comparison
def compare(a, b):
    a, b = a.lower(), b.lower()
    return (a > b) - (a < b)

print(sorted(["b", "A", "c"], key=cmp_to_key(compare)))         # ['A', 'b', 'c']

# 7. Currying: turn f(a, b, c) into f(a)(b)(c)
def curry(func):
    needed = func.__code__.co_argcount

    def curried(*args):
        if len(args) >= needed:
            return func(*args)
        return lambda *more: curried(*args, *more)

    return curried

@curry
def volume(length, width, height):
    return length * width * height

print(volume(2)(3)(4), volume(2, 3)(4), volume(2)(3, 4))        # 24 24 24

# 8. The strategy pattern: a dictionary of functions
strategies = {"sum": sum, "max": max, "mean": statistics.mean}
print({name: func([1, 2, 3, 4]) for name, func in strategies.items()})
# {'sum': 10, 'max': 4, 'mean': 2.5}

# 9. Callbacks
def process(items, on_item=None, on_done=None):
    for item in items:
        if on_item:
            on_item(item)
    if on_done:
        on_done(len(items))

events = []
process([10, 20], on_item=lambda i: events.append(f"item {i}"), on_done=lambda n: events.append(f"done {n}"))
print(events)                                   # ['item 10', 'item 20', 'done 2']

# 10. Objects that behave like functions, and delayed calls
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):
        return x * self.factor

print(list(map(Multiplier(3), [1, 2])), callable(Multiplier(3)))  # [3, 6] True

def lazy(func, *args):                          # a "thunk": nothing runs until you call it
    return lambda: func(*args)

delayed = lazy(sum, [1, 2, 3])
print(delayed())                                # 6

# 11. Functions can have attributes
def counter():
    counter.calls += 1

counter.calls = 0
counter()
counter()
print(counter.calls)                            # 2

# 12. The operator module has ready-made function versions of operators and lookups
people = [("Ann", 30), ("Bob", 25)]
print(sorted(people, key=itemgetter(1)))        # [('Bob', 25), ('Ann', 30)]
print(list(map(methodcaller("upper"), ["a", "b"])), attrgetter("real")(3))      # ['A', 'B'] 3

# 13. Look at a function from outside
sig = inspect.signature(log)
print(sig, list(sig.parameters))                # (level, message) ['level', 'message']

# map/filter  or  comprehension?
#   list(map(str, xs))              a comprehension [str(x) for x in xs] is usually just as clear
#   list(map(func, xs)) with a ready-made function is neat
#   reduce                          use sum, max, min, any, all, "".join when they fit; reduce otherwise
# Python's own higher-order tools: sorted(key=), max(key=), min(key=), map, filter, functools.*,
# itertools.starmap, decorators (Module 17), callbacks (threading.Timer, signal, atexit).
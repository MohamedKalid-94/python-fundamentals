Write the questions as # comments and your solutions as code below each one.

Abstract base classes

Write a class Ring(Sequence) (a fixed-size circular buffer that supports len, indexing and slicing). Show which methods you did NOT have to write (index, count, in, reversed, iteration).
Write CaseInsensitiveSet(MutableSet) (the abstract methods are __contains__, __iter__, __len__, add, discard) and test the operators |, &, -, <= that come for free.
Write a Driver ABC with abstract open, read, write and close, a concrete FakeDriver, and a function transfer(driver, data) that uses it. Show the TypeError when a driver forgets one method. Add a __subclasshook__-based Readable ABC and check it against 3 unrelated classes.
Show with code that register() makes issubclass true but gives no methods, and that the registered class is not in the MRO.

Custom exceptions

Design an exception family for a serial-protocol library: ProtocolError, FrameError (with CrcError and LengthError), TimeoutError_, with a code, retryable, context, to_dict() and JSON output. Write a parser that raises them and a handler that decides what to do.
Make one of your exceptions work with pickle (and copy.deepcopy), and send it through a ProcessPoolExecutor to show it arrives intact. Then break it by changing super().__init__ and see what happens.
Write a decorator @translate_errors({KeyError: NotFoundError, ValueError: ValidationError}) that converts errors and chains them with from. Print the full traceback with traceback.format_exception to show the chain.

Higher-order functions

Write compose, pipe, curry and flip(func) (swaps the first two arguments), then build a text cleaner from five small functions (strip, lower, remove punctuation, collapse spaces, title-case).
Write your own map, filter and reduce using only loops, and a group_by(items, key) that returns a dictionary of lists. Compare your versions with the built-ins.
Write memoize(func) that works with several arguments, a size limit and a cache_clear() method, then compare it with functools.lru_cache.
Write once(func) (runs only the first time), debounce_calls(n) (runs every n-th call) and with_timeout_default(func, default) (returns the default if the function raises).

Object internals and memory

Write a class that logs every attribute read and write using __getattribute__ and __setattr__ (avoid the infinite recursion), then a version that makes attributes read-only after __init__.
Print everything you can learn about a function: name, signature, defaults, number of arguments, whether it has *args or **kwargs, its constants and its bytecode (dis.dis). Change its defaults at run time.
Show an object being freed at the moment its last reference goes (with __del__), then a cycle that stays alive with gc.disable(), then freed by gc.collect(). Break the cycle with weakref and show that the collector is no longer needed.
Measure with tracemalloc and sys.getsizeof the memory of 100,000 points stored as: a list of dictionaries, a list of plain objects, a list of __slots__ objects, a list of tuples, a list of namedtuples, and an array("d"). Print a table sorted by size.

Metaclasses and metaprogramming

Write a metaclass Frozen that makes the CLASS attributes read-only after the class is created (hint: __setattr__ on the metaclass), and another one that refuses classes whose method names are not in snake_case.
Write a metaclass-based “abstract” check: a class must define every name listed in required = (...), otherwise a TypeError is raised when the class is defined. Compare it with ABC.
Extend the Model example of file 07 with: a max_length option for str fields, a required=True option, a from_dict class method, and to_json(). Test inheritance and error messages.
Write a class decorator @add_slots_repr that reads __slots__ and creates __repr__, __eq__ and __hash__, and compare it with @dataclass(slots=True, frozen=True).
Build a tiny command-line framework: a decorator @command("name") registers functions, run("add 2 3") parses the text and calls the function with arguments converted using the function’s type annotations.
Write make_record(name, fields) that builds a class with __slots__, __init__, __repr__ and __eq__ using exec on generated source (validate the names), and compare it with collections.namedtuple.
Predict first, then run, and explain each result in a comment:
python
import gc, sys, weakref
from abc import ABC, abstractmethod

class Meta(type):
    def __new__(m, name, bases, ns):
        ns["tag"] = name.upper()
        return super().__new__(m, name, bases, ns)

class A(metaclass=Meta): pass
class B(A): pass
print(A.tag, B.tag, type(B).__name__)

class Shape(ABC):
    @abstractmethod
    def area(self): ...

try:
    Shape()
except TypeError:
    print("abstract")
print(Shape.area(None))

class Node:
    def __init__(self): self.me = self
gc.disable()
n = Node()
r = weakref.ref(n)
del n
print(r() is not None, gc.collect() >= 1, r())
gc.enable()

class V:
    def __eq__(self, o): return True
print(V() == 1, V() != 1, hash(V.__eq__) is not None)
try:
    {V()}
except TypeError:
    print("unhashable")

def f(a, b=[]):
    b.append(a)
    return b
print(f(1), f(2), f.__defaults__)
print(sys.getrefcount(f) >= 2)
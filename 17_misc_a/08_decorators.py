import functools
import time

# A DECORATOR is a function that takes a function and returns a (usually wrapped) function.
#
#   @shout                   is the same as          greet = shout(greet)
#   def greet(): ...

# 1. The standard pattern
def shout(func):
    @functools.wraps(func)                      # copies the name and docstring of the original
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper

@shout
def greet(name):
    """Say hello."""
    return f"hello {name}"

print(greet("ann"))                             # HELLO ANN
print(greet.__name__, greet.__doc__)            # greet Say hello.
print(greet.__wrapped__("x"))                   # hello x       the original function

# Without functools.wraps the metadata is lost
def careless(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@careless
def work():
    pass

print(work.__name__)                            # wrapper

# 2. Logging calls
calls = []

def logged(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        calls.append(f"{func.__name__}{args}")
        return func(*args, **kwargs)
    return wrapper

@logged
def add(a, b):
    return a + b

print(add(2, 3), calls)                         # 5 ['add(2, 3)']

# 3. Timing, keeping the result in an attribute of the wrapper
def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            wrapper.last = time.perf_counter() - start
    wrapper.last = 0.0
    return wrapper

@timed
def slow():
    time.sleep(0.02)
    return "done"

print(slow(), slow.last > 0.01)                 # done True

# 4. A decorator WITH arguments: one more level (a decorator factory)
def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(times)]
        return wrapper
    return decorator

@repeat(3)
def hi():
    return "hi"

print(hi())                                     # ['hi', 'hi', 'hi']

# 5. Stacking: the one nearest to the function is applied first
def tag(name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            return f"<{name}>{func()}</{name}>"
        return wrapper
    return decorator

@tag("b")
@tag("i")
def text():
    return "hi"

print(text())                                   # <b><i>hi</i></b>

# 6. Retry on errors
attempts = 0

def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except ConnectionError as e:
                    last = e
            raise last
        return wrapper
    return decorator

@retry(3)
def flaky():
    global attempts
    attempts += 1
    if attempts < 3:
        raise ConnectionError("no link")
    return "ok"

print(flaky(), attempts)                        # ok 3

# 7. Validating arguments
def in_range(low, high):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(value):
            if not low <= value <= high:
                raise ValueError(f"{value} not in {low}..{high}")
            return func(value)
        return wrapper
    return decorator

@in_range(0, 100)
def set_volume(v):
    return v

print(set_volume(50))                           # 50
try:
    set_volume(150)
except ValueError as e:
    print(e)                                    # 150 not in 0..100

# 8. Caching with the standard library
@functools.lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(30), fib.cache_info())                # 832040 CacheInfo(hits=28, misses=31, maxsize=None, currsize=31)

@functools.cache                                # the same without a size limit (Python 3.9+)
def fib2(n):
    return n if n < 2 else fib2(n - 1) + fib2(n - 2)

print(fib2(50))                                 # 12586269025

# 9. A CLASS decorator
def add_repr(cls):
    cls.__repr__ = lambda self: f"{type(self).__name__}({self.__dict__})"
    return cls

@add_repr
class P:
    def __init__(self, x):
        self.x = x

print(P(1))                                     # P({'x': 1})

# 10. A decorator written as a class (it keeps state in attributes)
class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

@CountCalls
def hello():
    return "hi"

hello()
hello()
print(hello.count)                              # 2

# 11. A registry: the decorator stores the function and returns it unchanged
commands = {}

def command(name):
    def register(func):
        commands[name] = func
        return func
    return register

@command("start")
def start():
    return "starting"

@command("stop")
def stop():
    return "stopping"

print(commands["start"](), sorted(commands))    # starting ['start', 'stop']

# DECORATORS YOU ALREADY KNOW
#   @property  @staticmethod  @classmethod  @dataclass  @abstractmethod  @functools.cached_property
#   @contextlib.contextmanager  @functools.singledispatch  @functools.lru_cache
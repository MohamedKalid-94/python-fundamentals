import gc
import tracemalloc
import warnings
import weakref
from collections import deque
from functools import lru_cache

# A "memory leak" in Python means: objects you no longer NEED are still REACHABLE, so they are never freed.
# (Python frees unreachable objects by itself, so the usual cause is a forgotten reference.)

# 1. An unbounded cache or global list
cache = {}
tracemalloc.start()
before, _ = tracemalloc.get_traced_memory()
for i in range(1000):
    cache[i] = bytes(1000)                      # one entry per request, never removed
after, _ = tracemalloc.get_traced_memory()
print(after - before > 900_000)                 # True      about 1 MB kept for ever
tracemalloc.stop()

@lru_cache(maxsize=10)                          # FIX: a cache with a limit
def make(i):
    return bytes(1000)

for i in range(100):
    make(i)
print(make.cache_info().currsize)               # 10

history = deque(maxlen=3)                       # a log that keeps only the last 3 items
for i in range(5):
    history.append(i)
print(list(history))                            # [2, 3, 4]

# 2. lru_cache on a METHOD keeps every "self" alive (self is part of the cache key)
class Leaky:
    @lru_cache(maxsize=None)
    def compute(self, x):
        return x * 2

leaky = Leaky()
leaky.compute(1)
leaky_ref = weakref.ref(leaky)
del leaky
gc.collect()
print(leaky_ref() is not None)                  # True      LEAK: the class-level cache still holds it
Leaky.compute.cache_clear()

class Fixed:
    def __init__(self):
        self._compute = lru_cache(maxsize=None)(self._compute_impl)     # one cache per object

    def compute(self, x):
        return self._compute(x)

    def _compute_impl(self, x):
        return x * 2

fixed = Fixed()
fixed.compute(1)
fixed_ref = weakref.ref(fixed)
del fixed
gc.collect()
print(fixed_ref() is None)                      # True      the object and its cache can be freed together

# 3. Listeners that are never removed: a bound method holds its object alive
class Bus:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, callback):
        self.subscribers.append(callback)

class Widget:
    def on_event(self):
        pass

bus = Bus()
widget = Widget()
bus.subscribe(widget.on_event)
widget_ref = weakref.ref(widget)
del widget
gc.collect()
print(widget_ref() is not None)                 # True      LEAK: the bus still holds the bound method

class WeakBus:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, callback):
        self.subscribers.append(weakref.WeakMethod(callback))       # a weak reference to the method

    def alive(self):
        return sum(1 for s in self.subscribers if s() is not None)

weak_bus = WeakBus()
widget2 = Widget()
weak_bus.subscribe(widget2.on_event)
widget2_ref = weakref.ref(widget2)
del widget2
gc.collect()
print(widget2_ref() is None, weak_bus.alive())  # True 0

# 4. A stored exception keeps the whole call stack (all its local variables) alive
class Big:
    pass

refs = []

def work():
    obj = Big()
    refs.append(weakref.ref(obj))
    raise ValueError("x")

saved = []
try:
    work()
except ValueError as e:
    saved.append(e)                             # e.__traceback__ -> frame -> obj
gc.collect()
print(refs[0]() is not None)                    # True      still alive through the traceback
saved.clear()
gc.collect()
print(refs[0]() is None)                        # True

# 5. FIND leaks: compare two snapshots of the allocations
tracemalloc.start()
first = tracemalloc.take_snapshot()
leaked = [bytes(1000) for _ in range(200)]
second = tracemalloc.take_snapshot()
top = second.compare_to(first, "lineno")[0]
print(top.size_diff > 150_000)                  # True
tracemalloc.stop()

# ... or count how many objects of a class exist
class Suspect:
    pass

def count(type_name):
    return sum(1 for o in gc.get_objects() if type(o).__name__ == type_name)

start = count("Suspect")
kept = [Suspect() for _ in range(10)]
print(count("Suspect") - start)                 # 10

# 6. Resources that are not closed (files, sockets): Python warns when they are destroyed
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    f = open(__file__, encoding="utf-8")
    del f                                       # destroyed without close()
    gc.collect()
print([w.category.__name__ for w in caught])    # ['ResourceWarning']
# Run with  python -X dev  to see these warnings. Always use "with open(...)".

# CHECKLIST: WHAT CAN KEEP OBJECTS ALIVE?
#   a module-level list or dict that only grows          a cache without a size limit
#   lru_cache / cache on methods                          listeners and callbacks that are never removed
#   closures and bound methods stored somewhere           exceptions (and their tracebacks) stored in a variable
#   threads, timers and tasks that are still running      objects that reference each other with __del__ in old code
#   C extensions that forget to release memory            logging handlers, atexit callbacks, global registries
# TOOLS: tracemalloc (standard), gc.get_objects(), objgraph (draws who refers to whom),
#   memray and pympler (profilers), psutil (the process memory, "RSS"), and in production
#   a worker that restarts after N requests (gunicorn max_requests) as a safety net.
# NOTE: Python can hold on to memory after you free objects (pymalloc arenas), so a process size that
#   does not shrink is not always a leak: a leak is a size that keeps GROWING under a steady workload.
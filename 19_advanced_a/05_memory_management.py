import gc
import sys
import tracemalloc
import weakref
from array import array

# CPython manages memory with TWO systems:
#   1. REFERENCE COUNTING: every object counts how many names/containers point at it.
#      When the count reaches 0 the object is freed at once.
#   2. A CYCLIC GARBAGE COLLECTOR (gc): finds groups of objects that point at each other
#      (so their counts never reach 0) but that nobody else can reach.

# 1. Reference counts
x = object()
print(sys.getrefcount(x))                       # 2     x itself, plus the argument of getrefcount()
y = x
print(sys.getrefcount(x))                       # 3
holder = [x]
print(sys.getrefcount(x))                       # 4
del y
print(sys.getrefcount(x))                       # 3
del holder
print(sys.getrefcount(x))                       # 2

# "del name" removes a NAME, never the object (unless it was the last reference)
a = [1]
b = a
del a
print(b)                                        # [1]

# 2. In CPython an object is destroyed the moment its last reference goes
events = []

class Tracker:
    def __init__(self, name):
        self.name = name

    def __del__(self):
        events.append(f"freed {self.name}")

t = Tracker("a")
t = None                                        # the only reference is gone
t = Tracker("b")
t = Tracker("c")                                # "c" is built first, then "b" loses its last reference
del t

def make():
    local = Tracker("local")                    # a local variable dies when the function returns

make()
print(events)                                   # ['freed a', 'freed b', 'freed c', 'freed local']
# (PyPy and other implementations may free later: never rely on the exact moment. Use "with".)

# 3. A reference CYCLE: the counts never reach zero
class Node:
    pass

gc.disable()                                    # stop automatic collections so we can watch
n1, n2 = Node(), Node()
n1.other, n2.other = n2, n1
probe = weakref.ref(n1)
del n1, n2
print(probe() is not None)                      # True      still alive: each one is held by the other
collected = gc.collect()                        # the collector finds the unreachable group
print(probe(), collected >= 2)                  # None True
gc.enable()

# 4. The collector and its settings
print(gc.isenabled(), len(gc.get_threshold()), len(gc.get_count()))             # True 3 3
print(isinstance(gc.collect(), int), gc.get_referents(["a"]))                   # True ['a']
#   gc.disable() / gc.enable()   switch the automatic collector     gc.freeze()   exclude objects
#   gc.get_objects()             every tracked container            gc.get_referrers(obj)   who holds obj
# The collector works in 3 GENERATIONS: young objects are checked often, old ones rarely.

# 5. Lists grow in STEPS (over-allocation), so appending is fast on average
numbers = []
sizes = []
for i in range(100):
    numbers.append(i)
    sizes.append(sys.getsizeof(numbers))
print(len(set(sizes)) < 30, sizes[-1] > sys.getsizeof([]))      # True True

# 6. How big is an object? sys.getsizeof is SHALLOW: it does not count what the object points to
def deep_size(obj, seen=None):
    seen = set() if seen is None else seen
    if id(obj) in seen:                         # count shared objects only once
        return 0
    seen.add(id(obj))
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(deep_size(k, seen) + deep_size(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(deep_size(item, seen) for item in obj)
    return size

nested = {"a": [1, 2, 3], "b": ("x", "y")}
print(deep_size(nested) > sys.getsizeof(nested))                # True
shared = [1, 2, 3]
print(deep_size([shared, shared]) == sys.getsizeof([shared, shared]) + deep_size(shared))   # True

# 7. Compact data types
print(sys.getsizeof(array("i", range(1000))) < sys.getsizeof(list(range(1000))))            # True
# Also: tuples are smaller than lists, __slots__ removes the per-object dictionary,
# generators do not store their items, memoryview does not copy.

# 8. Small integers are shared (a cache), big ones are not
print(int("5") is int("5"), int("100000") is int("100000"))     # True False
print(isinstance(sys.getallocatedblocks(), int))                # True       memory blocks in use

# 9. Find WHERE memory is allocated
tracemalloc.start()
data = [bytes(1000) for _ in range(100)]        # about 100 KB
snapshot = tracemalloc.take_snapshot()
tracemalloc.stop()
top = snapshot.statistics("lineno")[0]
print(top.size > 90_000)                        # True

# 10. How the memory is organised
#   - Small objects (up to 512 bytes) come from "pymalloc": big blocks (arenas) cut into pools.
#     That is quick, but free memory inside an arena is returned to the OS only when the WHOLE
#     arena is empty. So a program can keep a large resident size after you delete many objects.
#   - Large objects use the C library's malloc.
#   - Python has no "free" and no pointer arithmetic: references are safe, but cycles, caches and
#     global lists can still make memory grow (Module 20, Memory Leaks).
#
# MICROPYTHON (microcontrollers)
#   A simple mark-and-sweep collector and a fixed heap: import gc; gc.collect(); gc.mem_free();
#   gc.mem_alloc(). Preallocate buffers (bytearray) and reuse them to avoid fragmentation.
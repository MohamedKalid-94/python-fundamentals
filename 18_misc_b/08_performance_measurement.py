import cProfile
import io
import pstats
import sys
import time
import timeit
import tracemalloc
from collections import deque

# RULE 1: measure first, then optimise. RULE 2: a better ALGORITHM beats clever tricks.

# 1. A stopwatch: time.perf_counter() (wall clock) and time.process_time() (CPU time only)
t0, c0 = time.perf_counter(), time.process_time()
time.sleep(0.1)
print(time.perf_counter() - t0 >= 0.09)         # True    sleeping takes wall time ...
print(time.process_time() - c0 < 0.05)          # True    ... but almost no CPU time

# A reusable timer
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *exc):
        self.elapsed = time.perf_counter() - self.start
        return False

with Timer() as timer:
    time.sleep(0.02)
print(timer.elapsed >= 0.015)                   # True

# 2. timeit: repeat a small piece of code many times and total the time
total = timeit.timeit("sum(range(100))", number=1000)
print(total > 0)                                # True
runs = timeit.repeat("sum(range(100))", repeat=3, number=100)
print(len(runs) == 3, min(runs) > 0)            # True True     use the MINIMUM of several runs

# 3. Compare two ways of doing the same thing
data_list = list(range(100_000))
data_set = set(data_list)
slow = timeit.timeit(lambda: 99_999 in data_list, number=200)       # scans the whole list
fast = timeit.timeit(lambda: 99_999 in data_set, number=200)        # one hash lookup
print(fast < slow)                              # True

def list_insert():
    items = []
    for i in range(20_000):
        items.insert(0, i)                      # shifts every item: O(n) each time

def deque_appendleft():
    items = deque()
    for i in range(20_000):
        items.appendleft(i)                     # O(1) each time

print(timeit.timeit(deque_appendleft, number=1) < timeit.timeit(list_insert, number=1))    # True

# 4. cProfile: which FUNCTIONS take the time?
def work():
    return sum(i * i for i in range(10_000))

profiler = cProfile.Profile()
profiler.enable()
work()
profiler.disable()
stream = io.StringIO()
pstats.Stats(profiler, stream=stream).sort_stats("cumulative").print_stats(5)
report = stream.getvalue()
print("function calls" in report, "work" in report)     # True True
# From the terminal:  python -m cProfile -s cumulative myscript.py

# 5. tracemalloc: how much MEMORY does a piece of code use?
tracemalloc.start()
numbers = [str(i) for i in range(10_000)]
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(current > 100_000, peak >= current)       # True True

# 6. sys.getsizeof: the size of ONE object (not of what it points to)
print(sys.getsizeof("a" * 1000) > 1000, sys.getsizeof((1, 2, 3)) < sys.getsizeof([1, 2, 3]))  # True True

# COMMON WINS
#   x in a_set / a_dict instead of x in a_list      (O(1) instead of O(n))
#   "".join(parts) instead of += in a long loop
#   generators for big data, deque for queues, local variables in hot loops
#   built-ins and the standard library (they are written in C)
#   NumPy for numeric work, multiprocessing for CPU-bound work, lru_cache for repeated calls
# TOOLS   line_profiler (line by line), memory_profiler, py-spy (a profiler that attaches to a
#         running program), python -X importtime (slow imports)
# BIG-O   O(1) constant, O(log n) binary search, O(n) one pass, O(n log n) sort, O(n^2) nested loops
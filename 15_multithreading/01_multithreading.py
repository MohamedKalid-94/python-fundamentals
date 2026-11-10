import sys
import threading
import time

# A THREAD is a path of execution inside a program. All the threads of one process
# SHARE the same memory, so they can work on the same data (and can also corrupt it).
#
#                  process                          thread
#   memory         its own                          shared with the other threads
#   start cost     high                             low
#   crash          does not harm other processes    can bring the whole process down
#   talk to others pipes, sockets, queues           ordinary variables (with locks!)
#   use for        CPU-heavy work, isolation        waiting: network, files, serial ports

# 1. Every program starts with one thread
print(threading.current_thread().name)          # MainThread
print(threading.active_count())                 # 1

# 2. Threads share memory
shared = []

def add(item):
    shared.append(item)

t = threading.Thread(target=add, args=("from thread",))
t.start()
t.join()
print(shared)                                   # ['from thread']

# 3. Threads pay off when the program WAITS (I/O-bound work)
def fetch(_):
    time.sleep(0.2)                             # pretend to wait for a network answer

start = time.perf_counter()
for i in range(4):
    fetch(i)
sequential = time.perf_counter() - start
print(sequential >= 0.8)                        # True    4 waits of 0.2 s, one after the other

start = time.perf_counter()
threads = [threading.Thread(target=fetch, args=(i,)) for i in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
threaded = time.perf_counter() - start
print(threaded < 0.6)                           # True    the 4 waits overlap
print(threaded < sequential)                    # True

# 4. THE GIL (Global Interpreter Lock)
# In standard CPython only ONE thread runs Python bytecode at any moment.
# - While a thread WAITS (sleep, network, file, serial port), another one can run: threads help.
# - For CPU-heavy pure-Python work, threads do NOT run in parallel:
#   use multiprocessing, or libraries that release the GIL (NumPy, many C extensions).
# - Python 3.13 has an optional "free-threaded" build without the GIL.
print(getattr(sys, "_is_gil_enabled", lambda: True)())      # True     (on a standard build)

# 5. Counting threads
gate = threading.Event()
t = threading.Thread(target=gate.wait)
t.start()
print(threading.active_count())                 # 2
gate.set()
t.join()
print(threading.active_count())                 # 1

# WHEN TO USE WHAT
#   threading            waiting work: network, files, serial/USB devices, GUIs
#   multiprocessing      CPU-bound work in pure Python
#   asyncio              thousands of waiting tasks in ONE thread (Module 20, Coroutines)
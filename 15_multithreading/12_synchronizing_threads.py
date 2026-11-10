import threading
import time

# THE PROBLEM: threads share data, and "counter = counter + 1" is three steps:
# read the value, add 1, write it back. Another thread can run between the steps.
# That is a RACE CONDITION. The lock below makes it safe.

counter = 0

def unsafe_increment():
    global counter
    value = counter                             # read
    time.sleep(0.001)                           # another thread gets in here
    counter = value + 1                         # write (it may overwrite the others' work)

threads = [threading.Thread(target=unsafe_increment) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter < 10)                             # True    updates were LOST (it should be 10)

# 1. LOCK: only one thread at a time inside the "with" block
counter = 0
lock = threading.Lock()

def safe_increment():
    global counter
    with lock:
        value = counter
        time.sleep(0.001)
        counter = value + 1

threads = [threading.Thread(target=safe_increment) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter)                                  # 10

# 2. The Lock methods
lock = threading.Lock()
lock.acquire()
print(lock.locked())                            # True
print(lock.acquire(blocking=False))             # False   did not wait
print(lock.acquire(timeout=0.05))               # False   waited 50 ms, then gave up
lock.release()
print(lock.locked())                            # False

try:
    lock.release()
except RuntimeError as e:
    print(e)                                    # release unlocked lock

# 3. RLock: the SAME thread may acquire it several times (a Lock would block itself)
rlock = threading.RLock()
rlock.acquire()
rlock.acquire()
rlock.release()
rlock.release()
print("rlock ok")                               # rlock ok

# 4. Semaphore: at most N threads inside at once (a pool of N resources)
sem = threading.Semaphore(2)
guard = threading.Lock()
active = 0
peak = 0

def job():
    global active, peak
    with sem:
        with guard:
            active += 1
            peak = max(peak, active)
        time.sleep(0.05)
        with guard:
            active -= 1

threads = [threading.Thread(target=job) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(peak <= 2)                                # True    (peak is 2 in practice)

bounded = threading.BoundedSemaphore(1)
bounded.acquire()
bounded.release()
try:
    bounded.release()                           # more releases than acquires
except ValueError as e:
    print(type(e).__name__)                     # ValueError

# 5. Barrier: everyone waits until all N threads have arrived
barrier = threading.Barrier(3)
log = []

def meet():
    log.append("before")
    barrier.wait()
    log.append("after")

threads = [threading.Thread(target=meet) for _ in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(log[:3] == ["before"] * 3, log[3:] == ["after"] * 3)      # True True

# 6. A class that protects its own data
class SafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1

    @property
    def value(self):
        with self._lock:
            return self._value

sc = SafeCounter()

def many():
    for _ in range(1000):
        sc.increment()

threads = [threading.Thread(target=many) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(sc.value)                                 # 5000

# 7. Thread-local data: every thread sees its OWN copy
local = threading.local()
local.x = "main"

def set_local():
    local.x = "worker"

t = threading.Thread(target=set_local)
t.start()
t.join()
print(local.x)                                  # main

# RULES
#  - Lock around every read-modify-write of shared data (use "with", never forget release()).
#  - Keep locked sections short, and never wait on I/O while holding a lock.
#  - Single operations like list.append() are atomic in CPython, but "x += 1" and
#    "if key not in d: d[key] = ..." are NOT.
#  - Best of all: do not share. Pass data through a Queue (next file).
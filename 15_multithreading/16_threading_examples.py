import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor


# 1. Parallel "downloads" with a pool: the waits overlap
def fetch(url):
    time.sleep(0.1)                             # pretend to download
    return f"page:{url}"

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=4) as pool:
    pages = list(pool.map(fetch, ["a", "b", "c", "d"]))
print(pages)                                    # ['page:a', 'page:b', 'page:c', 'page:d']
print(time.perf_counter() - start < 0.3)        # True


# 2. A thread-safe counter used by many threads
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

counter = SafeCounter()

def bump():
    for _ in range(1000):
        counter.increment()

threads = [threading.Thread(target=bump) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter.value)                            # 5000


# 3. A two-stage pipeline: numbers -> squares -> total
numbers, squares = queue.Queue(), queue.Queue()
total = []

def generate():
    for n in range(1, 6):
        numbers.put(n)
    numbers.put(None)

def square_stage():
    while (n := numbers.get()) is not None:
        squares.put(n * n)
    squares.put(None)

def sum_stage():
    s = 0
    while (n := squares.get()) is not None:
        s += n
    total.append(s)

stages = [threading.Thread(target=f) for f in (generate, square_stage, sum_stage)]
for t in stages:
    t.start()
for t in stages:
    t.join()
print(total[0])                                 # 55       1 + 4 + 9 + 16 + 25


# 4. A periodic task that stops cleanly
stop = threading.Event()
runs = []

def periodic():
    while not stop.wait(0.02):                  # wait() returns True when stop is set
        runs.append(time.perf_counter())

t = threading.Thread(target=periodic)
t.start()
time.sleep(0.15)
stop.set()
t.join()
print(len(runs) >= 3)                           # True


# 5. A simulated serial port: a reader thread and a parser thread
frames = [b"\xAA\x01", b"\xAA\x02", b"\xAA\x03"]
raw = queue.Queue()
checksums = []

def reader():
    for frame in frames:
        time.sleep(0.01)                        # time between frames on the wire
        raw.put(frame)
    raw.put(None)

def parser():
    while (frame := raw.get()) is not None:
        checksums.append(sum(frame) & 0xFF)

tr = threading.Thread(target=reader, name="uart-rx")
tp = threading.Thread(target=parser, name="parser")
tr.start()
tp.start()
tr.join()
tp.join()
print(checksums)                                # [171, 172, 173]


# 6. Compute a value only ONCE, even when many threads ask for it
cache = {}
cache_lock = threading.Lock()
calls = []

def get(key):
    with cache_lock:
        if key not in cache:
            calls.append(key)                   # the "expensive" computation
            cache[key] = 42
        return cache[key]

values = []
threads = [threading.Thread(target=lambda: values.append(get("k"))) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(len(calls), set(values))                  # 1 {42}


# 7. A worker pool built by hand: 3 workers, 10 jobs
jobs, out = queue.Queue(), queue.Queue()

def pool_worker():
    while (job := jobs.get()) is not None:
        out.put(job * 2)

workers = [threading.Thread(target=pool_worker) for _ in range(3)]
for w in workers:
    w.start()
for i in range(10):
    jobs.put(i)
for _ in workers:
    jobs.put(None)
for w in workers:
    w.join()
print(sorted(out.get() for _ in range(10)))     # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]


# 8. A timeout around a slow function (the thread cannot be killed, so it is a daemon)
def run_with_timeout(func, seconds):
    box = []
    t = threading.Thread(target=lambda: box.append(func()), daemon=True)
    t.start()
    t.join(seconds)
    if t.is_alive():
        raise TimeoutError(f"took longer than {seconds}s")
    return box[0]

print(run_with_timeout(lambda: 5, 1))           # 5
try:
    run_with_timeout(lambda: time.sleep(0.3), 0.05)
except TimeoutError as e:
    print(e)                                    # took longer than 0.05s


# 9. Moving money in both directions without a deadlock (locks taken in a fixed order)
class Account:
    def __init__(self, ident, balance):
        self.ident = ident
        self.balance = balance
        self.lock = threading.Lock()

def transfer(src, dst, amount):
    first, second = sorted((src, dst), key=lambda a: a.ident)
    with first.lock, second.lock:
        src.balance -= amount
        dst.balance += amount

a, b = Account(1, 100), Account(2, 100)

def a_to_b():
    for _ in range(100):
        transfer(a, b, 1)

def b_to_a():
    for _ in range(100):
        transfer(b, a, 1)

t1, t2 = threading.Thread(target=a_to_b), threading.Thread(target=b_to_a)
t1.start()
t2.start()
t1.join()
t2.join()
print(a.balance, b.balance, a.balance + b.balance)      # 100 100 200
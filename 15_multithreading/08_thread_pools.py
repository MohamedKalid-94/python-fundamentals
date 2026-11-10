import concurrent.futures
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# A THREAD POOL keeps a fixed number of worker threads and gives them tasks.
# It is cheaper than one thread per task, limits the load, and returns results and errors.

def square(n):
    time.sleep(0.01)
    return n * n

# 1. map(): results come back in the ORDER of the inputs
with ThreadPoolExecutor(max_workers=4) as pool:
    print(list(pool.map(square, range(6))))     # [0, 1, 4, 9, 16, 25]

# 2. submit() returns a Future: a promise of a result
    futures = [pool.submit(square, n) for n in (3, 4)]
    print([f.result() for f in futures])        # [9, 16]
# leaving the "with" block waits for every task (shutdown(wait=True))

# 3. as_completed(): in the order the tasks FINISH
def job(name, delay):
    time.sleep(delay)
    return name

with ThreadPoolExecutor(max_workers=2) as pool:
    futures = [pool.submit(job, "slow", 0.3), pool.submit(job, "fast", 0.1)]
    print([f.result() for f in as_completed(futures)])          # ['fast', 'slow']

# 4. Errors travel back to the caller
def boom():
    raise ValueError("bad")

with ThreadPoolExecutor(max_workers=1) as pool:
    f = pool.submit(boom)
    try:
        f.result()
    except ValueError as e:
        print("caught", e)                      # caught bad
    print(type(f.exception()).__name__, f.done())               # ValueError True

# 5. A callback runs when the Future completes
done = []
with ThreadPoolExecutor(max_workers=1) as pool:
    pool.submit(square, 3).add_done_callback(lambda fut: done.append(fut.result()))
print(done)                                     # [9]

# 6. cancel(): only tasks that have NOT started can be cancelled
pool = ThreadPoolExecutor(max_workers=1)
busy = pool.submit(time.sleep, 0.2)             # the only worker is busy
queued = pool.submit(square, 2)                 # this one waits in line
print(queued.cancel(), queued.cancelled())      # True True
pool.shutdown()

# 7. A timeout while waiting for a result
with ThreadPoolExecutor(max_workers=1) as pool:
    f = pool.submit(time.sleep, 0.3)
    try:
        f.result(timeout=0.05)
    except concurrent.futures.TimeoutError:
        print("timeout")                        # timeout

# 8. A pool REUSES its threads
names = []

def record(_):
    names.append(threading.current_thread().name)
    time.sleep(0.01)

with ThreadPoolExecutor(max_workers=3, thread_name_prefix="pool") as pool:
    list(pool.map(record, range(10)))
print(len(set(names)) <= 3, all(n.startswith("pool_") for n in names))      # True True

# CHOOSING
#   ThreadPoolExecutor    waiting work: downloads, file I/O, serial devices
#   ProcessPoolExecutor   the same API, for CPU-bound work (separate processes)
#   default size          min(32, cpu_count + 4)
# Python 3.9+: pool.shutdown(cancel_futures=True) cancels everything still queued.
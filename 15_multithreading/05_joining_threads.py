import threading
import time

# join() makes the CALLING thread wait until the other thread has finished.

# 1. join with a timeout: it gives up waiting, the thread keeps running
slow = threading.Thread(target=time.sleep, args=(0.3,))
slow.start()
slow.join(timeout=0.05)
print(slow.is_alive())                          # True    the wait timed out
slow.join()                                     # now wait for real
print(slow.is_alive())                          # False
# join() always returns None: check is_alive() to see whether it worked

# 2. Errors
try:
    threading.current_thread().join()
except RuntimeError as e:
    print(e)                                    # cannot join current thread

try:
    threading.Thread(target=print).join()
except RuntimeError as e:
    print(e)                                    # cannot join thread before it is started

# 3. Join BEFORE you use the results
parts = [0] * 4
ranges = [(1, 26), (26, 51), (51, 76), (76, 101)]

def partial_sum(index, start, stop):
    parts[index] = sum(range(start, stop))

threads = [
    threading.Thread(target=partial_sum, args=(i, a, b))
    for i, (a, b) in enumerate(ranges)
]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(parts, sum(parts))                        # [325, 950, 1575, 2200] 5050

# 4. START ALL, then JOIN ALL. Do not start-join-start-join: that runs one after the other.
def work():
    time.sleep(0.1)

start = time.perf_counter()
for _ in range(3):
    t = threading.Thread(target=work)
    t.start()
    t.join()                                    # waits here, so there is no overlap
print(time.perf_counter() - start >= 0.3)       # True    3 x 0.1 s

start = time.perf_counter()
threads = [threading.Thread(target=work) for _ in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(time.perf_counter() - start < 0.25)       # True    the three waits overlap

# 5. A program waits at the end for every non-daemon thread anyway,
#    but join() is how YOUR code waits for a result at the right moment.
# 6. A pool does the same with:  with ThreadPoolExecutor() as pool: ...  (it joins on exit)
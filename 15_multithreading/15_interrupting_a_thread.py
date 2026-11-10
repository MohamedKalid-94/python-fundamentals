import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor

# Python has NO way to kill or interrupt a thread from outside:
print(hasattr(threading.Thread, "kill"), hasattr(threading.Thread, "interrupt"))   # False False
# (Forcing a stop could leave locks held and data half-written.)
# The correct way is COOPERATIVE: ask the thread to stop, and let it finish cleanly.

# 1. A stop Event that the thread checks
stop = threading.Event()
ticks = []

def worker():
    n = 0
    while not stop.is_set():
        n += 1
        stop.wait(0.01)                         # a sleep that ends as soon as stop is set
    ticks.append(n)

t = threading.Thread(target=worker)
t.start()
time.sleep(0.1)
stop.set()
t.join()
print(ticks[0] > 0, t.is_alive())               # True False

# 2. Event.wait() is an INTERRUPTIBLE sleep (time.sleep() is not)
stop = threading.Event()
t = threading.Thread(target=lambda: stop.wait(5))
t.start()
begin = time.perf_counter()
stop.set()
t.join()
print(time.perf_counter() - begin < 1)          # True    it did not wait the 5 seconds

# 3. Blocking calls with a TIMEOUT, so the thread can look at the flag between waits
stop = threading.Event()
q = queue.Queue()
got = []

def reader():
    while not stop.is_set():
        try:
            item = q.get(timeout=0.02)
        except queue.Empty:
            continue
        got.append(item)

t = threading.Thread(target=reader)
t.start()
for n in (1, 2, 3):
    q.put(n)
time.sleep(0.1)
stop.set()
t.join()
print(got)                                      # [1, 2, 3]

# 4. A reusable StoppableThread
class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class Counter(StoppableThread):
    def run(self):
        self.count = 0
        while not self.stopped():
            self.count += 1
            self._stop_event.wait(0.01)


c = Counter()
c.start()
time.sleep(0.1)
c.stop()
c.join()
print(c.count > 0, c.stopped())                 # True True

# 5. Keep the MAIN thread responsive to Ctrl+C while it waits
def wait_for(thread):
    try:
        while thread.is_alive():
            thread.join(timeout=0.01)           # short waits: Ctrl+C is handled between them
    except KeyboardInterrupt:
        print("interrupted: asking the worker to stop")
        raise

short = threading.Thread(target=time.sleep, args=(0.05,))
short.start()
wait_for(short)
print("finished")                               # finished

# 6. A pool can cancel the tasks that have not started
started = threading.Event()

def task():
    started.set()
    time.sleep(0.1)

pool = ThreadPoolExecutor(max_workers=1)
futures = [pool.submit(task) for _ in range(4)]
started.wait()                                  # the first task is running now
pool.shutdown(cancel_futures=True)              # waits for it, cancels the three still queued
print([f.cancelled() for f in futures])         # [False, True, True, True]

# OTHER OPTIONS
#   - Work that MUST be killable: run it in a separate PROCESS (multiprocessing.Process.terminate()).
#   - Network code: set timeouts (socket.settimeout) so blocking calls come back.
#   - Do NOT use ctypes tricks such as PyThreadState_SetAsyncExc: they can corrupt state.
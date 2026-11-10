import queue
import threading

# How threads TALK to each other: Event (a signal), Condition (wait for a state),
# Queue (pass data).

# 1. Queue: the safe way to pass data (producer -> consumer)
q = queue.Queue()
results = []

def producer():
    for i in range(5):
        q.put(i)
    q.put(None)                                 # a sentinel: "no more data"

def consumer():
    while True:
        item = q.get()
        if item is None:
            break
        results.append(item * 10)

p = threading.Thread(target=producer)
c = threading.Thread(target=consumer)
p.start()
c.start()
p.join()
c.join()
print(results)                                  # [0, 10, 20, 30, 40]

# 2. Several consumers: one sentinel for each
q = queue.Queue()
results = []

def consumer2():
    while True:
        item = q.get()
        if item is None:
            break
        results.append(item * 2)

consumers = [threading.Thread(target=consumer2) for _ in range(3)]
for t in consumers:
    t.start()
for n in range(1, 6):
    q.put(n)
for _ in consumers:
    q.put(None)
for t in consumers:
    t.join()
print(sorted(results))                          # [2, 4, 6, 8, 10]

# 3. task_done() and join(): wait until every item has been PROCESSED
q = queue.Queue()
results = []

def worker():
    while True:
        item = q.get()
        results.append(item + 100)
        q.task_done()

threading.Thread(target=worker, daemon=True).start()
for n in (1, 2, 3):
    q.put(n)
q.join()                                        # returns when task_done() was called 3 times
print(sorted(results))                          # [101, 102, 103]

# 4. A bounded queue gives BACK-PRESSURE
bq = queue.Queue(maxsize=2)
bq.put_nowait(1)
bq.put_nowait(2)
try:
    bq.put_nowait(3)
except queue.Full:
    print("full")                               # full
try:
    queue.Queue().get_nowait()
except queue.Empty:
    print("empty")                              # empty
try:
    bq.put(3, timeout=0.05)
except queue.Full:
    print("put timed out")                      # put timed out

# 5. Other queues
lifo = queue.LifoQueue()
for n in (1, 2, 3):
    lifo.put(n)
print([lifo.get() for _ in range(3)])           # [3, 2, 1]
pq = queue.PriorityQueue()
pq.put((2, "b"))
pq.put((1, "a"))
print(pq.get())                                 # (1, 'a')

# 6. Event: a flag that threads can wait for
ready = threading.Event()
print(ready.wait(0.05))                         # False   timed out
ready.set()
print(ready.wait(0.05), ready.is_set())         # True True
ready.clear()
print(ready.is_set())                           # False

# 7. Condition: wait until something is TRUE
cond = threading.Condition()
items = []
log = []

def waiting_consumer():
    with cond:
        cond.wait_for(lambda: len(items) >= 3)      # releases the lock while waiting
        log.append(f"got {len(items)}")

def slow_producer():
    for i in range(3):
        with cond:
            items.append(i)
            cond.notify()                       # wake a waiting thread so it re-checks

tc = threading.Thread(target=waiting_consumer)
tp = threading.Thread(target=slow_producer)
tc.start()
tp.start()
tc.join()
tp.join()
print(log)                                      # ['got 3']

# 8. Two-way talk: a request queue and a response queue
requests, responses = queue.Queue(), queue.Queue()

def squarer():
    while True:
        n = requests.get()
        if n is None:
            break
        responses.put(n * n)

t = threading.Thread(target=squarer)
t.start()
for n in (1, 2, 3):
    requests.put(n)
requests.put(None)
t.join()
print([responses.get() for _ in range(3)])      # [1, 4, 9]

# WHICH TOOL?
#   Queue       pass DATA between threads (first choice)
#   Event       a one-bit signal: "start", "stop", "ready"
#   Condition   wait until shared data reaches some STATE
#   Lock        protect shared data that is changed in place
#   Barrier     make a group of threads meet at one point
# RTOS names: Queue = message queue, Event = event flag, Lock = mutex, Semaphore = semaphore.
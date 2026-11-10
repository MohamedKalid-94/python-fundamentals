import sys
import threading
import time

# SCHEDULING decides which thread gets the CPU, and when.
# Python threads are real OS threads, so the operating system's scheduler decides.
# Inside CPython the GIL is passed from thread to thread every few milliseconds
# (the "switch interval"), or sooner when a thread waits.

# 1. The switch interval
print(sys.getswitchinterval())                  # 0.005       (5 ms)
sys.setswitchinterval(0.001)
print(sys.getswitchinterval())                  # 0.001
sys.setswitchinterval(0.005)                    # put it back

# 2. You cannot predict the order in which threads run.
#    Whatever the order, the RESULTS must be right: each thread here has its own counter.
counts = {}

def count_up(name):
    n = 0
    for _ in range(200_000):
        n += 1
    counts[name] = n

threads = [threading.Thread(target=count_up, args=(k,)) for k in ("a", "b")]
for t in threads:
    t.start()
for t in threads:
    t.join()
print([counts["a"], counts["b"]])               # [200000, 200000]

# 3. If you NEED an order, create it with synchronisation: a ping-pong with two Events
ping_turn = threading.Event()
pong_turn = threading.Event()
out = []

def ping():
    for _ in range(3):
        ping_turn.wait()
        ping_turn.clear()
        out.append("ping")
        pong_turn.set()

def pong():
    for _ in range(3):
        pong_turn.wait()
        pong_turn.clear()
        out.append("pong")
        ping_turn.set()

t1 = threading.Thread(target=ping)
t2 = threading.Thread(target=pong)
t1.start()
t2.start()
ping_turn.set()                                 # ping goes first
t1.join()
t2.join()
print(out)                                      # ['ping', 'pong', 'ping', 'pong', 'ping', 'pong']

# 4. Sleeping to "order" threads is only a hint, never a guarantee.
#    With big gaps it works in practice, but it is NOT safe on a busy machine:
result = []

def delayed(value):
    time.sleep(value * 0.1)
    result.append(value)

threads = [threading.Thread(target=delayed, args=(v,)) for v in (3, 1, 2)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(result)                                   # [1, 2, 3]      (usually!)

# 5. time.sleep(0) offers the CPU to another thread
def polite():
    for _ in range(3):
        time.sleep(0)                           # a "yield"

# 6. Threads are PREEMPTIVE: the scheduler can pause a thread between any two bytecodes.
#    asyncio tasks are COOPERATIVE: they switch only at "await" (Module 20).
#
# WHAT YOU CAN AND CANNOT CONTROL
#   can      how many threads, when they wait, which locks/events/queues they use
#   cannot   the order of execution, the time slice, a "run this one first" rule
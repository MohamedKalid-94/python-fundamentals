import queue
import threading

# Python threads have NO PRIORITY. There is no setPriority() like in Java.
# The operating system schedules them, and Python gives you no knob for it.
print(hasattr(threading.Thread, "priority"), hasattr(threading.Thread, "setPriority"))
# False False

# WHAT YOU CAN DO INSTEAD

# 1. Prioritise the WORK, not the thread: a PriorityQueue hands out the lowest number first
tasks = queue.PriorityQueue()
for priority, name in [(3, "low"), (1, "urgent"), (2, "normal")]:
    tasks.put((priority, name))
tasks.put((99, "stop"))                         # a sentinel that sorts last

done = []

def worker():
    while True:
        priority, name = tasks.get()
        if name == "stop":
            break
        done.append(name)

t = threading.Thread(target=worker)
t.start()
t.join()
print(done)                                     # ['urgent', 'normal', 'low']

# 2. Items with the same priority are compared by the NEXT tuple element.
#    Add a counter to keep first-in first-out order and avoid comparing objects:
import itertools
counter = itertools.count()
q = queue.PriorityQueue()
for priority, name in [(1, "b"), (1, "a"), (1, "c")]:
    q.put((priority, next(counter), name))
print([q.get()[2] for _ in range(3)])           # ['b', 'a', 'c']      (the order they arrived)

# 3. Separate workers (or pools) for urgent and normal work
#    urgent_pool = ThreadPoolExecutor(2) ; normal_pool = ThreadPoolExecutor(8)

# 4. Operating-system priorities (platform specific, usually needs special rights):
#      Linux/macOS   os.nice(10) lowers the priority of the whole PROCESS
#                    os.sched_setscheduler(...) real-time policies (Linux, root)
#      Windows       ctypes calls to SetThreadPriority, or the psutil package
#    These apply to a process (or to one OS thread you identify yourself),
#    and they are not portable.

# 5. For hard real-time deadlines, Python is the wrong tool: do that part in C or on an
#    RTOS, and let Python talk to it (serial, sockets, shared memory).

# PRIORITY INVERSION (a classic RTOS problem)
#    A low-priority task holds a lock that a high-priority task needs.
#    Python does not have it, because it has no priorities, but a slow thread
#    holding a lock still makes every other thread wait: keep locked sections SHORT.
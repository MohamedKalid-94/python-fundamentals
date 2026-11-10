import threading

# start() creates the new thread, and the new thread then calls run().
# Calling run() yourself does NOT create a thread: it is an ordinary function call.

names = []

def show():
    names.append(threading.current_thread().name)

t1 = threading.Thread(target=show, name="T1")
t1.run()                                        # runs in the CURRENT thread
print(names)                                    # ['MainThread']

t2 = threading.Thread(target=show, name="T2")
t2.start()                                      # runs in a NEW thread
t2.join()
print(names)                                    # ['MainThread', 'T2']

# A thread can be started only once
try:
    t2.start()
except RuntimeError as e:
    print(e)                                    # threads can only be started once

# Starting order is NOT running order
results = []
threads = [threading.Thread(target=results.append, args=(i,)) for i in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(sorted(results))                          # [0, 1, 2, 3, 4]
# results itself may be in any order, so never rely on it.

# start() returns at once: the main thread keeps running while the new thread works.
# Here an Event forces the order so the output is the same every time:
go = threading.Event()
log = []

def worker():
    go.wait()                                   # wait for the signal
    log.append("worker")

t = threading.Thread(target=worker)
t.start()
log.append("main continues")                    # runs while the worker is still waiting
go.set()
t.join()
print(log)                                      # ['main continues', 'worker']

# Know when a thread is really running: let it signal you
ready = threading.Event()
threading.Thread(target=ready.set).start()
print(ready.wait(1))                            # True    wait() returns True when the event is set

# Fire and forget (no join): fine for work whose result you do not need,
# but the program will still wait for it at exit (it is not a daemon thread).
threading.Thread(target=lambda: None).start()

# NOTES
# - Every thread uses memory (a stack) and OS resources: do not start thousands.
#   Use a thread pool (file 08).
# - Data reaches a thread through args/kwargs or shared objects, never through the return value.
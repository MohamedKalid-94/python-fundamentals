import threading
import time

# THE LIFE OF A THREAD
#
#   NEW  --start()-->  RUNNABLE  <-->  RUNNING  --run() ends or raises-->  TERMINATED
#                                        |  ^
#                           sleep / wait / lock / I-O
#                                        v  |
#                                     BLOCKED (waiting)
#
# Python shows no state names. You observe a thread with is_alive() and ident.

# 1. NEW: created but not started
ev = threading.Event()
t = threading.Thread(target=ev.wait, name="worker")
print(t.is_alive(), t.ident)                    # False None

# 2. start(): the thread is alive (running, or blocked inside ev.wait())
t.start()
print(t.is_alive(), t.ident is not None)        # True True

# 3. TERMINATED: run() finished
ev.set()
t.join()
print(t.is_alive())                             # False

# 4. A thread can be started only ONCE
try:
    t.start()
except RuntimeError as e:
    print(e)                                    # threads can only be started once

# 5. Blocked on a timed wait, then finished
sleeper = threading.Thread(target=time.sleep, args=(0.2,))
sleeper.start()
print(sleeper.is_alive())                       # True
sleeper.join()
print(sleeper.is_alive())                       # False

# 6. A small helper that names the state
def state(thread):
    if thread.ident is None:
        return "new"
    return "alive" if thread.is_alive() else "terminated"

gate = threading.Event()
t3 = threading.Thread(target=gate.wait)
print(state(t3))                                # new
t3.start()
print(state(t3))                                # alive
gate.set()
t3.join()
print(state(t3))                                # terminated

# 7. An exception ends the thread, NOT the program.
#    threading.excepthook decides what happens to it (the default prints a traceback).
errors = []
original = threading.excepthook
threading.excepthook = lambda args: errors.append(args.exc_type.__name__)

boom = threading.Thread(target=lambda: 1 / 0)
boom.start()
boom.join()
threading.excepthook = original
print(errors, boom.is_alive())                  # ['ZeroDivisionError'] False

# SUMMARY OF THE STATES
#   NEW         Thread(...) created, start() not called: ident is None
#   RUNNABLE    start() called, waiting for the OS to give it CPU time
#   RUNNING     executing its run() method
#   BLOCKED     waiting: sleep(), join(), lock.acquire(), event.wait(), I/O
#   TERMINATED  run() returned or raised: is_alive() is False. It can never be restarted.
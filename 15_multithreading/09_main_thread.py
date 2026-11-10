import signal
import sys
import threading

# The MAIN THREAD is the one that runs your script.

# 1. Identify it
print(threading.current_thread().name)                          # MainThread
print(threading.current_thread() is threading.main_thread())    # True
print(threading.main_thread().ident == threading.get_ident())   # True

# 2. Other threads are not the main thread
info = []

def who():
    me = threading.current_thread()
    info.append((me.name, me is threading.main_thread()))

t = threading.Thread(target=who, name="worker")
t.start()
t.join()
print(info)                                     # [('worker', False)]

# 3. sys.exit() inside a thread ends only THAT thread
t = threading.Thread(target=sys.exit)
t.start()
t.join()
print("main still running")                     # main still running

# 4. An exception in a thread does not stop the main thread
errors = []
original = threading.excepthook
threading.excepthook = lambda args: errors.append(args.exc_type.__name__)

def fail():
    raise RuntimeError("worker failed")

t = threading.Thread(target=fail)
t.start()
t.join()
threading.excepthook = original
print(errors)                                   # ['RuntimeError']

# 5. Only the main thread can install signal handlers (and receives Ctrl+C)
problems = []

def try_signal():
    try:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
    except ValueError as e:
        problems.append(type(e).__name__)

t = threading.Thread(target=try_signal)
t.start()
t.join()
print(problems)                                 # ['ValueError']

# 6. Ctrl+C raises KeyboardInterrupt in the MAIN thread. A main thread stuck in a long
#    join() reacts to it only between waits, so wait in short steps:
#        while worker.is_alive():
#            worker.join(timeout=0.1)

# 7. At the end of the script the interpreter waits for every NON-daemon thread
#    (daemon threads are stopped abruptly, file 11).
# 8. The main thread is not a daemon thread:
print(threading.main_thread().daemon)           # False

# EMBEDDED ANALOGY
#   main thread          the main() loop / the "super loop"
#   worker threads       RTOS tasks
#   signal handlers      interrupt service routines (only one place may own them)
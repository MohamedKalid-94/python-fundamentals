import threading
import time

# A DAEMON thread is a background helper:
# when only daemon threads are left, the program exits and they are stopped abruptly.
# A normal (non-daemon) thread keeps the program alive until it finishes.

# 1. Set the flag when you create the thread (or before start())
def forever():
    while True:
        time.sleep(0.01)

d = threading.Thread(target=forever, daemon=True)
d.start()
print(d.daemon, threading.current_thread().daemon)      # True False

# 2. You cannot change it after the thread has started
try:
    d.daemon = False
except RuntimeError as e:
    print(e)                                    # cannot set daemon status of active thread

# 3. A new thread INHERITS the flag of the thread that creates it
flags = []

def spawn():
    child = threading.Thread(target=lambda: None)
    flags.append(child.daemon)

parent = threading.Thread(target=spawn, daemon=True)
parent.start()
parent.join()
print(flags)                                    # [True]

# 4. The graceful alternative: a normal thread plus a stop Event, and join()
stop = threading.Event()
beats = []

def heartbeat():
    while not stop.is_set():
        beats.append("beat")
        stop.wait(0.02)                         # waits, but wakes at once when stop is set

h = threading.Thread(target=heartbeat)
h.start()
time.sleep(0.1)
stop.set()
h.join()
print(len(beats) > 0, h.is_alive())             # True False

# WHEN TO USE A DAEMON THREAD
#   good     heartbeats, monitors, log flushers, caches refreshers: work that is fine to lose
#   bad      anything that must finish: writing a file, saving data, releasing hardware.
#            A daemon thread can be stopped in the MIDDLE of a write, with locks still held.
#   For work that needs a clean ending, use a normal thread, a stop Event, and join().
#
# ThreadPoolExecutor workers are NOT daemon threads: the program waits for them at exit.

# 5. This script ends even though the daemon thread loops forever
print("end of script")                          # end of script
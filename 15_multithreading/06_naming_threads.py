import io
import logging
import threading

# Names make logs and debugging readable.

# 1. The default name looks like "Thread-1 (function_name)"
t = threading.Thread(target=print)
print(t.name.startswith("Thread-"))             # True

# 2. Choose a name when you create the thread, or change it later
t = threading.Thread(target=print, name="sensor-reader")
print(t.name)                                   # sensor-reader
t.name = "renamed"
print(t.name)                                   # renamed
# (setName() and getName() are old and deprecated: use the name attribute)

# 3. A thread can read its own name
names = []

def whoami():
    names.append(threading.current_thread().name)

t = threading.Thread(target=whoami, name="reader")
t.start()
t.join()
print(names)                                    # ['reader']
print(threading.current_thread().name)          # MainThread

# 4. Names are not required to be unique
a = threading.Thread(target=print, name="w")
b = threading.Thread(target=print, name="w")
print(a.name == b.name)                         # True    (use ident to tell them apart)

# 5. ident and native_id are numbers
ev = threading.Event()
t = threading.Thread(target=ev.wait, name="a")
t2 = threading.Thread(target=ev.wait, name="b")
t.start()
t2.start()
print(isinstance(t.ident, int), isinstance(t.native_id, int))   # True True

# 6. List the live threads
print(sorted(x.name for x in threading.enumerate()))            # ['MainThread', 'a', 'b']
ev.set()
t.join()
t2.join()

# 7. Name the thread in a subclass
class Reader(threading.Thread):
    def __init__(self, port):
        super().__init__(name=f"reader-{port}")

print(Reader("COM3").name)                      # reader-COM3

# 8. Thread names in log messages: %(threadName)s
stream = io.StringIO()
log = logging.getLogger("t06")
log.setLevel(logging.INFO)
log.propagate = False
handler = logging.StreamHandler(stream)
handler.setFormatter(logging.Formatter("%(threadName)s:%(message)s"))
log.addHandler(handler)

t = threading.Thread(target=log.info, args=("started",), name="reader")
t.start()
t.join()
print(stream.getvalue().strip())                # reader:started

# TIP: name threads after their ROLE ("uart-rx", "logger", "heartbeat"), not after a number.
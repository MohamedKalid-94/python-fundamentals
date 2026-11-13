import signal
import subprocess
import sys
from contextlib import contextmanager

# A SIGNAL is a message from the operating system (or another process) to your program:
#   SIGINT   Ctrl+C                       SIGTERM   "please stop" (kill, Docker stop, systemd)
#   SIGHUP   terminal closed (Unix)       SIGALRM   a timer ran out (Unix only)
#   SIGUSR1  your own use (Unix)          SIGKILL   cannot be caught
# It is like an interrupt: the handler runs, the normal code resumes.
# Windows supports only a few (SIGINT, SIGTERM, SIGBREAK, SIGABRT ...).

# 1. By default Ctrl+C raises KeyboardInterrupt
print(signal.getsignal(signal.SIGINT) is signal.default_int_handler)    # True
print(signal.SIGINT.value, signal.SIGTERM.value)                        # 2 15

# A helper that installs a handler and ALWAYS puts the old one back
@contextmanager
def handler(sig, func):
    previous = signal.signal(sig, func)
    try:
        yield
    finally:
        signal.signal(sig, previous)

# 2. Your own handler. signal.raise_signal() sends a signal to ourselves (works on Windows too)
received = []

def record(signum, frame):
    received.append(signal.Signals(signum).name)

with handler(signal.SIGINT, record):
    signal.raise_signal(signal.SIGINT)
print(received)                                 # ['SIGINT']
print(signal.getsignal(signal.SIGINT) is signal.default_int_handler)    # True      restored

# 3. The default handler turns SIGINT into an exception
try:
    signal.raise_signal(signal.SIGINT)
except KeyboardInterrupt:
    print("KeyboardInterrupt")                  # KeyboardInterrupt

# 4. GRACEFUL SHUTDOWN: the handler only sets a flag, the main loop checks it
processed = []
stop = False

def request_stop(signum, frame):
    global stop
    stop = True

with handler(signal.SIGTERM, request_stop):
    for item in range(10):
        if item == 4:
            signal.raise_signal(signal.SIGTERM)     # in real life: somebody stops your service
        if stop:
            break                               # finish cleanly: close files, save state
        processed.append(item)
print(processed, stop)                          # [0, 1, 2, 3] True

# 5. A timeout with a timer signal (Unix only; there is no SIGALRM on Windows)
if hasattr(signal, "SIGALRM"):
    def on_alarm(signum, frame):
        raise TimeoutError("took too long")

    with handler(signal.SIGALRM, on_alarm):
        signal.setitimer(signal.ITIMER_REAL, 0.05)
        try:
            while True:                         # a loop that never ends
                pass
        except TimeoutError as e:
            print(e)                            # took too long
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
else:
    print("took too long")                      # (on Windows use threads or asyncio.timeout instead)

# 6. Ignore a signal
with handler(signal.SIGINT, signal.SIG_IGN):
    signal.raise_signal(signal.SIGINT)
    print("ignored")                            # ignored

# 7. Stop ANOTHER process
child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
child.terminate()                               # SIGTERM on Unix, TerminateProcess on Windows
child.wait(timeout=10)
print(child.poll() is not None)                 # True      the child has ended
# os.kill(pid, signal.SIGTERM) and child.send_signal(sig) send other signals (Unix)

# RULES
#  - A handler must be SHORT: set a flag, put an item in a queue, write one byte. Do the work in the main loop.
#  - Only the MAIN thread can install handlers and receives signals (Module 15).
#  - Blocking calls (sleep, recv, input) are interrupted by a signal and then resumed (PEP 475),
#    unless your handler raises an exception.
#  - asyncio has its own way:  loop.add_signal_handler(signal.SIGTERM, callback)  (Unix).
#  - Docker and systemd stop a service with SIGTERM, wait a few seconds, then send SIGKILL:
#    so handle SIGTERM and exit quickly.
#
# EMBEDDED ANALOGY
#   a signal handler is an interrupt service routine: keep it tiny, set a volatile flag,
#   and let the main loop do the real work.
# Module 15: Multithreading & Synchronization, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Multithreading | Thread | A path of execution inside a process; the threads of a process share its memory |
| 01 | Multithreading | vs process | Thread: cheap, shared memory, needs locks. Process: own memory, safer, needs pipes/queues |
| 01 | Multithreading | Use for | Waiting work (network, files, serial ports, GUIs) |
| 01 | Multithreading | GIL | Standard CPython runs one thread of Python code at a time; threads overlap WAITING, not pure-Python CPU work |
| 01 | Multithreading | CPU-bound | Use `multiprocessing` or `ProcessPoolExecutor` (or C-based libraries like NumPy) |
| 01 | Multithreading | Free-threaded | Python 3.13 has an optional build without the GIL |
| 02 | Life Cycle | States | New, Runnable, Running, Blocked (waiting), Terminated |
| 02 | Life Cycle | Observe | `t.is_alive()`, `t.ident` (`None` before `start()`) |
| 02 | Life Cycle | Restart | A thread can be started only once (`RuntimeError`) |
| 02 | Life Cycle | Exceptions | An exception ends only that thread; `threading.excepthook` handles it |
| 03 | Creating | Function | `Thread(target=f, args=(...), kwargs={...})` |
| 03 | Creating | `args` | Must be a tuple: `("Ann",)`, not `("Ann")` |
| 03 | Creating | Subclass | Override `run()`; keep results in attributes |
| 03 | Creating | Other | A callable object, `Timer(seconds, f)` (cancellable), a pool `submit()` |
| 03 | Creating | Results | A thread does not return a value: use attributes, a Queue, or a `Future` |
| 04 | Starting | `start()` | Creates the thread, which then calls `run()` |
| 04 | Starting | `run()` | Calling it directly runs in the CURRENT thread (no new thread) |
| 04 | Starting | Order | Start order is not run order; sort results or synchronise |
| 04 | Starting | Signal | Use an `Event` to know that a thread is ready |
| 05 | Joining | `join()` | The caller waits until the thread ends; always returns `None` |
| 05 | Joining | Timeout | `join(timeout)` may return with the thread still alive: check `is_alive()` |
| 05 | Joining | Pattern | Start ALL threads, then join ALL (start-join-start-join runs them one by one) |
| 05 | Joining | Errors | Joining yourself or an unstarted thread raises `RuntimeError` |
| 05 | Joining | Results | Join before you read what the threads wrote |
| 06 | Naming | Name | `Thread(name="uart-rx")` or `t.name = ...` (`getName()` is deprecated) |
| 06 | Naming | Default | `Thread-N (function)`; names need not be unique |
| 06 | Naming | Inspect | `current_thread().name`, `threading.enumerate()`, `t.ident`, `t.native_id` |
| 06 | Naming | Logging | `%(threadName)s` in the log format |
| 07 | Scheduling | Who decides | The OS (preemptive); CPython passes the GIL every `getswitchinterval()` (5 ms) or when a thread waits |
| 07 | Scheduling | Order | Not predictable: results must not depend on it |
| 07 | Scheduling | Create order | With Events (ping-pong), Barriers, Queues |
| 07 | Scheduling | `sleep()` | A hint, never a guarantee; `sleep(0)` yields |
| 07 | Scheduling | asyncio | Cooperative switching at `await` |
| 08 | Thread Pools | Pool | `ThreadPoolExecutor(max_workers=N)`: reused threads, limited load |
| 08 | Thread Pools | `map` | Results in input order |
| 08 | Thread Pools | `submit` | Returns a `Future`: `result()`, `exception()`, `done()`, `cancel()`, `add_done_callback()` |
| 08 | Thread Pools | `as_completed` | Results in the order tasks finish |
| 08 | Thread Pools | Errors | They re-raise from `future.result()` |
| 08 | Thread Pools | `with` | Waits for all tasks on exit; `shutdown(cancel_futures=True)` cancels queued ones |
| 08 | Thread Pools | Choose | Thread pool for waiting work, process pool for CPU work |
| 09 | Main Thread | Identify | `threading.main_thread()`; its name is `MainThread` |
| 09 | Main Thread | Exit | The program waits for non-daemon threads before it ends |
| 09 | Main Thread | `sys.exit()` | Inside another thread it ends only that thread |
| 09 | Main Thread | Signals | Only the main thread installs handlers and gets Ctrl+C |
| 09 | Main Thread | Ctrl+C | Wait in short `join(timeout)` steps to stay responsive |
| 10 | Priority | None | Python threads have no priority setting |
| 10 | Priority | Alternative | Prioritise WORK with `queue.PriorityQueue`; separate pools; OS tools like `os.nice` (process level, not portable) |
| 10 | Priority | Ties | Add a counter to keep first-in first-out order |
| 10 | Priority | Real time | Do hard real-time work in C or on an RTOS |
| 11 | Daemon | Meaning | Stopped abruptly when only daemon threads remain |
| 11 | Daemon | Set | `daemon=True` before `start()`; changing it later raises `RuntimeError` |
| 11 | Daemon | Inherit | A thread copies the daemon flag of its creator |
| 11 | Daemon | Use | Heartbeats and monitors; never for work that must finish cleanly |
| 11 | Daemon | Clean stop | A normal thread, a stop `Event`, and `join()` |
| 12 | Synchronizing | Race condition | `x = x + 1` is read, add, write: another thread can run in between |
| 12 | Synchronizing | `Lock` | `with lock:`; `acquire(blocking=False)`, `acquire(timeout=...)`, `locked()` |
| 12 | Synchronizing | `RLock` | The same thread may acquire it several times |
| 12 | Synchronizing | `Semaphore` | At most N threads at once; `BoundedSemaphore` forbids extra releases |
| 12 | Synchronizing | `Barrier` | N threads wait until all have arrived |
| 12 | Synchronizing | `threading.local()` | Per-thread data |
| 12 | Synchronizing | Rules | Short locked sections, no I/O under a lock, prefer not sharing |
| 12 | Synchronizing | Atomic | `list.append` is atomic in CPython; `x += 1` and check-then-set are not |
| 13 | Communication | `Queue` | Thread-safe data passing: `put`, `get`, `task_done`, `join`, `maxsize` |
| 13 | Communication | Sentinel | Put `None` (one per consumer) to say "no more data" |
| 13 | Communication | Errors | `queue.Full`, `queue.Empty`, `put(timeout=...)`, `get_nowait()` |
| 13 | Communication | Kinds | `Queue` (FIFO), `LifoQueue`, `PriorityQueue`, `SimpleQueue` |
| 13 | Communication | `Event` | `set`, `clear`, `is_set`, `wait(timeout)` returns `True` or `False` |
| 13 | Communication | `Condition` | `with cond: cond.wait_for(predicate)` and `cond.notify()` |
| 13 | Communication | Choose | Queue for data, Event for signals, Condition for states |
| 14 | Deadlock | Meaning | Threads wait for each other forever |
| 14 | Deadlock | Four conditions | Mutual exclusion, hold and wait, no preemption, circular wait |
| 14 | Deadlock | Fix | Take locks in one fixed order, hold one lock at a time, use timeouts, or use a Queue |
| 14 | Deadlock | Self-deadlock | A `Lock` blocks its own thread when acquired twice; use `RLock` |
| 14 | Deadlock | Related | Livelock (busy but no progress), starvation (never gets the lock) |
| 14 | Deadlock | Debug | `faulthandler.dump_traceback_later(...)`, `py-spy dump` |
| 15 | Interrupting | No kill | Python offers no safe way to stop a thread from outside |
| 15 | Interrupting | Cooperative | A stop `Event` checked by the thread |
| 15 | Interrupting | Interruptible sleep | `stop.wait(seconds)` instead of `time.sleep(seconds)` |
| 15 | Interrupting | Blocking calls | Use timeouts: `q.get(timeout=...)`, `socket.settimeout(...)` |
| 15 | Interrupting | Pools | `shutdown(cancel_futures=True)`; running tasks cannot be cancelled |
| 15 | Interrupting | Killable work | Use a separate process and `terminate()` |
| 16 | Examples | Pipeline | Stages connected by queues, each ends by passing the sentinel on |
| 16 | Examples | Cache | A lock around check-and-set computes a value once |
| 16 | Examples | Timeout | `join(seconds)` then `is_alive()`; a daemon thread cannot be killed |
| 16 | Examples | Transfers | Lock both accounts in id order to avoid deadlock |
import asyncio
import time
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock

# A COROUTINE is a function that can PAUSE at "await" and let other work run, all in ONE thread.
#   async def f(): ...     defines a coroutine function; calling it gives a coroutine OBJECT
#   await x                pauses until x is done (only allowed inside async def)
#   asyncio.run(main())    runs the event loop until main() finishes
# Great for waiting work (network, sockets, timers) with thousands of tasks.

async def hello():
    return "hi"

# 1. A coroutine object does nothing until it is awaited or run
c = hello()
print(type(c).__name__)                         # coroutine
print(asyncio.run(c))                           # hi

c2 = hello()                                    # a coroutine is driven like a generator
try:
    c2.send(None)
except StopIteration as e:
    print(e.value)                              # hi

async def fetch(name, delay):
    await asyncio.sleep(delay)                  # pauses THIS coroutine, others keep running
    return f"{name} done"

# 2. One after the other, or at the same time
async def demo_concurrency():
    start = time.perf_counter()
    a = await fetch("a", 0.1)
    b = await fetch("b", 0.1)
    sequential = time.perf_counter() - start
    start = time.perf_counter()
    results = await asyncio.gather(fetch("c", 0.1), fetch("d", 0.1))
    parallel = time.perf_counter() - start
    print([a, b], results, sequential >= 0.19, parallel < 0.18)
    # ['a done', 'b done'] ['c done', 'd done'] True True

# 3. Tasks start running as soon as the current coroutine pauses
async def worker(name, delay, log):
    log.append(f"{name} start")
    await asyncio.sleep(delay)
    log.append(f"{name} end")

async def demo_tasks():
    log = []
    slow = asyncio.create_task(worker("slow", 0.1, log))
    fast = asyncio.create_task(worker("fast", 0.02, log))
    log.append("main continues")                # no await yet, so the tasks have not started
    await asyncio.gather(slow, fast)
    print(log)      # ['main continues', 'slow start', 'fast start', 'fast end', 'slow end']

# 4. Blocking code freezes EVERY coroutine
async def blocking_task():
    time.sleep(0.05)                            # WRONG inside async code: nobody else can run

async def friendly_task():
    await asyncio.sleep(0.05)

async def demo_blocking():
    start = time.perf_counter()
    await asyncio.gather(blocking_task(), blocking_task())
    blocked = time.perf_counter() - start
    start = time.perf_counter()
    await asyncio.gather(friendly_task(), friendly_task())
    friendly = time.perf_counter() - start
    print(blocked >= 0.09, friendly < 0.09)     # True True

# 5. Timeouts (Python 3.11+)
async def demo_timeouts():
    try:
        async with asyncio.timeout(0.05):
            await asyncio.sleep(1)
    except TimeoutError:
        print("timeout")                        # timeout
    try:
        await asyncio.wait_for(asyncio.sleep(1), 0.05)
    except TimeoutError:
        print("wait_for timed out")             # wait_for timed out

# 6. Cancellation: the task gets CancelledError at its await, and can clean up
async def forever(log):
    log.append("started")
    try:
        while True:
            await asyncio.sleep(0.01)
    finally:
        log.append("cleanup")

async def demo_cancel():
    log = []
    task = asyncio.create_task(forever(log))
    await asyncio.sleep(0.03)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("cancelled")                      # cancelled
    print(log)                                  # ['started', 'cleanup']

# 7. Errors in several tasks
async def ok():
    return "ok"

async def bad():
    raise ValueError("bad")

async def double(n):
    await asyncio.sleep(0)
    return n * 2

async def slow_forever():
    await asyncio.sleep(1)

async def demo_errors():
    results = await asyncio.gather(ok(), bad(), return_exceptions=True)
    print([type(r).__name__ if isinstance(r, Exception) else r for r in results])   # ['ok', 'ValueError']

    async with asyncio.TaskGroup() as tg:       # structured concurrency (Python 3.11+)
        t1 = tg.create_task(double(1))
        t2 = tg.create_task(double(2))
    print([t1.result(), t2.result()])           # [2, 4]

    try:
        async with asyncio.TaskGroup() as tg:   # if one task fails, the others are cancelled
            tg.create_task(bad())
            tg.create_task(slow_forever())
    except* ValueError as eg:
        print("group:", [str(e) for e in eg.exceptions])        # group: ['bad']

# 8. Coordination: Queue, Semaphore, Event
async def producer(q):
    for i in (1, 2, 3):
        await q.put(i)
        await asyncio.sleep(0)
    await q.put(None)

async def consumer(q, out):
    while (item := await q.get()) is not None:
        out.append(item * 10)

async def demo_coordination():
    q, out = asyncio.Queue(), []
    await asyncio.gather(producer(q), consumer(q, out))
    print(out)                                  # [10, 20, 30]

    sem = asyncio.Semaphore(2)                  # at most 2 at a time
    state = {"active": 0, "peak": 0}

    async def limited():
        async with sem:
            state["active"] += 1
            state["peak"] = max(state["peak"], state["active"])
            await asyncio.sleep(0.01)
            state["active"] -= 1

    await asyncio.gather(*(limited() for _ in range(5)))
    print(state["peak"])                        # 2

    event, log = asyncio.Event(), []

    async def waiter():
        log.append("waiting")
        await event.wait()
        log.append("woke")

    async def setter():
        await asyncio.sleep(0.01)
        log.append("set")
        event.set()

    await asyncio.gather(waiter(), setter())
    print(log)                                  # ['waiting', 'set', 'woke']

# 9. Async iterators, async comprehensions, async context managers
async def ticker(n):
    for i in range(n):
        await asyncio.sleep(0)
        yield i                                 # an ASYNC generator

class AsyncResource:
    def __init__(self, log):
        self.log = log

    async def __aenter__(self):
        self.log.append("open")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.log.append("close")
        return False

async def demo_async_protocols():
    collected = []
    async for i in ticker(3):
        collected.append(i)
    print(collected, [i * 2 async for i in ticker(3)])          # [0, 1, 2] [0, 2, 4]

    log = []
    async with AsyncResource(log):
        log.append("use")

    @asynccontextmanager
    async def managed():
        log.append("start")
        try:
            yield "res"
        finally:
            log.append("end")

    async with managed() as r:
        log.append(r)
    print(log)                                  # ['open', 'use', 'close', 'start', 'res', 'end']

# 10. Run blocking code in a thread so the loop stays free
async def demo_threads():
    start = time.perf_counter()
    await asyncio.gather(*(asyncio.to_thread(time.sleep, 0.1) for _ in range(3)))
    elapsed = time.perf_counter() - start
    print(elapsed < 0.25, await asyncio.to_thread(sum, [1, 2, 3]))      # True 6

# 11. asyncio.run() cannot be used inside a running loop
async def demo_nested():
    inner = hello()
    try:
        asyncio.run(inner)
    except RuntimeError:
        inner.close()
        print("RuntimeError")                   # RuntimeError

# 12. AsyncMock: the mock for coroutines (Module 20, file 01)
async def demo_asyncmock():
    m = AsyncMock(return_value=5)
    print(await m(), m.await_count)             # 5 1

# 13. A network server in 10 lines
async def demo_server():
    async def handle(reader, writer):
        data = await reader.readline()
        writer.write(data.upper())
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    server = await asyncio.start_server(handle, "127.0.0.1", 0)
    port = server.sockets[0].getsockname()[1]
    reader, writer = await asyncio.open_connection("127.0.0.1", port)
    writer.write(b"hello\n")
    await writer.drain()
    print(await reader.readline())              # b'HELLO\n'
    writer.close()
    await writer.wait_closed()
    server.close()
    await server.wait_closed()

async def main():
    await demo_concurrency()
    await demo_tasks()
    await demo_blocking()
    await demo_timeouts()
    await demo_cancel()
    await demo_errors()
    await demo_coordination()
    await demo_async_protocols()
    await demo_threads()
    await demo_nested()
    await demo_asyncmock()
    await demo_server()

if __name__ == "__main__":
    asyncio.run(main())

# async vs threads
#   asyncio   one thread, switches ONLY at await: no data races between awaits, thousands of tasks, but
#             every library you call must be async (or run in to_thread)
#   threads   the OS switches anywhere: simpler with blocking libraries, needs locks
# Typical uses: web servers (FastAPI/Starlette run on asyncio), many HTTP calls, MQTT, BLE, sockets, bots.
# Common mistakes: forgetting "await" (the coroutine never runs: "coroutine was never awaited"),
# blocking calls in a coroutine, calling asyncio.run() twice inside one program's loop.
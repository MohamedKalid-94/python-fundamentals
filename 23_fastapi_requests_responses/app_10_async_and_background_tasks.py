import asyncio
import time

from fastapi import BackgroundTasks, FastAPI

# def or async def? (this matters a lot for LLM, vector-store and database calls)
#
#   def endpoint():          FastAPI runs it in a THREAD POOL. Blocking calls are fine
#                            (time.sleep, requests.get, a normal database driver).
#   async def endpoint():    FastAPI runs it ON THE EVENT LOOP. You must only await async code there.
#                            ONE blocking call (time.sleep, requests.get) freezes EVERY other request.
#                            It is the same as blocking the main loop of a bare-metal program.
#
# RULES OF THUMB
#   - the library has an async API (httpx.AsyncClient, an async OpenAI/Anthropic client, asyncpg)
#       -> async def + await
#   - the library is blocking and you do not want to rewrite it -> plain def, or
#       await asyncio.to_thread(blocking_function, args) inside an async def
#   - many independent waits (3 vector searches, 5 API calls) -> asyncio.gather(...): the total time is
#     the SLOWEST call, not the sum (Module 20, file 08)
#
# BACKGROUND TASKS: work that runs AFTER the response has been sent, in the same process.
#   background_tasks.add_task(function, arguments)      the function may be def or async def
#   Good for: writing a log line, sending a short e-mail, clearing a cache.
#   Not for: heavy or long work, or anything that must not be lost if the server restarts.
#   Use a task queue (Celery, RQ, arq) and a separate worker for that.
#   Return 202 Accepted for "I took your request, the work is not finished yet".

app = FastAPI()


@app.get("/sync")
def sync_endpoint():
    time.sleep(0.01)                    # blocking, but harmless here: it runs in a worker thread
    return {"mode": "sync"}


@app.get("/async")
async def async_endpoint():
    await asyncio.sleep(0.01)           # does not block the event loop
    return {"mode": "async"}


def on_event_loop() -> bool:
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False


@app.get("/where-sync")
def where_sync():
    return {"on_event_loop": on_event_loop()}       # False: a def endpoint runs in a worker thread


@app.get("/where-async")
async def where_async():
    return {"on_event_loop": on_event_loop()}       # True


async def slow_double(n: int) -> int:
    await asyncio.sleep(0.05)
    return n * 2


@app.get("/gather")
async def gather():
    results = await asyncio.gather(slow_double(1), slow_double(2), slow_double(3))
    return {"results": results}                     # about 0.05 s in total, not 0.15 s


def blocking_read(n: int) -> int:
    time.sleep(0.01)                                # pretend: a blocking driver
    return n + 1


@app.get("/to-thread/{n}")
async def to_thread(n: int):
    return {"result": await asyncio.to_thread(blocking_read, n)}


log: list[str] = []


def write_log(message: str):
    log.append(message)


async def async_log(message: str):
    await asyncio.sleep(0)
    log.append(message)


@app.post("/notify/{user}", status_code=202)
def notify(user: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"notified {user}")
    background_tasks.add_task(async_log, f"async notified {user}")
    return {"status": "accepted"}                   # sent first; the tasks run after it
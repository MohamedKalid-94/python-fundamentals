Write the questions as # comments and your solutions as code below each one.

Mocking, monkey patching, signals

Write get_user(user_id, http_get) that calls http_get(url) and returns the name from the JSON. Test it with a stub, with a Mock (check the URL and the call count), and with side_effect that raises ConnectionError on the first call.
Test a function that writes a log file with mock_open, and a function that reads the environment variable APP_MODE with patch.dict. Then test code that calls datetime.now() by injecting a clock.
Write a FakeGpio class with set(pin, value) and read(pin) and a blink(gpio, pin, times) function. Test that blink toggles the pin the right number of times, using the fake first and a create_autospec mock second.
Show with two small modules (use types.ModuleType) why patch("consumer.helper") works and patch("lib.helper") does not for code that did from lib import helper.
Write a decorator @patched_during(obj, name, value) that works as a decorator and as a with block, and restores the original even when the test raises.
Write a long-running worker that processes items from a list and stops cleanly on SIGINT and SIGTERM, saving its position to a file. Use signal.raise_signal to test it, and print the saved position.

Type hints, automation, humanize

Write @validate like the one in file 04 for dict[str, int], tuple[int, ...], Literal["r", "w"] and Optional[list[str]]. Add checks for the return value, and a clear error message with the argument name and the path to the bad item (for example numbers[2]).
Write a TypedDict for a sensor reading and a function that checks a dictionary against it at run time (required keys, types, extra keys).
Write a script tidy.py with argparse: --dry-run, --move-by-extension, --delete-older-than 30, logging, and a summary at the end. Test it on a temporary folder with files of different ages.
Write watch(folder, callback, interval) that polls a folder and calls the callback with the created, modified and deleted files. Test it with a fake clock and a fake file system (a function returning a dictionary).
Write your own naturaltime(then, now) for datetimes (“just now”, “5 minutes ago”, “yesterday”, “3 days ago”, “in 2 hours”) and test the boundaries (59 seconds, 60 seconds, 23 hours, 24 hours).

Context managers, coroutines

Write a Timer context manager (class version and @contextmanager version) that stores the elapsed time in .elapsed and still does so when the block raises. Make one version usable as a decorator.
Write serial_session(port) as a context manager that opens a fake port, sets a “busy” flag, and always releases it, with a test where the body raises an error. Add a retries option that retries only the open step.
Write an async function fetch_all(urls, limit) that uses a fake fetch coroutine, runs at most limit at the same time (with a Semaphore), keeps the order of the results, and cancels everything when one call fails (use a TaskGroup).
Build an async producer-consumer pipeline with an asyncio.Queue(maxsize=5), three consumers, a sentinel per consumer, and a timeout for the whole run. Test the order and the total.
Write an async context manager async_timer and an async generator read_chunks(data, size) that yields chunks with an await asyncio.sleep(0) between them. Use both with async for and async with.

Descriptors, memory, immutability

Write the descriptors Range(min, max), String(max_length) and Choice(*options) with __set_name__, and use them in a Device class. Add a descriptor Computed(func) that is read-only and recalculated each time.
Write a register class with the bit fields of a 32-bit status register (3 single bits and two multi-bit fields) using BitField, plus from_bytes and to_bytes for big-endian data. Print the register as a binary table.
Reproduce three memory leaks (global list, lru_cache on a method, event listeners) and fix each. Prove every fix with weakref and gc.collect(), and show the memory difference with tracemalloc.
Write a deep_freeze that handles dictionaries, lists, sets and dataclasses, and a deep_thaw that converts back. Show that the frozen version is hashable, and measure how much slower a modification is compared with a mutable version.

DSL, data model

Extend the filter DSL of file 12 with .isin([...]), .contains("text"), .between(a, b) and sort_by(field), and a to_sql_like_text() method that prints the rule in plain text.
Write an external DSL for sensor alarm rules, for example temp > 30 and (hum < 20 or pressure != 1013), with a tokenizer, a parser that builds a small tree of objects, an evaluator for a dictionary of readings, and good error messages with the position of the problem.
Write a Money class (amount in cents and a currency) with the full data model: +, -, * by a number, / by a number (returning cents correctly rounded), comparisons (same currency only, otherwise NotImplemented or an error), __hash__, __format__ (f"{m:,.2f}"), __bool__, __round__, sum() support, and __repr__ that can be pasted back into Python.
Write a Matrix class with __getitem__ for m[i, j] and m[i], __matmul__, __add__, __iter__, __eq__, __repr__, __len__, and __contains__, and compare its results with a list of lists.
Predict first, then run, and explain each result in a comment:
python
import asyncio
from contextlib import contextmanager

class D:
    def __set_name__(self, owner, name): self.n = name
    def __get__(self, obj, owner=None): return (self.n, obj is None)
    def __set__(self, obj, value): obj.__dict__[self.n] = value

class A:
    d = D()
a = A()
print(a.d, A.d)
a.d = 5
print(a.__dict__, a.d)

@contextmanager
def cm(log):
    log.append("in")
    try:
        yield
    finally:
        log.append("out")

log = []
try:
    with cm(log):
        raise KeyError("k")
except KeyError as e:
    print(log, repr(e))

class V:
    def __init__(self, n): self.n = n
    def __add__(self, o): return V(self.n + o.n)
    def __radd__(self, o): return self if o == 0 else NotImplemented
    def __repr__(self): return f"V({self.n})"
print(sum([V(1), V(2), V(3)]), 0 + V(5))
try:
    "a" + V(1)
except TypeError:
    print("TypeError")

async def a1():
    await asyncio.sleep(0)
    return 1
async def main():
    t = asyncio.create_task(a1())
    print(t.done())
    await asyncio.sleep(0.01)
    print(t.done(), t.result())
asyncio.run(main())
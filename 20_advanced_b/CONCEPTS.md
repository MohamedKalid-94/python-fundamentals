# Module 20: Advanced Concepts B, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Mocking | Test doubles | Dummy (unused), stub (canned answers), fake (simple working version), mock (records calls), spy (wraps the real thing) |
| 01 | Mocking | `Mock` | Accepts any call; `return_value`, `side_effect` (list, exception or function), `call_args`, `call_count`, `assert_called_once_with`, `assert_any_call` |
| 01 | Mocking | `MagicMock` | Also supports magic methods (`len`, `[]`, `str`) |
| 01 | Mocking | `patch` | `patch.object(module, "name")`, `patch("pkg.mod.name")`, `patch.dict(os.environ, {...})`, as a `with` block or a decorator |
| 01 | Mocking | `spec` / `create_autospec` | The mock copies the real signature: unknown attributes and wrong arguments fail |
| 01 | Mocking | Special mocks | `mock_open`, `PropertyMock`, `AsyncMock`, `Mock(wraps=real)` |
| 01 | Mocking | Dependency injection | Pass the dependency in; a test passes a stub |
| 01 | Mocking | Guidelines | Replace boundaries (network, clock, disk, hardware), test results not exact calls, prefer fakes for databases and devices |
| 02 | Monkey Patching | What | Changing a class, module or object at run time (`Dog.speak = f`) |
| 02 | Monkey Patching | Restore | Always put the original back (`try/finally` or `mock.patch`) |
| 02 | Monkey Patching | Name lookup | Patch where the name is USED: `from lib import f` copies the reference |
| 02 | Monkey Patching | Limits | Built-in types cannot be patched |
| 02 | Monkey Patching | Use | Tests, shims, hot fixes; prefer subclassing, composition or injection |
| 03 | Signals | Common signals | `SIGINT` (Ctrl+C), `SIGTERM` (stop), `SIGHUP`, `SIGALRM`, `SIGUSR1`; `SIGKILL` cannot be caught |
| 03 | Signals | API | `signal.signal(sig, handler)`, `getsignal`, `raise_signal`, `SIG_IGN`, `SIG_DFL` |
| 03 | Signals | Default | `SIGINT` raises `KeyboardInterrupt` |
| 03 | Signals | Handler rule | Tiny: set a flag; the main loop does the work (graceful shutdown) |
| 03 | Signals | Limits | Only the main thread installs handlers; Windows supports few signals; `SIGALRM` is Unix only |
| 03 | Signals | Other processes | `child.terminate()`, `child.send_signal(...)`, `os.kill(pid, sig)` |
| 04 | Type Hints | Storage | `__annotations__`; not enforced at run time |
| 04 | Type Hints | Forms | `int | None`, `Optional`, `Union`, `Literal`, `Final`, `ClassVar`, `TypedDict` (`NotRequired`), `Callable`, `Self`, `NewType`, `Annotated`, `TypeGuard`, `cast`, `Any` |
| 04 | Type Hints | Exhaustive checks | `assert_never(x)` |
| 04 | Type Hints | Introspection | `get_type_hints`, `get_origin`, `get_args`, `inspect.signature` |
| 04 | Type Hints | Run-time use | FastAPI, Pydantic and dataclasses read the hints; you can write your own validator |
| 04 | Type Hints | Checkers | `mypy`, `Pyright`/Pylance; `# type: ignore[...]`, `reveal_type`; adopt gradually |
| 05 | Automation | Safety habits | `--dry-run`, idempotent, parameters (paths, clocks) for testing, atomic writes, exit codes, secrets in environment variables |
| 05 | Automation | File tasks | `pathlib`, `shutil`, regex renames, content hashes for duplicates, `os.utime` for dates |
| 05 | Automation | Scheduling | `sched` (standard), `schedule`/APScheduler, cron, Windows Task Scheduler; a fake clock makes it testable |
| 05 | Automation | Programs | `subprocess.run([...], check=True, capture_output=True, text=True, timeout=...)` |
| 05 | Automation | Watching | Compare snapshots (or use `watchdog`) |
| 06 | Humanize | Purpose | Turn raw values into readable text only for display |
| 06 | Humanize | Functions | `naturalsize`, `intcomma`, `ordinal`, `plural`, `apnumber`, `intword`, `naturaldelta`, `naturaltime`, `precisedelta` |
| 06 | Humanize | Package | `pip install humanize` (also `rich.filesize`, `babel` for locales) |
| 06 | Humanize | Rule | Store raw data (bytes, seconds, UTC); never parse humanized text back |
| 07 | Context Managers | Protocol | `__enter__` returns the `as` value; `__exit__(exc_type, exc, tb)` returns `True` to swallow the error |
| 07 | Context Managers | Generator form | `@contextmanager`: setup, `yield`, cleanup in `try/finally`; single use |
| 07 | Context Managers | Order | Several contexts close in reverse order |
| 07 | Context Managers | Helpers | `ContextDecorator`, `ExitStack`, `closing`, `suppress`, `nullcontext`, `chdir` (3.11), `localcontext`, `AbstractContextManager` |
| 07 | Context Managers | Patterns | Transaction with rollback, temporary setting, lock, chip select |
| 08 | Coroutines | Basics | `async def` makes a coroutine function; calling it gives a coroutine object; `await` pauses; `asyncio.run(main())` |
| 08 | Coroutines | Concurrency | `asyncio.gather`, `create_task` (starts at the next pause), `TaskGroup` (3.11), `timeout`, `wait_for`, `cancel` |
| 08 | Coroutines | Errors | `gather(return_exceptions=True)`; a failing `TaskGroup` cancels the rest and raises an `ExceptionGroup` |
| 08 | Coroutines | Coordination | `asyncio.Queue`, `Semaphore`, `Event`, `Lock` |
| 08 | Coroutines | Async protocols | `async for`, `async with`, `async def` generators, `asynccontextmanager`, async comprehensions |
| 08 | Coroutines | Blocking | `time.sleep` blocks every task; use `await asyncio.sleep` or `asyncio.to_thread(func, ...)` |
| 08 | Coroutines | Pitfalls | Forgetting `await`; `asyncio.run` inside a running loop (`RuntimeError`) |
| 08 | Coroutines | Choose | asyncio for many waiting tasks in one thread; threads for blocking libraries |
| 09 | Descriptors | Protocol | `__get__(obj, owner)`, `__set__`, `__delete__`, `__set_name__` on a class attribute |
| 09 | Descriptors | Data vs non-data | A data descriptor (has `__set__`) beats the instance `__dict__`; a non-data one loses to it |
| 09 | Descriptors | Built on them | Functions (methods), `property`, `classmethod`, `staticmethod`, `cached_property`, ORM fields |
| 09 | Descriptors | Uses | Reusable validated fields, lazy values, per-object data (`WeakKeyDictionary`), hardware register bit fields |
| 09 | Descriptors | Class access | `obj is None` means the attribute was read on the class: return `self` |
| 10 | Memory Leaks | Meaning | Objects you no longer need are still reachable |
| 10 | Memory Leaks | Causes | Unbounded caches or lists, `lru_cache` on methods, listeners never removed, stored exceptions (tracebacks), unclosed resources |
| 10 | Memory Leaks | Fixes | Bounded caches (`lru_cache(maxsize=n)`, `deque(maxlen=n)`), `WeakMethod`/`weakref`, per-object caches, `with` |
| 10 | Memory Leaks | Finding them | `tracemalloc` snapshots and `compare_to`, counting objects with `gc.get_objects()`, `objgraph`, `memray` |
| 10 | Memory Leaks | Not a leak | Memory that does not shrink but does not grow either |
| 10 | Memory Leaks | `ResourceWarning` | Shown when a file or socket is destroyed unclosed (`python -X dev`) |
| 11 | Immutable Data | Built-ins | `int`, `str`, `bytes`, `tuple`, `frozenset`; a tuple holding a list is not truly frozen or hashable |
| 11 | Immutable Data | Tools | `MappingProxyType` (read-only dict view), `@dataclass(frozen=True)` + `replace`, `NamedTuple`, `memoryview.toreadonly()` |
| 11 | Immutable Data | By hand | `__slots__` + a guarded `__setattr__`; `object.__setattr__` in `__init__`; `with_x()` returns a new object |
| 11 | Immutable Data | Structural sharing | New versions reuse the unchanged parts (persistent stack) |
| 11 | Immutable Data | Benefits | Hashable keys, safe to share between threads, no aliasing surprises, safe defaults (`()` not `[]`) |
| 11 | Immutable Data | Third-party | `pyrsistent`, `immutables`, `frozendict` |
| 12 | DSL | Kinds | Internal (inside Python) and external (own syntax with a parser) |
| 12 | DSL | Internal tools | Operator overloading, method chaining (`return self`), `with` blocks, decorators, `__getattr__` |
| 12 | DSL | External | Tokenizer (regex) plus recursive-descent parser: one method per grammar rule |
| 12 | DSL | Rules | Never `eval` DSL text; good error messages matter most; start internal |
| 13 | Data Model | Idea | Dunder methods connect your class to the language (`len`, `+`, `for`, `with`, `[]`, `in`, `hash`) |
| 13 | Data Model | Return `NotImplemented` | For unknown operand types, so Python tries the other side |
| 13 | Data Model | Reflected and in-place | `__radd__` (for `0 + v`, `sum`), `__iadd__` (same object changes) |
| 13 | Data Model | Containers | `__getitem__`, `__setitem__`, `__len__`, `__contains__`, `__iter__`, `__reversed__`, `__missing__` (not used by `get`) |
| 13 | Data Model | Comparison | `__eq__` with `__hash__`; `functools.total_ordering` |
| 13 | Data Model | Others | `__index__`, `__class_getitem__`, `__dir__`, `__format__`, `__bool__` |
| 13 | Data Model | Lookup | Special methods are found on the TYPE, not the instance |
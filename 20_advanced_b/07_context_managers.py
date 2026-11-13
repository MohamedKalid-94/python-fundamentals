import contextlib
import tempfile
from contextlib import AbstractContextManager, ContextDecorator, ExitStack, closing, contextmanager
from decimal import Decimal, localcontext
from pathlib import Path
from types import SimpleNamespace

# The "with" statement guarantees SETUP and CLEANUP around a block.
#   with A() as x:  body      ==      x = A().__enter__() ; try: body ; finally: __exit__(...)

log = []

# 1. A class with __enter__ and __exit__
class Tracer:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        log.append(f"enter {self.name}")
        return self                             # this becomes "as x"

    def __exit__(self, exc_type, exc, tb):      # the exception (or None, None, None)
        log.append(f"exit {self.name} ({exc_type.__name__ if exc_type else 'ok'})")
        return False                            # False: do not hide the exception

with Tracer("a") as t:
    log.append("body")
print(log)                                      # ['enter a', 'body', 'exit a (ok)']

log.clear()
try:
    with Tracer("b"):
        raise ValueError("bad")
except ValueError:
    print(log)                                  # ['enter b', 'exit b (ValueError)']

# 2. Returning True from __exit__ SWALLOWS the exception
class IgnoreZeroDivision:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return exc_type is ZeroDivisionError

with IgnoreZeroDivision():
    1 / 0
print("continued")                              # continued

# 3. Several at once: they close in REVERSE order (like a stack)
log.clear()
with (Tracer("x") as x, Tracer("y") as y):      # parentheses allowed since Python 3.10
    log.append("body")
print(log)                                      # ['enter x', 'enter y', 'body', 'exit y (ok)', 'exit x (ok)']

# 4. The short way: @contextmanager and a generator (code before yield = enter, after = exit)
@contextmanager
def temp_value(obj, attribute, value):
    old = getattr(obj, attribute)
    setattr(obj, attribute, value)
    try:
        yield old                               # the value of "as"
    finally:                                    # ALWAYS use try/finally: it also runs on errors
        setattr(obj, attribute, old)

cfg = SimpleNamespace(debug=False)
with temp_value(cfg, "debug", True) as old:
    print(cfg.debug, old)                       # True False
print(cfg.debug)                                # False

@contextmanager
def ignore_zero():                              # to swallow an error: catch it and do not re-raise
    try:
        yield
    except ZeroDivisionError:
        pass

with ignore_zero():
    1 / 0
print("after")                                  # after

# A generator-based manager can be used only ONCE
cm = temp_value(cfg, "debug", True)
with cm:
    pass
try:
    with cm:
        pass
except RuntimeError:
    print("RuntimeError")                       # RuntimeError

# 5. ContextDecorator: the same object works as a "with" AND as a decorator
class Logged(ContextDecorator):
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        log.append(f"enter {self.name}")
        return self

    def __exit__(self, *exc):
        log.append(f"exit {self.name}")
        return False

log.clear()

@Logged("f")
def f():
    log.append("call")

f()
print(log)                                      # ['enter f', 'call', 'exit f']

# 6. ExitStack: a number of contexts that is only known at run time
with tempfile.TemporaryDirectory() as tmp:
    with ExitStack() as stack:
        files = [stack.enter_context(open(Path(tmp) / f"{i}.txt", "w", encoding="utf-8")) for i in range(3)]
        for i, fh in enumerate(files):
            fh.write(str(i))
    print([fh.closed for fh in files])          # [True, True, True]

# 7. closing(): give any object with close() a "with"
class Resource:
    closed = False

    def close(self):
        self.closed = True

with closing(Resource()) as resource:
    pass
print(resource.closed)                          # True

# 8. Other helpers in contextlib
with tempfile.TemporaryDirectory() as tmp:
    before = Path.cwd()
    with contextlib.chdir(tmp):                 # Python 3.11+
        print(Path.cwd().resolve() == Path(tmp).resolve())      # True
    print(Path.cwd() == before)                 # True

with localcontext() as ctx:                     # a temporary change of the decimal precision
    ctx.prec = 5
    print(Decimal(1) / Decimal(3))              # 0.33333
print(Decimal(1) / Decimal(4))                  # 0.25

# 9. AbstractContextManager gives you a default __enter__ (it returns self)
class Quiet(AbstractContextManager):
    def __exit__(self, *exc):
        return None

with Quiet() as q:
    print(type(q).__name__)                     # Quiet

# 10. A TRANSACTION: undo the changes if an error happens
class Transaction:
    def __init__(self, data):
        self.data = data

    def __enter__(self):
        self.backup = dict(self.data)
        return self.data

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.data.clear()
            self.data.update(self.backup)
        return False

state = {"a": 1}
with Transaction(state) as s:
    s["b"] = 2
print(state)                                    # {'a': 1, 'b': 2}
try:
    with Transaction(state) as s:
        s["c"] = 3
        raise ValueError("fail")
except ValueError:
    print(state)                                # {'a': 1, 'b': 2}      "c" was rolled back

# WHERE YOU ALREADY USE "with"
#   open()  threading.Lock  tempfile.TemporaryDirectory  sqlite3 connection (commit/rollback)
#   zipfile  socket  subprocess.Popen  unittest.mock.patch  decimal.localcontext  concurrent futures pools
# ASYNC VERSION: "async with" uses __aenter__ and __aexit__ (next file).
# EMBEDDED: wrap "select the chip ... deselect the chip", "lock the bus ... unlock", "power on ... power off".
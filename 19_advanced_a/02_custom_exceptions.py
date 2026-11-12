import functools
import json
import pickle
import sys

# Module 14 showed how to write a custom exception. Here is how to design a family of them.

# 1. A base class that carries a CODE, a message and CONTEXT data
class AppError(Exception):
    """Base of every error raised by this application."""

    code = "E000"
    retryable = False

    def __init__(self, message="", **context):
        super().__init__(message)
        self.message = message
        self.context = context

    def __str__(self):
        extra = ", ".join(f"{k}={v!r}" for k, v in sorted(self.context.items()))
        return f"[{self.code}] {self.message}" + (f" ({extra})" if extra else "")

    def to_dict(self):                          # ready for JSON logs and API answers
        return {"type": type(self).__name__, "code": self.code,
                "message": self.message, "context": self.context}


# 2. Join a built-in family: callers who catch LookupError also catch NotFoundError
class NotFoundError(AppError, LookupError):
    code = "E404"

class DeviceTimeout(AppError):
    code = "E408"
    retryable = True

class ConfigError(AppError):
    code = "E500"

print(NotFoundError("user missing", user_id=7))             # [E404] user missing (user_id=7)
try:
    raise NotFoundError("user missing", user_id=7)
except LookupError as e:
    print("caught as LookupError:", e)          # caught as LookupError: [E404] user missing (user_id=7)
print([c.__name__ for c in NotFoundError.__mro__])
# ['NotFoundError', 'AppError', 'LookupError', 'Exception', 'BaseException', 'object']
print(DeviceTimeout("no reply", port="COM3", waited=0.5).to_dict())
# {'type': 'DeviceTimeout', 'code': 'E408', 'message': 'no reply', 'context': {'port': 'COM3', 'waited': 0.5}}

# 3. Policy lives in the exception: a retry loop asks the error whether it is worth repeating
def call_with_retry(func, attempts=3):
    for n in range(1, attempts + 1):
        try:
            return func(), n
        except AppError as e:
            if not e.retryable or n == attempts:
                raise

calls = {"n": 0}

def flaky():
    calls["n"] += 1
    if calls["n"] < 3:
        raise DeviceTimeout("slow")
    return "ok"

print(call_with_retry(flaky))                   # ('ok', 3)

calls["n"] = 0

def missing():
    calls["n"] += 1
    raise NotFoundError("gone")

try:
    call_with_retry(missing)
except NotFoundError:
    print(calls["n"], "call")                   # 1 call      not retryable: it stopped at once

# 4. Translate the errors of other libraries into yours, and keep the cause
def read_config(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ConfigError("invalid JSON", line=e.lineno) from e

try:
    read_config("{bad")
except ConfigError as e:
    print(e, "|", type(e.__cause__).__name__)   # [E500] invalid JSON (line=1) | JSONDecodeError

def translate(source, target, message):         # the same idea as a decorator
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except source as e:
                raise target(message, original=type(e).__name__) from e
        return wrapper
    return decorator

@translate(KeyError, NotFoundError, "no such key")
def lookup(data, key):
    return data[key]

try:
    lookup({}, "x")
except NotFoundError as e:
    print(e, type(e.__cause__).__name__)        # [E404] no such key (original='KeyError') KeyError

# 5. PICKLING: exceptions travel between processes (multiprocessing, ProcessPoolExecutor).
#    Python rebuilds them with  cls(*self.args).  If __init__ takes arguments that are not in
#    self.args, the copy fails.
class BadError(Exception):
    def __init__(self, code, message):
        super().__init__(message)               # args == (message,), the code is lost
        self.code = code

try:
    pickle.loads(pickle.dumps(BadError(1, "x")))
except TypeError:
    print("TypeError")                          # TypeError

class GoodError(Exception):
    def __init__(self, code, message):
        super().__init__(code, message)         # args == (code, message)
        self.code = code
        self.message = message

copy = pickle.loads(pickle.dumps(GoodError(1, "x")))
print(copy.code, copy.message, copy.args)       # 1 x (1, 'x')

# 6. Several custom errors at once (Python 3.11+)
try:
    raise ExceptionGroup("batch", [NotFoundError("a"), DeviceTimeout("b")])
except* NotFoundError as eg:
    print("not found:", [str(e) for e in eg.exceptions])        # not found: ['[E404] a']
except* DeviceTimeout as eg:
    print("timeouts:", [str(e) for e in eg.exceptions])         # timeouts: ['[E408] b']

# 7. A global handler for anything nobody caught (sys.excepthook runs for an unhandled error)
captured = []

def hook(exc_type, exc, tb):
    captured.append(f"unhandled {exc_type.__name__}: {exc}")

original = sys.excepthook
sys.excepthook = hook
sys.excepthook(AppError, AppError("boom"), None)    # Python calls this for you at a crash
sys.excepthook = original
print(captured)                                 # ['unhandled AppError: [E000] boom']

# 8. Notes add information to an exception while it travels up (Python 3.11+)
error = ConfigError("bad port")
error.add_note("while reading settings.json")
print(error.__notes__)                          # ['while reading settings.json']

# DESIGN GUIDE
#   - ONE base class per library or application (AppError) so users can write "except AppError".
#   - Child classes by what the CALLER can DO about it (retry, fix the input, give up),
#     not by where in your code it happened.
#   - Inherit from a built-in too (LookupError, ValueError) when the meaning matches.
#   - Keep data on the object (code, context), and a clear message for humans.
#   - Pass every constructor argument to super().__init__ so the exception can be pickled.
#   - Raise with "from" when you translate; never swallow the original silently.
#   - Do not use exceptions for normal control flow in hot loops; they are slower than an "if".
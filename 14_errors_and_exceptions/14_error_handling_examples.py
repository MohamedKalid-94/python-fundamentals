import io
import json
import logging


# 1. A conversion with a default value
def to_int(text, default=None):
    try:
        return int(text)
    except (ValueError, TypeError):
        return default

print(to_int("42"), to_int("x"), to_int(None, -1))      # 42 None -1


# 2. Retry a few times, then give up with a clear error that keeps the cause
def retry(func, attempts=3):
    last = None
    for n in range(1, attempts + 1):
        try:
            return func()
        except ConnectionError as e:
            last = e
            print(f"attempt {n} failed: {e}")
    raise RuntimeError(f"gave up after {attempts} attempts") from last


calls = {"n": 0}

def flaky():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("no link")
    return "ok"

print(retry(flaky))
# attempt 1 failed: no link
# attempt 2 failed: no link
# ok

def always_fail():
    raise ConnectionError("down")

try:
    retry(always_fail, 2)
except RuntimeError as e:
    print(e, "| cause:", e.__cause__)
# attempt 1 failed: down
# attempt 2 failed: down
# gave up after 2 attempts | cause: down


# 3. Report ALL the problems at once instead of stopping at the first
class ValidationError(Exception):
    def __init__(self, errors):
        super().__init__("; ".join(errors))
        self.errors = errors


def validate(cfg):
    errors = []
    if not isinstance(cfg.get("baud"), int):
        errors.append("baud must be an int")
    if cfg.get("parity") not in ("N", "E", "O"):
        errors.append("parity must be N, E or O")
    if errors:
        raise ValidationError(errors)
    return cfg

try:
    validate({"baud": "fast", "parity": "X"})
except ValidationError as e:
    print(len(e.errors), e)                     # 2 baud must be an int; parity must be N, E or O
print(validate({"baud": 9600, "parity": "N"}))  # {'baud': 9600, 'parity': 'N'}


# 4. Device errors with codes
class DeviceError(Exception):
    code = 0

    def __str__(self):
        return f"[E{self.code:03d}] {self.args[0]}"


class TimeoutErr(DeviceError):
    code = 1


class CrcErr(DeviceError):
    code = 2


def read_frame(kind):
    if kind == "timeout":
        raise TimeoutErr("no response")
    if kind == "crc":
        raise CrcErr("bad checksum")
    return b"\x01\x02"

for kind in ("ok", "timeout", "crc"):
    try:
        print(read_frame(kind))
    except DeviceError as e:
        print(type(e).__name__, e)
# b'\x01\x02'
# TimeoutErr [E001] no response
# CrcErr [E002] bad checksum


# 5. Translate a low-level error into the error of your own layer
class ConfigError(Exception):
    pass


def load(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ConfigError("config file is not valid JSON") from e

try:
    load("{bad")
except ConfigError as e:
    print(e, "|", type(e.__cause__).__name__)   # config file is not valid JSON | JSONDecodeError


# 6. Log the lines you cannot parse and keep going
stream = io.StringIO()
log = logging.getLogger("example")
log.setLevel(logging.INFO)
log.propagate = False
handler = logging.StreamHandler(stream)
handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
log.addHandler(handler)


def parse_line(line):
    try:
        name, value = line.split("=")
        return name, float(value)
    except ValueError:
        log.warning("bad line %r", line)
        return None

print(parse_line("TEMP=36.5"), parse_line("garbage"), parse_line("A=x"))
# ('TEMP', 36.5) None None
print(stream.getvalue().splitlines())
# ["WARNING:bad line 'garbage'", "WARNING:bad line 'A=x'"]


# 7. Always release the bus, whatever happens
events = []

class Bus:
    def lock(self):
        events.append("lock")

    def unlock(self):
        events.append("unlock")

bus = Bus()

def transfer(data):
    bus.lock()
    try:
        if not data:
            raise ValueError("empty transfer")
        events.append(f"sent {len(data)}")
    finally:
        bus.unlock()

transfer(b"abc")
try:
    transfer(b"")
except ValueError as e:
    events.append(f"error: {e}")
print(events)
# ['lock', 'sent 3', 'unlock', 'lock', 'unlock', 'error: empty transfer']


# 8. Process a whole batch, then report every failure together (Python 3.11+)
def process(items):
    errors = []
    for item in items:
        try:
            int(item)
        except ValueError as e:
            errors.append(e)
    if errors:
        raise ExceptionGroup("bad items", errors)

try:
    process(["1", "x", "2", "y"])
except* ValueError as eg:
    print(len(eg.exceptions), "bad items")      # 2 bad items


# 9. A top-level function that turns errors into exit codes
class UserError(Exception):
    pass


def run(arg):
    if arg == "user":
        raise UserError("please check the input")
    if arg == "bug":
        raise RuntimeError("unexpected")
    return "done"


def main(arg):
    try:
        print(run(arg))
        return 0
    except UserError as e:
        print("error:", e)
        return 2
    except Exception:
        print("internal error")
        return 1

print([main(a) for a in ("ok", "user", "bug")])
# done
# error: please check the input
# internal error
# [0, 2, 1]
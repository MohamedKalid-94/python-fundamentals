import asyncio
import signal
from dataclasses import FrozenInstanceError, dataclass
from typing import get_args, get_origin, get_type_hints
from unittest.mock import AsyncMock, Mock


# 1. Settings from text: type hints + a frozen dataclass
@dataclass(frozen=True)
class Settings:
    port: int
    debug: bool = False
    tags: tuple[str, ...] = ()


def coerce(value, expected):
    if expected is bool:
        return str(value).lower() in ("1", "true", "yes")
    if get_origin(expected) is tuple:
        item = get_args(expected)[0]
        parts = value.split(",") if isinstance(value, str) else value
        return tuple(coerce(v, item) for v in parts)
    return expected(value)


def load(cls, data):
    hints = get_type_hints(cls)
    return cls(**{key: coerce(value, hints[key]) for key, value in data.items()})


settings = load(Settings, {"port": "502", "debug": "yes", "tags": "a,b"})
print(settings)                                 # Settings(port=502, debug=True, tags=('a', 'b'))
try:
    settings.port = 1
except FrozenInstanceError:
    print("frozen")                             # frozen


# 2. A retry loop tested with a mock: no real network, no real waiting
def fetch_with_retry(fetch, url, attempts=3, sleep=None):
    for n in range(1, attempts + 1):
        try:
            return fetch(url)
        except ConnectionError:
            if n == attempts:
                raise
            sleep(2 ** (n - 1))                 # wait 1 s, then 2 s ...

fetch = Mock(side_effect=[ConnectionError(), ConnectionError(), "payload"])
fake_sleep = Mock()
print(fetch_with_retry(fetch, "http://x", sleep=fake_sleep))    # payload
print(fetch.call_count, fake_sleep.call_args_list)              # 3 [call(1), call(2)]


# 3. The same idea in async code, with the sleep injected
async def retry_async(func, attempts=3, sleep=asyncio.sleep):
    delays = []
    for n in range(1, attempts + 1):
        try:
            return await func(), delays
        except ConnectionError:
            if n == attempts:
                raise
            delays.append(2 ** (n - 1))
            await sleep(0)                      # a real program would await sleep(delay)

flaky = AsyncMock(side_effect=[ConnectionError(), ConnectionError(), "ok"])
result, delays = asyncio.run(retry_async(flaky))
print(result, delays)                           # ok [1, 2]


# 4. A report people can read (see file 06)
def naturalsize(n):
    size = float(n)
    for unit in ("B", "kB", "MB", "GB", "TB"):
        if abs(size) < 1000 or unit == "TB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1000

def naturaldelta(seconds):
    for name, size in (("hour", 3600), ("minute", 60), ("second", 1)):
        if seconds >= size:
            count = seconds // size
            return f"{count} {name}{'' if count == 1 else 's'}"
    return "0 seconds"

files = [("log.txt", 2_048), ("backup.zip", 1_500_000_000), ("photo.jpg", 3_400_000)]
ranked = sorted(files, key=lambda f: f[1], reverse=True)
print([(name, naturalsize(size)) for name, size in ranked])
# [('backup.zip', '1.5 GB'), ('photo.jpg', '3.4 MB'), ('log.txt', '2.0 kB')]
print("total", naturalsize(sum(size for _, size in files)), "| took", naturaldelta(150))
# total 1.5 GB | took 2 minutes


# 5. A loop that stops cleanly when it receives SIGTERM
processed = []
stop = False

def request_stop(signum, frame):
    global stop
    stop = True

previous = signal.signal(signal.SIGTERM, request_stop)
try:
    for item in range(10):
        if item == 4:
            signal.raise_signal(signal.SIGTERM)
        if stop:
            break
        processed.append(item)
finally:
    signal.signal(signal.SIGTERM, previous)
print(processed, stop)                          # [0, 1, 2, 3] True
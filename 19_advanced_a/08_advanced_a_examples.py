import functools
import json
import sys
from abc import ABC, abstractmethod
from collections import OrderedDict
from functools import partial, reduce


# 1. A plugin system: ABC + __init_subclass__ registry + a custom exception family
class PluginError(Exception):
    pass


class UnknownPluginError(PluginError, LookupError):
    def __init__(self, key, available):
        super().__init__(f"unknown plugin {key!r}; available: {', '.join(sorted(available))}")
        self.key = key
        self.available = sorted(available)


class Exporter(ABC):
    registry = {}

    def __init_subclass__(cls, key=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if key:
            Exporter.registry[key] = cls

    @abstractmethod
    def export(self, rows):
        ...

    @classmethod
    def create(cls, key, **options):
        if key not in cls.registry:
            raise UnknownPluginError(key, cls.registry)
        return cls.registry[key](**options)


class CsvExporter(Exporter, key="csv"):
    def __init__(self, sep=","):
        self.sep = sep

    def export(self, rows):
        return "\n".join(self.sep.join(map(str, row)) for row in rows)


class JsonExporter(Exporter, key="json"):
    def export(self, rows):
        return json.dumps(rows)


rows = [[1, "a"], [2, "b"]]
print(Exporter.create("csv", sep=";").export(rows))
# 1;a
# 2;b
print(Exporter.create("json").export(rows))     # [[1, "a"], [2, "b"]]
try:
    Exporter.create("xml")
except LookupError as e:
    print(e)                                    # unknown plugin 'xml'; available: csv, json


# 2. A data pipeline built from small functions
def pipe(value, *funcs):
    return reduce(lambda acc, f: f(acc), funcs, value)

readings = [20.5, None, 21.0, 150.0, 22.5, None, 23.0]
drop_missing = partial(filter, lambda x: x is not None)
clip = lambda values: (min(max(v, 0), 100) for v in values)
average = lambda values: round(sum(values) / len(values), 2)

print(pipe(readings, drop_missing, clip, list, average))        # 37.4


# 3. An LRU cache decorator: the least recently used entry is dropped first
def lru(maxsize):
    def decorator(func):
        cache = OrderedDict()
        stats = {"hits": 0, "misses": 0}

        @functools.wraps(func)
        def wrapper(key):
            if key in cache:
                cache.move_to_end(key)          # mark as recently used
                stats["hits"] += 1
                return cache[key]
            stats["misses"] += 1
            value = func(key)
            cache[key] = value
            if len(cache) > maxsize:
                cache.popitem(last=False)       # drop the oldest
            return value

        wrapper.stats = stats
        wrapper.keys = lambda: list(cache)
        return wrapper
    return decorator

@lru(2)
def square(n):
    return n * n

for n in (1, 2, 1, 3, 2):
    square(n)
print(square.stats, square.keys())              # {'hits': 1, 'misses': 4} [3, 2]


# 4. A retry decorator that asks the exception whether it is retryable
class TransientError(Exception):
    retryable = True


class FatalError(Exception):
    retryable = False


def retry(attempts):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for n in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if not getattr(e, "retryable", False) or n == attempts:
                        raise
        return wrapper
    return decorator

state = {"calls": 0}

@retry(3)
def flaky():
    state["calls"] += 1
    if state["calls"] < 3:
        raise TransientError("try again")
    return "ok"

print(flaky(), state["calls"])                  # ok 3

state["calls"] = 0

@retry(3)
def broken():
    state["calls"] += 1
    raise FatalError("stop")

try:
    broken()
except FatalError:
    print("fatal after", state["calls"], "call") # fatal after 1 call


# 5. How big is a data structure, really?
def deep_size(obj, seen=None):
    seen = set() if seen is None else seen
    if id(obj) in seen:
        return 0
    seen.add(id(obj))
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(deep_size(k, seen) + deep_size(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(deep_size(item, seen) for item in obj)
    return size

class Plain:
    def __init__(self):
        self.a, self.b = 1, 2

class Slotted:
    __slots__ = ("a", "b")

    def __init__(self):
        self.a, self.b = 1, 2

print(deep_size([Plain() for _ in range(100)]) > deep_size([Slotted() for _ in range(100)]))     # True
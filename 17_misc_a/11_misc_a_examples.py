import functools
import re
from collections import deque
from datetime import date, datetime, timedelta
from itertools import groupby, pairwise


# 1. Age in whole years, and days until a date
def age(born, on):
    return on.year - born.year - ((on.month, on.day) < (born.month, born.day))

print(age(date(1990, 5, 20), date(2026, 11, 10)),
      (date(2026, 12, 25) - date(2026, 11, 10)).days)           # 36 45


# 2. Working days (Monday to Friday) between two dates, both included
def working_days(start, end):
    days, d = 0, start
    while d <= end:
        if d.weekday() < 5:
            days += 1
        d += timedelta(days=1)
    return days

print(working_days(date(2026, 11, 2), date(2026, 11, 13)))      # 10


# 3. The time between two log timestamps
start = datetime.fromisoformat("2026-11-10T10:00:00")
end = datetime.fromisoformat("2026-11-10T10:45:30")
print(end - start, (end - start).total_seconds())               # 0:45:30 2730.0


# 4. A date range as a generator
def date_range(first, last):
    d = first
    while d <= last:
        yield d
        d += timedelta(days=1)

print([d.isoformat() for d in date_range(date(2026, 2, 27), date(2026, 3, 2))])
# ['2026-02-27', '2026-02-28', '2026-03-01', '2026-03-02']


# 5. A streaming moving average (a generator with a fixed-size window)
def moving_average(values, window):
    recent = deque(maxlen=window)
    for v in values:
        recent.append(v)
        yield round(sum(recent) / len(recent), 2)

print(list(moving_average([1, 2, 3, 4, 5], 3)))                 # [1.0, 1.5, 2.0, 3.0, 4.0]


# 6. Cut a byte stream into frames
def frames(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]

print(list(frames(b"abcdefg", 3)))                              # [b'abc', b'def', b'g']


# 7. Detect rising readings with pairwise
readings = [20, 21, 21, 23, 22]
print([b > a for a, b in pairwise(readings)])                   # [True, False, True, False]


# 8. A closure that remembers a limit
def make_threshold(limit):
    def above(value):
        return value > limit
    return above

above30 = make_threshold(30)
print([above30(x) for x in (25, 31, 30)])                       # [False, True, False]


# 9. Group log entries by level
entries = [("INFO", "a"), ("INFO", "b"), ("ERROR", "c")]
groups = {k: [msg for _, msg in g] for k, g in groupby(sorted(entries), key=lambda e: e[0])}
print(groups)                                                   # {'ERROR': ['c'], 'INFO': ['a', 'b']}


# 10. Recursion on a nested structure: the total size of a "folder"
tree = {"a.bin": 100, "src": {"m.py": 50, "u": {"x.py": 25}}}

def total_size(t):
    return sum(v if isinstance(v, int) else total_size(v) for v in t.values())

print(total_size(tree))                                         # 175


# 11. Memoized recursion: the number of paths through a grid (only right and down)
@functools.lru_cache(maxsize=None)
def paths(rows, cols):
    if rows == 1 or cols == 1:
        return 1
    return paths(rows - 1, cols) + paths(rows, cols - 1)

print(paths(3, 3), paths(18, 18))                               # 6 2333606220


# 12. A regex tokenizer for simple expressions
print(re.findall(r"\d+\.?\d*|[+\-*/()]", "3 + 4.5*(2 - 1)"))
# ['3', '+', '4.5', '*', '(', '2', '-', '1', ')']
# Module 17: Miscellaneous A, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Date & Time | Epoch | `time.time()` is seconds since 1970-01-01 UTC; `time.gmtime()`, `time.strftime()` |
| 01 | Date & Time | Durations | `time.perf_counter()` or `time.monotonic()`; never `time.time()` for timeouts |
| 01 | Date & Time | Classes | `date`, `time`, `datetime`, `timedelta`, `timezone` from `datetime` |
| 01 | Date & Time | Weekday | `d.weekday()` is 0 for Monday, `isoweekday()` is 1 for Monday |
| 01 | Date & Time | Arithmetic | `datetime + timedelta` gives a datetime; `date - date` gives a `timedelta` (`.days`, `.total_seconds()`) |
| 01 | Date & Time | Format | `strftime("%Y-%m-%d %H:%M")` turns a datetime into text |
| 01 | Date & Time | Parse | `strptime(text, format)` and `fromisoformat(text)` turn text into a datetime; bad text raises `ValueError` |
| 01 | Date & Time | Naive vs aware | Naive has no zone, aware has an offset; comparing the two raises `TypeError` |
| 01 | Date & Time | Zones | `timezone(timedelta(hours=5, minutes=30))`, `.astimezone(timezone.utc)`; `zoneinfo` for named zones |
| 01 | Date & Time | Best practice | Store UTC or an epoch number, show local time only for display, use ISO 8601 text |
| 01 | Date & Time | `calendar` | `isleap`, `monthrange(year, month)`, `weekday`, `month_name`, `day_name` |
| 02 | Maths | `math` | `pi`, `e`, `sqrt`, `pow`, `exp`, `log`, `log10`, `log2`, `floor`, `ceil`, `trunc`, `factorial`, `gcd`, `lcm`, `comb`, `perm`, `isqrt`, `prod` |
| 02 | Maths | Trigonometry | Works in radians: `radians()` and `degrees()` convert |
| 02 | Maths | Remainders | `%` follows the divisor's sign; `math.fmod` follows the dividend's sign (like C) |
| 02 | Maths | Accuracy | `math.fsum` for exact float sums; `math.isclose` to compare floats |
| 02 | Maths | Errors | `math.sqrt(-1)` and `math.log(0)` raise `ValueError: math domain error` |
| 02 | Maths | `cmath` | Maths for complex numbers: `cmath.sqrt(-1)` is `1j` |
| 02 | Maths | `random` | `seed` makes it repeatable; `choice`, `sample`, `shuffle` (in place), `randint`, `uniform`; not secure, use `secrets` |
| 02 | Maths | `statistics` | `mean`, `median`, `mode`, `stdev` (sample), `pstdev` (population), `pvariance` |
| 02 | Maths | Exact numbers | `Decimal` for money and decimal rounding, `Fraction` for exact ratios |
| 02 | Maths | Embedded style | `& 0xFF` wraps like a `uint8_t`; clamp for saturation; Q-format fixed point |
| 03 | Iterators | Terms | An iterable has `__iter__`; an iterator has `__next__` and remembers its place |
| 03 | Iterators | Protocol | `iter(x)` and `next(it)`; `StopIteration` ends it; `next(it, default)` avoids the error |
| 03 | Iterators | One pass | An iterator is used up after one loop; an iterable that returns a fresh iterator can be reused |
| 03 | Iterators | Lazy | `map`, `filter`, `zip`, `enumerate` and `range` produce items on demand |
| 03 | Iterators | `itertools` | `count`, `cycle`, `repeat`, `chain`, `islice`, `zip_longest`, `accumulate`, `groupby`, `product`, `permutations`, `combinations`, `takewhile`, `dropwhile`, `starmap`, `pairwise`, `tee` |
| 03 | Iterators | `groupby` | Groups only NEIGHBOURS: sort first |
| 03 | Iterators | Sentinel | `iter(func, sentinel)` calls `func` until it returns the sentinel (read a file in chunks) |
| 04 | Generators | `yield` | A function with `yield` returns a generator; it pauses and keeps its variables |
| 04 | Generators | Lazy start | Nothing runs until the first `next()` |
| 04 | Generators | Endless | `fib()` with `while True` plus `islice` |
| 04 | Generators | `yield from` | Delegates to another iterable and gives you its return value |
| 04 | Generators | `send()` | Pushes a value into the generator; prime it with `next()` first |
| 04 | Generators | `close()` / `throw()` | `close()` raises `GeneratorExit` inside; `throw(exc)` raises `exc` inside |
| 04 | Generators | Return | `return value` travels in `StopIteration.value` |
| 04 | Generators | State | `inspect.getgeneratorstate`: `GEN_CREATED`, `GEN_SUSPENDED`, `GEN_CLOSED` |
| 04 | Generators | Use for | Big or endless data, streams, pipelines; a generator is used once |
| 05 | Generator Expressions | Syntax | `(x * x for x in data)`: lazy, one pass, low memory |
| 05 | Generator Expressions | Calls | `sum(x for x in data)`: no extra parentheses needed for a sole argument |
| 05 | Generator Expressions | Short-circuit | `any` and `all` stop early, even on `itertools.count()` |
| 05 | Generator Expressions | First match | `next((x for x in data if cond), default)` |
| 05 | Generator Expressions | Limits | No `len()`, no indexing, one pass |
| 05 | Generator Expressions | Late evaluation | The condition and the source list are read when items are pulled |
| 06 | Lambda | Syntax | `lambda args: expression` (one expression, returns it) |
| 06 | Lambda | Use | `key=` functions, `map`, `filter`, `reduce`, callbacks, dispatch tables |
| 06 | Lambda | Limits | No statements or assignments; error messages say `<lambda>` |
| 06 | Lambda | Style | Do not write `f = lambda ...`; use `def` |
| 06 | Lambda | Loop trap | `[lambda: i for i in range(3)]` all return the last `i`; fix with `lambda i=i: i` |
| 06 | Lambda | Alternatives | `operator.itemgetter`, `operator.mul`, `functools.partial` |
| 07 | Closures | Idea | An inner function remembers variables of the enclosing function |
| 07 | Closures | Inspect | `f.__code__.co_freevars`, `f.__closure__[0].cell_contents` |
| 07 | Closures | `nonlocal` | Needed to REASSIGN an enclosing variable (not to change a list) |
| 07 | Closures | Uses | Function factories, hidden state, configured functions, memoization, event handlers |
| 07 | Closures | Loop trap | Same as lambda: capture with a default argument or a factory function |
| 07 | Closures | vs class | A closure for a little state, a class for more methods and attributes |
| 08 | Decorators | Meaning | `@d` above `def f` is `f = d(f)` |
| 08 | Decorators | Pattern | `def wrapper(*args, **kwargs)` plus `@functools.wraps(func)` keeps name and docstring |
| 08 | Decorators | With arguments | Three levels: factory, decorator, wrapper (`@repeat(3)`) |
| 08 | Decorators | Stacking | The decorator nearest the function is applied first |
| 08 | Decorators | Uses | Logging, timing, retry, validation, caching, registries |
| 08 | Decorators | Cache | `functools.lru_cache(maxsize=None)` and `functools.cache`; `cache_info()` |
| 08 | Decorators | Class decorators | A function that takes and returns a class; or a class with `__call__` |
| 08 | Decorators | `__wrapped__` | The original function, available when `wraps` is used |
| 09 | Recursion | Parts | A base case (stops) and a recursive case (smaller problem) |
| 09 | Recursion | Limit | About 1000 nested calls; `RecursionError`; `sys.getrecursionlimit()` |
| 09 | Recursion | No tail-call optimisation | Use a loop (or an explicit stack) for deep recursion |
| 09 | Recursion | Speed | `lru_cache` removes repeated work (`fib`) |
| 09 | Recursion | Good for | Trees, nested data, divide and conquer, backtracking (subsets, permutations, Hanoi) |
| 09 | Recursion | Mutual recursion | Two functions that call each other |
| 09 | Recursion | Embedded | Avoid recursion on microcontrollers (tiny stack) |
| 10 | Regex | Raw strings | Write patterns as `r"\d+"` |
| 10 | Regex | Functions | `search` (anywhere), `match` (start), `fullmatch` (all), `findall`, `finditer`, `sub`, `subn`, `split`, `compile` |
| 10 | Regex | Classes | `\d \w \s` and the opposites `\D \W \S`; `[abc]`, `[a-z]`, `[^0-9]` |
| 10 | Regex | Quantifiers | `*`, `+`, `?`, `{n}`, `{n,m}`; add `?` for lazy (`.+?`) |
| 10 | Regex | Anchors | `^`, `$`, `\b` |
| 10 | Regex | Groups | `(...)`, `(?P<name>...)`, `m.group()`, `m.groups()`, `m.groupdict()`, `m.span()` |
| 10 | Regex | `findall` | With groups it returns the groups (tuples), not the whole match |
| 10 | Regex | Look-around | `(?=...)` ahead, `(?<=...)` behind; `\1` back-reference |
| 10 | Regex | Flags | `re.IGNORECASE`, `re.MULTILINE`, `re.DOTALL`, `re.VERBOSE` |
| 10 | Regex | Replace | `re.sub(pattern, "\\2:\\1", text)` or with a function |
| 10 | Regex | Safety | `re.escape` for literal text; beware catastrophic backtracking; do not parse HTML or JSON with regex |
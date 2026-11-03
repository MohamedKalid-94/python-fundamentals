# Module 04: Functions & Modules, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Functions | `def` | Defines a function; `return` sends a value back |
| 01 | Functions | Parameter vs argument | The parameter is the name in `def`, the argument is the value you pass |
| 01 | Functions | No `return` | The function returns `None` |
| 01 | Functions | Several return values | Really one tuple: `return a, b` |
| 01 | Functions | Guard clauses | Return early to avoid deep nesting |
| 01 | Functions | Docstring | First string in the function, stored in `__doc__` |
| 01 | Functions | First-class objects | Functions can be stored, passed and returned; `f` is the object, `f()` is the call |
| 02 | Positional | Order | Position decides which parameter gets which value |
| 02 | Positional | Count | Too few or too many raises `TypeError` |
| 03 | Keyword | Call by name | `f(city="Pune", name="Ann")`; order is free |
| 03 | Keyword | Mixing | Positional arguments must come before keyword ones |
| 03 | Keyword | Errors | Same parameter twice or an unknown name raises `TypeError` |
| 04 | Default | Default value | `def f(x, y=2)`; defaults come after non-defaults |
| 04 | Default | When evaluated | Once, at definition time |
| 04 | Default | Mutable default trap | `items=[]` is shared between calls; use `None` and create inside |
| 05 | Keyword-only | `*` | Parameters after a bare `*` must be passed by name |
| 05 | Keyword-only | Required | A keyword-only parameter may have no default |
| 05 | Keyword-only | After `*args` | Parameters are automatically keyword-only |
| 06 | Positional-only | `/` | Parameters before `/` cannot be passed by name (3.8+) |
| 06 | Positional-only | Order of markers | `def f(a, /, b, *, c)` |
| 06 | Positional-only | Why | Names are not part of the API, so they can be renamed freely |
| 07 | Arbitrary | `*args` | Extra positional arguments collected into a tuple |
| 07 | Arbitrary | `**kwargs` | Extra keyword arguments collected into a dict |
| 07 | Arbitrary | Parameter order | positional, defaults, `*args`, keyword-only, `**kwargs` |
| 07 | Arbitrary | At the call | `f(*list)` and `f(**dict)` unpack into arguments |
| 07 | Arbitrary | Forwarding | `func(*args, **kwargs)` passes everything on |
| 08 | Scope | LEGB | Local, Enclosing, Global, Built-in |
| 08 | Scope | Assignment | Assigning inside a function makes the name local for the whole function |
| 08 | Scope | `UnboundLocalError` | Reading a name before assigning it locally |
| 08 | Scope | `global` / `nonlocal` | Rebind a module-level or enclosing variable; prefer return values |
| 08 | Scope | Blocks | `if`, `for`, `while` do not create a scope; only functions do |
| 08 | Scope | Passing objects | Python passes references: mutation is visible, rebinding is not |
| 08 | Scope | Shadowing | Never name variables `sum`, `list`, `max`, `str`, `id`, `type` |
| 09 | Annotations | Syntax | `def f(a: int, b: str = "x") -> bool:` |
| 09 | Annotations | Enforcement | Not enforced at run time |
| 09 | Annotations | Types | `list[int]`, `dict[str, int]`, `int \| None` (3.10+), `-> None` |
| 09 | Annotations | Used by | Editors, `mypy`, FastAPI and Pydantic |
| 09 | Annotations | Storage | Kept in `f.__annotations__` |
| 10 | Modules | What | A module is a `.py` file |
| 10 | Modules | Import styles | `import x`, `from x import y`, `import x as z`, `from x import y as z` |
| 10 | Modules | Avoid | `from x import *` |
| 10 | Modules | Runs once | A module is executed only on its first import |
| 10 | Modules | `__name__` | `"__main__"` when run directly, the module name when imported |
| 10 | Modules | Entry pattern | `if __name__ == "__main__": main()` |
| 10 | Modules | Search path | Script folder, installed packages, standard library (`sys.path`) |
| 10 | Modules | Naming | Never name your file `math.py`, `random.py`, `json.py` |
| 10 | Modules | `dir(module)` | Lists the names inside a module |
| 11 | Packing/Unpacking | Packing | `t = 1, 2, 3` builds a tuple |
| 11 | Packing/Unpacking | Unpacking | `a, b, c = t`; the counts must match or `ValueError` |
| 11 | Packing/Unpacking | Swap | `a, b = b, a` |
| 11 | Packing/Unpacking | Star | `first, *rest = items` and `head, *mid, tail = items` |
| 11 | Packing/Unpacking | Ignore | `_` for values you do not need |
| 11 | Packing/Unpacking | Merge | `[*a, *b]`, `{**d1, **d2}` (later keys win), `d1 \| d2` (3.9+) |
| 12 | Built-ins | Numbers | `abs`, `round`, `pow`, `divmod`, `min`, `max`, `sum` |
| 12 | Built-ins | Iteration | `sorted`, `reversed`, `enumerate`, `zip`, `map`, `filter` |
| 12 | Built-ins | Key functions | `sorted(x, key=len)` and `max(x, key=len)` |
| 12 | Built-ins | Lazy results | `map`, `filter`, `zip`, `reversed` return iterators; wrap in `list()` to see them |
| 12 | Built-ins | Truth tests | `any([])` is `False`, `all([])` is `True` |
| 12 | Built-ins | Safe `next` | `next(it, default)` avoids `StopIteration` |
| 12 | Built-ins | Inspection | `type`, `isinstance`, `callable`, `hasattr`, `getattr`, `dir` |
| 12 | Built-ins | `eval` | Never use on untrusted input |
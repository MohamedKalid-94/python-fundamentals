# Module 07: Tuples, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Tuples | What | Ordered, immutable, allows duplicates and mixed types |
| 01 | Tuples | Creation | `(1, 2)`, `1, 2` (commas make it), `tuple(iterable)`, `()` is empty |
| 01 | Tuples | Single item | `(5,)` is a tuple; `(5)` is just an int |
| 01 | Tuples | Immutable | `t[0] = 9` raises `TypeError` |
| 01 | Tuples | Hashable | Usable as a dict key or set member only if every item is hashable |
| 01 | Tuples | Comparison | Item by item; `(1, 2) == [1, 2]` is `False` |
| 01 | Tuples | Operators | `+` and `*` build new tuples; `in` tests membership |
| 01 | Tuples | Why | Fixed records, constants, dictionary keys, multiple return values |
| 02 | Access | Indexing | `t[0]`, `t[-1]`; out of range raises `IndexError` |
| 02 | Access | Slicing | Returns a new tuple and never raises `IndexError` |
| 02 | Access | Nested | `t[1][0]` |
| 02 | Access | Mutable inside | A list inside a tuple can still change in place |
| 02 | Access | Methods | `index(x)` (raises `ValueError` if missing) and `count(x)` |
| 03 | Update | No change | Build a new tuple instead |
| 03 | Update | Via list | `list(t)`, change it, then `tuple(items)` |
| 03 | Update | Concatenation | `t = t + (4,)` or `t += (4,)` makes a new object |
| 03 | Update | Slicing | Insert or remove with `t[:i] + (x,) + t[i:]` |
| 03 | Update | `del` | `del t[0]` is an error; `del t` removes only the name |
| 03 | Update | Quirk | `t[0] += [5]` with a list inside raises `TypeError` yet still extends the list |
| 03 | Update | `sorted()` | Returns a list; wrap with `tuple()` |
| 04 | Unpack | Basic | `x, y = (1, 2)`; the counts must match or `ValueError` |
| 04 | Unpack | Star | `first, *rest = t`; the starred part is a list |
| 04 | Unpack | Ignore | `_` for values you do not need |
| 04 | Unpack | Nested | `name, (r, g, b) = ("red", (255, 0, 0))` |
| 04 | Unpack | In calls | `f(*t)` passes the items as arguments |
| 04 | Unpack | In loops | `for name, age in pairs`, `for i, (a, b) in enumerate(...)` |
| 04 | Unpack | Any iterable | Strings and ranges unpack too |
| 05 | Loop | Items | `for x in t` |
| 05 | Loop | Index + item | `enumerate(t, start=1)` |
| 05 | Loop | Together | `zip(a, b)` |
| 05 | Loop | Views | `reversed(t)` and `sorted(t)` leave the tuple unchanged |
| 05 | Loop | Sorting tuples | Compared item by item, so `sorted(points)` sorts by x then y |
| 06 | Join | `+` | New tuple; both sides must be tuples |
| 06 | Join | `+=` | Also creates a new tuple |
| 06 | Join | Unpack | `(*a, *b)` |
| 06 | Join | `chain` | `tuple(chain(a, b))` |
| 06 | Join | Unique | `tuple(dict.fromkeys(a + b))` keeps the order |
| 06 | Join | Type rule | `(1,) + [2]` raises `TypeError` |
| 07 | Methods | Only two | `count` and `index` |
| 07 | Methods | Built-ins | `len`, `min`, `max`, `sum`, `sorted`, `reversed`, `any`, `all`, `enumerate`, `zip` |
| 07 | Methods | Choose | List for a changing collection, tuple for a fixed record |
| 08 | Namedtuple | Create | `namedtuple("Point", ["x", "y"])` or `"x y"` |
| 08 | Namedtuple | Access | By name (`p.x`) or by index (`p[0]`); unpacking still works |
| 08 | Namedtuple | Still a tuple | Immutable; `isinstance(p, tuple)` is `True` |
| 08 | Namedtuple | Helpers | `_replace()`, `_asdict()`, `_fields`, `_make()` |
| 08 | Namedtuple | Defaults | `defaults=[0]` apply to the rightmost fields |
| 08 | Namedtuple | Class form | `class E(NamedTuple): name: str` with type hints |
| 08 | Namedtuple | Choose | Read-only record: namedtuple; changing record: dataclass (Module 13) |
| 09 | Exercises | Multiple returns | `return a, b` and unpack the result |
| 09 | Exercises | Keys | Coordinates `(x, y)` work as dict keys |
| 09 | Exercises | Zip / unzip | `zip(a, b)` pairs, `zip(*pairs)` splits back |
| 09 | Exercises | Versions | Tuples compare item by item: `(3, 12) > (3, 9)` |

# Module 06: Lists, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Lists | What | Ordered, mutable, allows duplicates and mixed types |
| 01 | Lists | Creation | `[]`, `list()`, `list("abc")`, `list(range(5))` |
| 01 | Lists | Order | `[1, 2] != [2, 1]` |
| 01 | Lists | Nested | `matrix[row][col]` |
| 01 | Lists | Repetition trap | `[[0] * 2] * 2` repeats the SAME inner list; use a comprehension |
| 01 | Lists | Truthiness | `[]` is falsy, `[0]` is truthy |
| 02 | Access | Indexing | `lst[0]`, `lst[-1]`; out of range raises `IndexError` |
| 02 | Access | Slicing | `lst[a:b:c]` returns a new list and never raises `IndexError` |
| 02 | Access | Unpacking | `first, *rest = lst` |
| 02 | Access | Searching | `index(x)` raises `ValueError` if missing; `count(x)`; `x in lst` |
| 03 | Change | Single item | `lst[i] = v` |
| 03 | Change | Slice assignment | `lst[a:b] = [...]` can shrink, grow, insert (`lst[i:i] = ...`) and delete (`= []`) |
| 03 | Change | Extended slice | `lst[::2] = [...]` needs exactly the same length |
| 03 | Change | Loop trap | `for v in lst: v *= 2` changes nothing; assign through the index |
| 03 | Change | Aliases | Every name for the same list sees the change |
| 04 | Add | `append(x)` | Adds ONE item (a list becomes a nested item) |
| 04 | Add | `extend(it)` | Adds EACH item of the iterable |
| 04 | Add | `insert(i, x)` | `insert(-1, x)` goes before the last item; a big index goes to the end |
| 04 | Add | `+` vs `+=` | `+` builds a new list; `+=` extends in place |
| 04 | Add | Return value | These methods return `None`; never write `x = lst.append(1)` |
| 04 | Add | Speed | `append` is fast, `insert(0, x)` is slow on big lists |
| 05 | Remove | `remove(x)` | First match by value; `ValueError` if missing |
| 05 | Remove | `pop(i)` | Removes and returns; the last item by default |
| 05 | Remove | `del` | By index or slice: `del lst[1:3]`, `del lst[:]` |
| 05 | Remove | `clear()` | Empties the list |
| 05 | Remove | All occurrences | `lst = [n for n in lst if n != x]` |
| 05 | Remove | Loop trap | Never remove while looping; loop over `lst[:]` |
| 05 | Remove | Stack / queue | `append` + `pop()` is a stack; `pop(0)` is a slow queue |
| 06 | Loop | Items | `for x in lst` |
| 06 | Loop | Index + item | `for i, x in enumerate(lst, start=1)` |
| 06 | Loop | Two lists | `zip(a, b)` stops at the shorter one |
| 06 | Loop | Views | `reversed(lst)` and `sorted(lst)` leave the original unchanged |
| 06 | Loop | Rule | Do not add or remove items of the list you are looping over |
| 07 | Comprehension | Syntax | `[expr for x in it if cond]` |
| 07 | Comprehension | if-else | `[a if c else b for x in it]` (before `for`); a filter-only `if` goes after |
| 07 | Comprehension | Nested | `[v for row in m for v in row]` flattens; read left to right |
| 07 | Comprehension | Scope | The loop variable does not leak out |
| 07 | Comprehension | Others | `{...}` for sets, `{k: v ...}` for dicts, `(...)` for generators |
| 07 | Comprehension | Rule | Switch to a loop when it needs more than one condition or two loops |
| 08 | Sort | `sort()` | In place, returns `None` |
| 08 | Sort | `sorted()` | Returns a new list, works on any iterable |
| 08 | Sort | `key=` | `key=len`, `key=str.lower`, `key=int`, `key=lambda s: s[1]` |
| 08 | Sort | Multiple keys | Use a tuple: `key=lambda s: (-s[1], s[0])` |
| 08 | Sort | `reverse` | `reverse=True` sorts descending; `.reverse()` only flips the order |
| 08 | Sort | Stable | Equal items keep their original order |
| 08 | Sort | Mixed types | `sorted([3, "a"])` raises `TypeError` |
| 09 | Copy | Assignment | `b = a` does NOT copy |
| 09 | Copy | Shallow copy | `a.copy()`, `a[:]`, `list(a)`, `copy.copy(a)` |
| 09 | Copy | Shallow trap | Inner lists are still shared |
| 09 | Copy | Deep copy | `copy.deepcopy(a)` copies everything inside |
| 09 | Copy | In-place replace | `lst[:] = new_items` keeps the same list object |
| 10 | Join | `+` | New list |
| 10 | Join | `extend` / `+=` | In place |
| 10 | Join | Unpack | `[*a, *b]` |
| 10 | Join | `chain` | `itertools.chain(a, b)` for many or large lists |
| 10 | Join | Unique | `list(dict.fromkeys(a + b))` keeps the order |
| 10 | Join | Type rule | `+` needs two lists: `[1] + (2,)` raises `TypeError` |
| 10 | Join | Strings | `", ".join(map(str, nums))` |
| 11 | Methods | The 11 methods | `append`, `clear`, `copy`, `count`, `extend`, `index`, `insert`, `pop`, `remove`, `reverse`, `sort` |
| 11 | Methods | Return `None` | `append`, `extend`, `insert`, `remove`, `clear`, `sort`, `reverse` |
| 11 | Methods | Built-ins | `len`, `min`, `max`, `sum`, `sorted`, `reversed`, `any`, `all`, `enumerate`, `zip` |
| 12 | Exercises | Two pointers | `left`, `right = 0, len(x) - 1` and swap while `left < right` |
| 12 | Exercises | Chunking | `[x[i:i + n] for i in range(0, len(x), n)]` |
| 12 | Exercises | Stack | `append` to push, `pop()` to pop; balanced brackets |
| 12 | Exercises | Merge sorted | Two indexes, then `extend` the leftovers |
| 12 | Exercises | Rotation | `x[k:] + x[:k]` with `k %= len(x)` |
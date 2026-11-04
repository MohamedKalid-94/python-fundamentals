# Module 09: Dictionaries, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Dictionaries | What | Maps unique, hashable keys to any values; mutable; keeps insertion order (3.7+) |
| 01 | Dictionaries | Creation | `{k: v}`, `dict(a=1)`, `dict(pairs)`, `dict(zip(keys, values))`, `dict.fromkeys(keys, v)`, `{}` is empty |
| 01 | Dictionaries | Duplicate keys | The last value wins |
| 01 | Dictionaries | Equal keys | `1`, `1.0` and `True` are the same key |
| 01 | Dictionaries | Keys | Must be hashable: numbers, strings, tuples of those; never lists, sets or dicts |
| 01 | Dictionaries | Equality | Ignores order: `{"a": 1, "b": 2} == {"b": 2, "a": 1}` |
| 01 | Dictionaries | `in` | Tests KEYS; use `.values()` for values |
| 01 | Dictionaries | Speed | Lookup by key is O(1) on average |
| 02 | Access | `d[k]` | Raises `KeyError` if missing; keys are case-sensitive |
| 02 | Access | `get(k, default)` | No error; returns the default (`None` if none given) |
| 02 | Access | `setdefault(k, v)` | Returns the value and ADDS the key if missing |
| 02 | Access | `get` vs `in` | `get` cannot tell a missing key from a stored `None` |
| 02 | Access | Position | No index: use `list(d)`, `list(d.values())` or `next(iter(d))` |
| 02 | Access | Best by value | `max(d, key=d.get)` |
| 02 | Access | Nested safely | `d.get("a", {}).get("b")` |
| 03 | Change | Assign | `d[k] = v` overwrites and keeps the key's position |
| 03 | Change | `update` | Takes a dict, keywords or pairs |
| 03 | Change | In a loop | Changing values while looping is safe |
| 03 | Change | Rename a key | `d["new"] = d.pop("old")` moves it to the end; rebuild to keep the position |
| 03 | Change | Counting | `d[k] = d.get(k, 0) + 1` |
| 03 | Change | `\|` | Builds a new dict; the right side wins (3.9+) |
| 04 | Add | New key | `d[k] = v` adds it at the END |
| 04 | Add | Many | `update`, `\|=`, `{**a, **b}`, `a \| b` |
| 04 | Add | Only if missing | `setdefault`, or `if k not in d` |
| 04 | Add | Grouping | `d.setdefault(k, []).append(x)` or `defaultdict(list)` |
| 04 | Add | `defaultdict` | Reading a missing key creates it |
| 04 | Add | Hashable | `d[[1]] = 1` raises `TypeError` |
| 05 | Remove | `pop(k)` | Removes and returns the value; `KeyError` if missing |
| 05 | Remove | `pop(k, default)` | Safe version, no error |
| 05 | Remove | `popitem()` | Removes the LAST pair (LIFO) |
| 05 | Remove | `del d[k]` | `KeyError` if missing |
| 05 | Remove | `clear()` | Empties the dict |
| 05 | Remove | By condition | `{k: v for k, v in d.items() if cond}` |
| 05 | Remove | Loop trap | Deleting keys while looping raises `RuntimeError`; loop over `list(d)` |
| 06 | Views | Three views | `keys()`, `values()`, `items()` |
| 06 | Views | Live | They follow later changes to the dict |
| 06 | Views | No index | `d.keys()[0]` raises `TypeError`; use `list(...)` |
| 06 | Views | Set-like | `keys()` and `items()` support `&`, `\|`, `-`, `^`; `values()` does not |
| 06 | Views | Snapshot | `list(d.items())` is a copy that does not change |
| 06 | Views | Reverse | `reversed(d)` and `reversed(d.items())` (3.8+) |
| 07 | Loop | Keys | `for k in d` |
| 07 | Loop | Values | `for v in d.values()` |
| 07 | Loop | Both | `for k, v in d.items()` |
| 07 | Loop | Counter | `enumerate(d.items(), start=1)` |
| 07 | Loop | Sorted | `sorted(d)` and `sorted(d.items(), key=lambda kv: kv[1])` |
| 07 | Loop | Rule | Never add or remove keys while looping |
| 08 | Copy | Assignment | `b = a` shares the dict |
| 08 | Copy | Shallow | `a.copy()`, `dict(a)`, `{**a}`, `copy.copy(a)` |
| 08 | Copy | Shallow trap | Nested lists and dicts are still shared |
| 08 | Copy | Deep | `copy.deepcopy(a)` |
| 08 | Copy | Config pattern | `{**base, **override}` |
| 09 | Nested | Access | `d["a"]["b"]["c"]`; any missing level raises `KeyError` |
| 09 | Nested | Safe | `get` chains, or a `deep_get(data, path, default)` helper |
| 09 | Nested | Grouping | `setdefault(key, []).append(item)` builds a dict of lists |
| 09 | Nested | Trap | Reusing one inner dict for several keys shares it |
| 09 | Nested | JSON | `json.dumps(d, indent=2)` and `json.loads(text)` |
| 10 | Methods | The 11 methods | `clear`, `copy`, `fromkeys`, `get`, `items`, `keys`, `pop`, `popitem`, `setdefault`, `update`, `values` |
| 10 | Methods | `fromkeys` trap | `dict.fromkeys(keys, [])` shares one list |
| 10 | Methods | Built-ins | `len`, `sorted(d)`, `min`, `max`, `sum(d.values())`, `any`, `all`, `enumerate` |
| 10 | Methods | Sort by value | `dict(sorted(d.items(), key=lambda kv: kv[1]))` |
| 11 | Exercises | Counting | `d[k] = d.get(k, 0) + 1`, or `Counter` |
| 11 | Exercises | Two sum | Store `value: index` in a dict while looping |
| 11 | Exercises | Grouping | Sorted letters as a key groups anagrams |
| 11 | Exercises | Lookup table | `CODES.get(code, "UNKNOWN")` |
| 11 | Exercises | Dispatch table | `ops = {"add": add}` then `ops["add"](2, 3)` |
| 11 | Exercises | Memoization | A dict as a cache turns slow repeated work into lookups |

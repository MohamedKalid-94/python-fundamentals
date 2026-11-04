# Module 08: Sets, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Sets | What | Unordered, mutable, unique and hashable items |
| 01 | Sets | Creation | `{1, 2}`, `set(iterable)`; `{}` is an empty DICT, so use `set()` |
| 01 | Sets | Duplicates | Removed automatically; `{1, 1.0, True}` is `{1}` |
| 01 | Sets | No order | No indexing or slicing; printing order is not defined |
| 01 | Sets | Hashable | Items must be immutable: numbers, strings, tuples; not lists or dicts |
| 01 | Sets | `frozenset` | Immutable set; usable as a dict key or set member |
| 01 | Sets | Speed | `x in s` is very fast (hashing) compared with a list |
| 01 | Sets | Equality | `{1, 2} == {2, 1}` is `True` |
| 02 | Access | No index | `s[0]` raises `TypeError` |
| 02 | Access | Ways | Loop, `in`, `sorted(s)`, `min`, `max`, `sum`, `next(iter(s))` for any one item |
| 03 | Add | `add(x)` | One item as it is; no effect if already present |
| 03 | Add | `update(*its)` | Every item of the iterables; `|=` does the same |
| 03 | Add | `add` vs `update` | `add("abc")` adds one string; `update("abc")` adds 3 characters |
| 03 | Add | Return value | `None` |
| 04 | Remove | `remove(x)` | `KeyError` if missing |
| 04 | Remove | `discard(x)` | No error if missing |
| 04 | Remove | `pop()` | Removes an arbitrary item; `KeyError` if empty |
| 04 | Remove | Bulk | `-=`, `difference_update`, `intersection_update`, `clear()` |
| 04 | Remove | By condition | `s = {n for n in s if cond}` |
| 04 | Remove | Loop trap | Changing a set while looping raises `RuntimeError`; loop over `list(s)` |
| 05 | Loop | Order | Arbitrary; use `sorted(s)` when order matters |
| 05 | Loop | Tools | `for`, `enumerate(sorted(s))`, `while s: s.pop()` |
| 05 | Loop | Lookup | `if user in allowed_set` |
| 06 | Join | Union | `a \| b`, `a.union(b, c)`, `{*a, *b}` |
| 06 | Join | In place | `update()`, `\|=`, `intersection_update()`, `symmetric_difference_update()` |
| 06 | Join | No `+` | Sets do not support `+` |
| 06 | Join | Operators vs methods | `\|` needs two sets; `union()` accepts any iterable |
| 06 | Join | Type | The left operand's type wins (`frozenset \| set` gives `frozenset`) |
| 07 | Copy | Assignment | `b = a` shares the set |
| 07 | Copy | Copies | `a.copy()`, `set(a)`, `{*a}`, `copy.copy(a)` |
| 07 | Copy | Shallow is enough | Items are hashable, so `deepcopy` is rarely needed |
| 07 | Copy | In place | `clear()` then `update()` keeps the same object |
| 08 | Operators | Four operations | `\|` union, `&` intersection, `-` difference, `^` symmetric difference |
| 08 | Operators | Comparisons | `<=` subset, `<` proper subset, `>=` superset, `>` proper superset |
| 08 | Operators | Equal sets | `{1, 2} <= {1, 2}` is `True`; `<` is `False` |
| 08 | Operators | Precedence | `&` then `^` then `\|` |
| 08 | Operators | Types | Both sides must be sets |
| 08 | Operators | Similarity | `len(a & b) / len(a \| b)` |
| 09 | Methods | Return a new set | `union`, `intersection`, `difference`, `symmetric_difference`, `copy` |
| 09 | Methods | Return a bool | `isdisjoint`, `issubset`, `issuperset` |
| 09 | Methods | Change in place | `add`, `update`, `remove`, `discard`, `pop`, `clear`, `*_update` |
| 09 | Methods | Arguments | Methods accept any iterable and several arguments |
| 09 | Methods | Count | 17 methods in total |
| 10 | Exercises | Duplicates | `len(set(x)) != len(x)` |
| 10 | Exercises | Order | `list(dict.fromkeys(x))` removes duplicates and keeps the order |
| 10 | Exercises | Seen set | Loop with `if x in seen: ...; seen.add(x)` |
| 10 | Exercises | Subset test | `required <= granted` |
| 10 | Exercises | Anagram | A set forgets the counts; compare `sorted()` instead |
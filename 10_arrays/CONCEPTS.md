# Module 10: Arrays, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Arrays | What | `array.array`: a typed, packed, resizable array of numbers; import with `from array import array` |
| 01 | Arrays | Create | `array("i", [1, 2, 3])`, `array("d")`, `array("B", range(5))`, `array("B", b"AB")` |
| 01 | Arrays | Typecodes | `b B h H i I l L q Q f d` (the C types); `typecode` and `itemsize` show them |
| 01 | Arrays | Sizes | `b`/`B` 1 byte, `h`/`H` 2, `i`/`I` 4 (typical), `q`/`Q` 8, `f` 4, `d` 8 |
| 01 | Arrays | Enforced | A wrong type raises `TypeError`; a value out of range raises `OverflowError` (no silent wrap-around) |
| 01 | Arrays | vs list | A list holds any objects; an array holds one number type and uses far less memory |
| 01 | Arrays | Equality | `array == array` compares items; an array never equals a list |
| 01 | Arrays | Choose | list for general data, `array` for compact numbers and buffers, `bytearray` for bytes, NumPy for maths |
| 02 | Access | Index | `a[0]`, `a[-1]`; out of range raises `IndexError` |
| 02 | Access | Slice | Returns a new array of the same type; never raises `IndexError` |
| 02 | Access | Search | `index(x)`, `count(x)`, `x in a` |
| 02 | Access | Change | `a[i] = v`; a slice must be replaced by an ARRAY of the same type |
| 02 | Access | `buffer_info()` | `(address, length)`; bytes used = length * itemsize |
| 03 | Add | `append(x)` | One item at the end |
| 03 | Add | `extend(it)` | Every item of an array or iterable |
| 03 | Add | `insert(i, x)` | At a position; a big index goes to the end |
| 03 | Add | `fromlist(list)` | Add the items of a list |
| 03 | Add | `+` vs `+=` | `+` builds a new array; both sides need the same typecode |
| 03 | Add | Speed | `append` is fast; `insert(0, x)` shifts everything |
| 04 | Remove | `remove(x)` | First match; `ValueError` if missing |
| 04 | Remove | `pop(i)` | Removes and returns; `IndexError` if empty or out of range |
| 04 | Remove | `del a[i]`, `del a[a:b]` | Remove by index or slice |
| 04 | Remove | No `clear()` | Use `del a[:]` |
| 04 | Remove | All occurrences | `a[:] = array(a.typecode, [v for v in a if v != x])` |
| 04 | Remove | Loop trap | Never remove while looping; loop over `a[:]` |
| 05 | Loop | Items | `for v in a`; indexes with `range(len(a))`; `enumerate`, `zip` |
| 05 | Loop | Change in place | `a[i] *= 2` through the index |
| 05 | Loop | Bytes | Items of a `'B'` array are ints; use `chr()` to see characters |
| 05 | Loop | Convert | `[round(v * 3.3 / 1023, 2) for v in adc]` gives a list of volts |
| 06 | Copy | Assignment | `b = a` shares the array |
| 06 | Copy | Copies | `a[:]`, `copy.copy(a)`, `array(a.typecode, a)`, `a.tolist()` for a list |
| 06 | Copy | No shallow trap | Items are plain numbers, so every copy is fully independent |
| 06 | Copy | In place | `a[:] = other_array` keeps the same object |
| 07 | Reverse | New array | `a[::-1]` |
| 07 | Reverse | In place | `a.reverse()` or two pointers with a swap |
| 07 | Reverse | Iterator | `reversed(a)` |
| 07 | Reverse | Part | `a[i:j] = a[i:j][::-1]` |
| 07 | Reverse | vs `byteswap()` | `reverse()` flips the item order; `byteswap()` flips the bytes inside each item |
| 08 | Sort | No `sort()` | Arrays have no sort method |
| 08 | Sort | Way | `array(a.typecode, sorted(a))` or `a[:] = array(...)` |
| 08 | Sort | `sorted()` | Always returns a list |
| 08 | Sort | By hand | Insertion sort with a shifting loop, as in C |
| 08 | Sort | `bisect` | `bisect_left` and `insort` work on sorted arrays |
| 09 | Join | `+` | New array; same typecode needed (else `TypeError`) |
| 09 | Join | In place | `extend`, `+=`, `fromlist` |
| 09 | Join | Many | `array("i", chain(a, b))` |
| 09 | Join | Raw data | `a.tobytes() + b.tobytes()` |
| 09 | Join | To string | `" ".join(map(str, a))` |
| 10 | Methods | Count | `append, buffer_info, byteswap, count, extend, frombytes, fromfile, fromlist, fromunicode, index, insert, pop, remove, reverse, tobytes, tofile, tolist, tounicode` |
| 10 | Methods | Raw memory | `tobytes()` and `frombytes()` like `memcpy` to and from a buffer |
| 10 | Methods | Binary files | `tofile(f)` and `fromfile(f, n)` with files opened in `"wb"` and `"rb"` |
| 10 | Methods | Endianness | `byteswap()`, `int.to_bytes(n, "big")`, `int.from_bytes(b, "little")` |
| 10 | Methods | `'u'` typecode | Deprecated; use `str`, `bytes` or `bytearray` |
| 11 | Exercises | Checksums | `sum(p) & 0xFF`, XOR loop, `(-sum(p)) & 0xFF` |
| 11 | Exercises | Flat 2D array | Index `row * cols + col` |
| 11 | Exercises | Ring buffer | `buf[head] = v; head = (head + 1) % size` |
| 11 | Exercises | Prefix sums | Range sum = `prefix[j] - prefix[i]` |
| 11 | Exercises | Counting table | `counts[digit] += 1` |
| 11 | Exercises | 16-bit split | `value >> 8` and `value & 0xFF`; rebuild with `(high << 8) \| low` |
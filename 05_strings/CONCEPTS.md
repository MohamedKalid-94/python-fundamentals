# Module 05: Strings, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Strings | Creation | `'..'`, `".."`, and `"""..."""` for multi-line; use the other quote kind inside |
| 01 | Strings | Sequence | `len(s)`, indexing `s[0]`, `s[-1]`, looping with `for ch in s` |
| 01 | Strings | Index errors | `s[len(s)]` raises `IndexError` |
| 01 | Strings | Immutable | `s[0] = "J"` raises `TypeError`; every change creates a new string |
| 01 | Strings | Empty string | Falsy, with `len` 0 |
| 01 | Strings | `==` | Compares content (no `strcmp` needed) |
| 01 | Strings | `str()` / `repr()` | `str` is for reading, `repr` shows the exact value with escapes |
| 02 | Slicing | Syntax | `s[start:stop:step]`; the stop is excluded |
| 02 | Slicing | Defaults | Missing start is 0, missing stop is the end, missing step is 1 |
| 02 | Slicing | Negatives | `s[-3:]` is the last 3 characters; `s[1:-1]` removes both ends |
| 02 | Slicing | Reverse | `s[::-1]` |
| 02 | Slicing | Safe | Out-of-range slices give shorter or empty strings, never `IndexError` |
| 02 | Slicing | Rejoin | `s[:n] + s[n:] == s` |
| 02 | Slicing | `slice()` | A named, reusable slice object |
| 03 | Modify | Immutability | Methods return a new string; assign the result |
| 03 | Modify | Case | `upper`, `lower`, `title`, `capitalize`, `swapcase` |
| 03 | Modify | Strip | `strip`, `lstrip`, `rstrip`, or `strip("x")` for chosen characters |
| 03 | Modify | `replace` | `replace(old, new, count)`; an empty new string deletes |
| 03 | Modify | Rebuild | Change one character with `"J" + s[1:]` or through `list()` and `"".join()` |
| 03 | Modify | Padding | `center`, `ljust`, `rjust`, `zfill` |
| 03 | Modify | Translate | `str.maketrans()` plus `translate()` |
| 04 | Concatenation | `+` | Both sides must be strings: `"Age: " + str(5)` |
| 04 | Concatenation | `*` | Repeats: `"-" * 20` |
| 04 | Concatenation | `join` | Best for many pieces; items must already be strings |
| 04 | Concatenation | Loops | Collect in a list, then `"".join(parts)` once |
| 04 | Concatenation | Adjacent literals | `"a" "b"` joins at compile time (literals only) |
| 04 | Concatenation | Long text | Wrap adjacent literals in parentheses |
| 05 | Formatting | f-string | `f"{x}"`; the default choice (3.6+) |
| 05 | Formatting | Debug | `f"{x=}"` prints the name and the value |
| 05 | Formatting | Spec | `{value:[fill][align][sign][0][width][,][.precision][type]}` |
| 05 | Formatting | Common | `.2f`, `05d`, `>8`, `<8`, `^8`, `,`, `.1%`, `b`, `x`, `e` |
| 05 | Formatting | Dynamic | `{x:>{width}}` takes the width from a variable |
| 05 | Formatting | Braces | `{{` and `}}` print literal braces |
| 05 | Formatting | `.format()` | Positional `{0}`, named `{name}`; useful for stored templates |
| 05 | Formatting | `%` | Old style (`%s`, `%d`, `%.2f`, `%%`); seen in old code and logging |
| 06 | Escapes | Common | `\n`, `\t`, `\\`, `\'`, `\"` |
| 06 | Escapes | Codes | `\xhh`, `\ooo`, `\uXXXX`, `\UXXXXXXXX`, `\N{name}` |
| 06 | Escapes | Length | An escape sequence is one character: `len("\n")` is 1 |
| 06 | Escapes | Raw strings | `r"C:\new"` keeps backslashes; it cannot end in a single `\` |
| 06 | Escapes | Use | Raw strings for regex patterns and Windows paths |
| 06 | Escapes | Line join | A `\` at the end of a line continues the string |
| 07 | Methods | Search | `find` returns -1 when missing; `index` raises `ValueError` |
| 07 | Methods | Count | `count("an")` counts non-overlapping matches |
| 07 | Methods | Tests | `isdigit` rejects `""`, `-5` and `3.5`; `isdecimal` and `isnumeric` differ for special digits |
| 07 | Methods | Split | `split()` handles any whitespace; `split(",", 1)` limits splits |
| 07 | Methods | `partition` | Always returns 3 parts: before, separator, after |
| 07 | Methods | `splitlines` | Handles `\n` and `\r\n` |
| 07 | Methods | `casefold` | Use it for case-insensitive comparison |
| 07 | Methods | Prefix and suffix | `removeprefix`, `removesuffix` (3.9+) |
| 07 | Methods | Encoding | `encode("utf-8")` gives `bytes`; `decode` returns `str` |
| 07 | Methods | Chaining | `s.strip().lower().replace(" ", "_")` |
| 08 | Exercises | Patterns | Clean first (`isalnum`, `lower`), then compare |
| 08 | Exercises | Accumulate | Build the result in a variable or list, then return or join |
| 08 | Exercises | Parsing | `split(";")` then `split("=")` turns text into key/value data |
| 08 | Exercises | Caesar | `chr((ord(ch) - base + shift) % 26 + base)` |
| 08 | Exercises | Bytes | Iterating `bytes` gives integers; format them with `:02x` |
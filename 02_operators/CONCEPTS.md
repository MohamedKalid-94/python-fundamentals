# Module 02: Operators, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Arithmetic | `/` | Always returns a float, even `10 / 2` gives `5.0` |
| 01 | Arithmetic | `//` | Floors toward negative infinity: `-17 // 5` is `-4` |
| 01 | Arithmetic | `%` | The sign follows the divisor: `-17 % 5` is `3` |
| 01 | Arithmetic | Identity | `a == (a // b) * b + a % b` always holds |
| 01 | Arithmetic | `divmod(a, b)` | Returns `(quotient, remainder)` in one call |
| 01 | Arithmetic | `**` | Power; `9 ** 0.5` is a square root; `2 ** 100` never overflows |
| 01 | Arithmetic | Sequences | `"ab" * 3`, `[1] + [2]`, `[0] * 4` work |
| 01 | Arithmetic | Zero division | `1 / 0` raises `ZeroDivisionError` |
| 02 | Comparison | Result | Always a `bool` |
| 02 | Comparison | Chaining | `1 < x < 10` means `(1 < x) and (x < 10)` |
| 02 | Comparison | Numbers | `5 == 5.0` and `1 == True` are `True` |
| 02 | Comparison | Strings | Compared by code point: `"a" < "B"` is `False` |
| 02 | Comparison | Sequences | Compared element by element; different types are not equal |
| 02 | Comparison | Mixed types | `5 < "5"` raises `TypeError` |
| 03 | Assignment | Augmented | `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`, `&=`, `\|=`, `^=`, `<<=`, `>>=`, `@=` |
| 03 | Assignment | Mutable `+=` | Changes the object in place (same `id`), so aliases see it |
| 03 | Assignment | Immutable `+=` | Creates a new object |
| 03 | Assignment | `x = x + [3]` | Builds a new list; `x += [3]` modifies the existing one |
| 03 | Assignment | No `++` / `--` | `++n` is just `+(+n)`; use `n += 1` |
| 03 | Assignment | Multiple | `a = b = 0` and `p, q = 1, 2` both work |
| 04 | Logical | Words | Uses `and`, `or`, `not`, not `&&`, `\|\|`, `!` |
| 04 | Logical | Return value | `and` / `or` return an operand, not just `True` / `False` |
| 04 | Logical | `and` | Returns the first falsy operand, or the last one |
| 04 | Logical | `or` | Returns the first truthy operand, or the last one |
| 04 | Logical | Short-circuit | The right side runs only when needed |
| 04 | Logical | Default trap | `0 or 10` gives `10`, because `0` is falsy |
| 04 | Logical | Priority | `not` > `and` > `or` |
| 05 | Bitwise | Operators | `&`, `\|`, `^`, `~`, `<<`, `>>` |
| 05 | Bitwise | `~x` | Equals `-x - 1` because ints have infinite width |
| 05 | Bitwise | Masking | Use `& 0xFF` to see an 8-bit result; `f"{x:08b}"` shows the bits |
| 05 | Bitwise | Shifts | `<<` multiplies and `>>` divides by powers of 2; no overflow; `>>` keeps the sign |
| 05 | Bitwise | Registers | Set `\|= 1<<n`, clear `&= ~(1<<n)`, toggle `^= 1<<n`, test `& (1<<n)` |
| 05 | Bitwise | Helpers | `bit_count()`, `bit_length()`, `bin()`, `hex()` |
| 05 | Bitwise | `&` vs `and` | `5 & 3` is `1`; `5 and 3` is `3` |
| 05 | Bitwise | Priority | `&` binds tighter than `==` in Python (the opposite of C) |
| 06 | Membership | `in` / `not in` | Test whether a value is inside a container |
| 06 | Membership | Strings | Substring test, case-sensitive; `"" in "abc"` is `True` |
| 06 | Membership | Dicts | Checks keys; use `.values()` or `.items()` for the rest |
| 06 | Membership | Nesting | Does not look inside nested containers |
| 06 | Membership | Speed | `set` and `dict` lookups are fast; `list` is a slow linear search |
| 06 | Membership | Errors | `1 in "abc"` raises `TypeError` |
| 07 | Identity | `is` | Same object? (`==` asks equal value?) |
| 07 | Identity | `None` | Always test with `is None` / `is not None` |
| 07 | Identity | Small ints and strings | Caching is a CPython detail; never use `is` on numbers or strings |
| 07 | Identity | Sentinel | `MISSING = object()` with `is` detects "nothing passed" |
| 08 | Walrus | `:=` | Assigns and returns the value inside an expression (3.8+) |
| 08 | Walrus | Use cases | `if`, `while`, comprehensions where a value is used twice |
| 08 | Walrus | Syntax | A bare `x := 5` statement is an error; write `(x := 5)` |
| 09 | Precedence | Order | `()` > `**` > unary > `* / // %` > `+ -` > shifts > `&` > `^` > `\|` > comparisons > `not` > `and` > `or` > `if-else` > `lambda` > `:=` |
| 09 | Precedence | `**` | Right to left: `2 ** 3 ** 2` is `512` |
| 09 | Precedence | Unary minus | `-2 ** 2` is `-4` |
| 09 | Precedence | Same level | Left to right |
| 09 | Precedence | Best practice | Add parentheses whenever in doubt |
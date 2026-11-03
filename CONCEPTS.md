# Module 01: Python Basics, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Home & Syntax | How Python runs | Source `.py` is compiled to bytecode and run by the Python Virtual Machine (PVM) |
| 01 | Home & Syntax | REPL | Typing `python` opens an interactive prompt for quick tests |
| 01 | Home & Syntax | Indentation | Indentation defines blocks (no `{ }`); use 4 spaces consistently |
| 01 | Home & Syntax | Statements | One statement per line is the norm; `;` is allowed but discouraged |
| 01 | Home & Syntax | Line continuation | Use `\` or put the code inside `()`, `[]`, `{}` |
| 01 | Home & Syntax | Keywords | Reserved words (`for`, `class`, `if`) cannot be used as names; check with `keyword.kwlist` |
| 02 | Variables | Variables | Names point to objects, and the type belongs to the object |
| 02 | Variables | Dynamic typing | The same name can point to an int, then a str |
| 02 | Variables | Multiple assignment | `x = y = 0` and `a, b, c = 1, 2, 3` both work |
| 02 | Variables | Swap | `a, b = b, a` needs no temp variable |
| 02 | Variables | `is` vs `==` | `is` checks the same object, `==` checks equal value |
| 02 | Variables | `id()` | Returns the identity of an object; reassigning a name points it to a new object |
| 02 | Variables | Naming rules | Letters, digits, `_`; cannot start with a digit; case-sensitive; no keywords |
| 02 | Variables | Constants | Only a convention (`MAX_RETRIES`); Python does not enforce them |
| 02 | Variables | `del` | Removes the name, not necessarily the object |
| 03 | Private Variables | `_x` | "Internal use" by convention; skipped by `import *` |
| 03 | Private Variables | `__x` | Name-mangled to `_Class__x` inside a class |
| 03 | Private Variables | `__x__` | Reserved for Python itself (dunder names) |
| 03 | Private Variables | Privacy | Only conventions (`_x`, `__x`), never real security |
| 04 | Data Types | Main types | `int`, `float`, `complex`, `bool`, `str`, `None`, `list`, `tuple`, `set`, `dict`, `bytes`, `range` |
| 04 | Data Types | `type()` / `isinstance()` | `type()` shows the type; `isinstance()` answers True/False |
| 04 | Data Types | Immutable | `int`, `float`, `str`, `tuple`, `bool`. "Changing" them creates a new object |
| 04 | Data Types | Mutable | `list`, `dict`, `set` change in place (same `id`) |
| 04 | Data Types | `bool` | A subclass of `int`: `True == 1`, `False == 0`, so `True + True` is `2` |
| 04 | Data Types | `None` | Means "no value"; test with `is None`, and it is not `0` or `""` |
| 05 | Type Casting | Explicit casting | `int()`, `float()`, `str()`, `bool()`, `list()`, `tuple()`, `set()` |
| 05 | Type Casting | `int()` | Truncates toward zero (does not round), and strings must be valid literals |
| 05 | Type Casting | Float strings | `int("3.5")` fails; use `int(float("3.5"))` |
| 05 | Type Casting | Other bases | `int("101", 2)` converts from binary; `bin()`, `oct()`, `hex()` convert back |
| 05 | Type Casting | Implicit casting | Python widens automatically: `1 + 2.5` is `3.5`, `True + 1` is `2` |
| 05 | Type Casting | `chr()` / `ord()` | Number to character and character to number |
| 06 | Unicode | `str` | A sequence of Unicode code points |
| 06 | Unicode | `bytes` | Raw data; `.encode()` makes it from `str`, `.decode()` turns it back |
| 06 | Unicode | UTF-8 | The default encoding, using 1 to 4 bytes per character |
| 06 | Unicode | Length | `len(str)` counts characters; `len(bytes)` counts bytes |
| 06 | Unicode | Escapes | `\u00e9`, `\U0001F600`, `\N{...}` write Unicode characters |
| 06 | Unicode | Where to encode | Only at boundaries (files, network, APIs) |
| 07 | Literals | Integers | `0b` binary, `0o` octal, `0x` hex; `1_000_000` underscores for readability |
| 07 | Literals | Floats | `1.5e3` means 1500.0 |
| 07 | Literals | Complex | `3 + 4j`, with `.real`, `.imag`, `abs()` |
| 07 | Literals | Strings | `'..'`, `".."`, `'''..'''` (multi-line), `r".."` (raw), `f".."` (formatted), `b".."` (bytes) |
| 07 | Literals | Special values | `True`, `False`, `None` |
| 07 | Literals | Tuple trap | `(5)` is an int; the one-item tuple is `(5,)` |
| 07 | Literals | Empty set trap | `{}` is a dict; the empty set is `set()` |
| 08 | Comments | `#` | The only real comment syntax; there is no multi-line comment |
| 08 | Comments | Docstrings | `"""..."""` as the first statement of a function, class or module; stored in `__doc__` |
| 08 | Comments | Shebang | `#!/usr/bin/env python3` lets Linux/macOS run the file directly |
| 09 | User Input | `input()` | Always returns `str` |
| 09 | User Input | Converting input | Cast it yourself: `int(input())` |
| 09 | User Input | Multiple values | `map(int, input().split())` reads several numbers from one line |
| 09 | User Input | `print()` | `sep` and `end` control the separator and line ending |
| 09 | User Input | Pitfall | `input("5") + input("3")` gives `"53"`, not `8` |
| 10 | Numbers | Operators | `/` always gives a float; `//` floors toward negative infinity; `%` and `**` as expected |
| 10 | Numbers | `int` | Unlimited size, so no overflow |
| 10 | Numbers | `divmod()` | Gives `(quotient, remainder)` in one call |
| 10 | Numbers | `round()` | Uses banker's rounding: `round(2.5)` is `2`, `round(3.5)` is `4` |
| 10 | Numbers | `pow(a, b, m)` | Three-argument form does modular exponentiation |
| 10 | Numbers | `math` module | `sqrt`, `floor`, `ceil`, `pi` |
| 10 | Numbers | `Fraction` | Exact rational arithmetic |
| 11 | Booleans | Truthiness | `0`, `""`, `[]`, `{}`, `None` are falsy, and `"0"` is truthy |
| 11 | Booleans | `and` / `or` | Return one of their operands, not just True/False |
| 11 | Booleans | Short-circuit | `and` stops at the first falsy, `or` at the first truthy |
| 11 | Booleans | Style | Write `if items:` instead of `if len(items) > 0:` |
| 12 | Floating Points | `float` | Binary approximation (same as C `double`), so use `isclose` or `Decimal` |
| 12 | Floating Points | Classic bug | `0.1 + 0.2 != 0.3` |
| 12 | Floating Points | `Decimal` | Exact decimal arithmetic; use it for money, and build it from strings |
| 12 | Floating Points | Special values | `inf`, `-inf`, `nan`; `nan != nan`, so use `math.isnan()` |
| 12 | Floating Points | Formatting | `f"{x:.2f}"` and `f"{x:,.2f}"` |
| 12 | Floating Points | Limits | `sys.float_info.max` is about `1.8e308`; beyond that you get `inf` |
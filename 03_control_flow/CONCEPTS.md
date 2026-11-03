# Module 03: Control Flow, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Control Flow | Kinds of flow | Sequential, decision (`if`, `match`) and repetition (`for`, `while`) |
| 01 | Control Flow | Blocks | A colon plus indentation (4 spaces) defines a block; no braces |
| 01 | Control Flow | Errors | Bad indentation raises `IndentationError` |
| 01 | Control Flow | Conditions | Judged by truthiness: `0`, `""`, `[]`, `None` are falsy |
| 02 | If | Syntax | `if condition:` then an indented block |
| 02 | If | Condition | Any expression works; no parentheses needed |
| 02 | If | Style | Use `if items:` not `len(items) > 0`; `if flag:` not `== True` |
| 02 | If | Errors | `if x = 5` is a `SyntaxError`; a missing colon is a `SyntaxError` |
| 03 | If-else | `elif` | The keyword is `elif`, not `else if` |
| 03 | If-else | Branches | Only the first true branch runs |
| 03 | If-else | Order | Put the most specific condition first |
| 03 | If-else | `else` | Has no condition and comes last |
| 03 | If-else | Ternary | `a if condition else b` produces a value |
| 04 | Nested If | Nesting | An `if` inside an `if`; fine for dependent checks |
| 04 | Nested If | Flattening | Use `and` / `or`, or `elif`, to reduce nesting |
| 04 | Nested If | Depth | More than 3 levels is hard to read |
| 05 | User Input | Cleaning | Use `.strip()` and `.lower()` before comparing |
| 05 | User Input | Validation | Check with `.isdigit()` before `int()`; it rejects `-5` and `3.5` |
| 05 | User Input | Range check | `if not 0 <= x <= 100:` |
| 05 | User Input | Menus | Compare `input()` results as strings: `"1"`, not `1` |
| 06 | Match-Case | Version | Python 3.10 or newer |
| 06 | Match-Case | Default | `case _:` matches anything |
| 06 | Match-Case | Patterns | Literals, `\|` (or), guards (`case x if ...`), sequences, `*rest`, dicts |
| 06 | Match-Case | No fall-through | No `break` needed, unlike C `switch` |
| 06 | Match-Case | Bare names | `case RED:` captures, it does not compare |
| 07 | For Loops | `for` | Iterates over the items of any iterable |
| 07 | For Loops | `range()` | `range(stop)`, `range(start, stop)`, `range(start, stop, step)`; the stop is excluded and it is lazy |
| 07 | For Loops | `enumerate()` | Gives `(index, value)`; use `start=1` to change the first index |
| 07 | For Loops | `zip()` | Loops over several sequences together |
| 07 | For Loops | Dicts | `for k in d`, and `for k, v in d.items()` |
| 07 | For Loops | `_` | Name for a variable you do not use |
| 07 | For Loops | Loop variable | Still exists after the loop ends |
| 07 | For Loops | Modifying | Never change a list while looping over it; loop over `nums[:]` |
| 08 | For-else | `else` | Runs only if the loop finished without `break` |
| 08 | For-else | Use | Search patterns and prime checks |
| 08 | For-else | Empty loop | The `else` still runs |
| 08 | For-else | `continue` | Does not stop the `else`; only `break` does |
| 09 | While | `while` | Repeats while the condition is true; update the variable or it never ends |
| 09 | While | Use | Unknown number of repeats, or repeat until something happens |
| 09 | While | `while True` | Plus `break`: the standard way to loop until told to stop |
| 09 | While | Validation | Repeat input until it is valid |
| 09 | While | `while-else` | `else` runs when the condition becomes false |
| 09 | While | No do-while | Emulate with `while True` plus `if not cond: break` |
| 10 | break | `break` | Exits the innermost loop immediately and skips the loop `else` |
| 10 | break | Nested loops | Use a flag to leave both loops |
| 11 | continue | `continue` | Skips to the next iteration; flatter code than nested ifs |
| 11 | continue | In `while` | Update the counter before `continue` or you get an endless loop |
| 12 | pass | `pass` | Does nothing; a placeholder for an empty block |
| 12 | pass | `...` | Ellipsis works as a stub too |
| 12 | pass | Comparison | `pass` keeps going, `continue` skips ahead, `break` leaves |
| 12 | pass | Warning | `except: pass` hides errors |
| 13 | Nested Loops | Cost | Iterations multiply: 100 x 100 is 10,000 |
| 13 | Nested Loops | 2D data | `for row in matrix: for value in row:` |
| 13 | Nested Loops | Patterns | Use `end=""` in the inner loop and `print()` after it |
| 13 | Nested Loops | Control | `break` and `continue` affect only the innermost loop |
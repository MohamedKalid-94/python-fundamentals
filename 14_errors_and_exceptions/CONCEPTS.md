# Module 14: Errors & Exceptions, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Syntax Errors | Three kinds | Syntax (found before anything runs), runtime (an exception), logic (wrong answer, no message) |
| 01 | Syntax Errors | Types | `SyntaxError`, `IndentationError`, `TabError` (the last two are subclasses) |
| 01 | Syntax Errors | Where | Look at the reported line AND the line before it (unclosed brackets) |
| 01 | Syntax Errors | Typical causes | Missing `:`, unclosed `(`, wrong indentation, `=` instead of `==`, keyword as a name, `return` or `break` in the wrong place |
| 01 | Syntax Errors | Find early | `python -m py_compile file.py`, the editor, linters (`ruff`, `flake8`), `ast.parse` |
| 02 | Exceptions | What | An error that happens while the program runs; unhandled, it prints a traceback and stops |
| 02 | Exceptions | Traceback | Read from the BOTTOM: the last line is the type and message, the lines above are the call chain |
| 02 | Exceptions | Propagation | An exception travels up the call stack until something catches it |
| 02 | Exceptions | Object | `e.args`, `str(e)`, `repr(e)`, `e.__traceback__` |
| 02 | Exceptions | Hierarchy | Classes inherit from `Exception` and `BaseException`; `KeyError` is a `LookupError` |
| 03 | try-except | Form | `try / except Type as e / else / finally` |
| 03 | try-except | `else` | Runs only if `try` raised nothing |
| 03 | try-except | Order | The FIRST matching `except` runs: specific types before general ones |
| 03 | try-except | Tuple | `except (ValueError, TypeError)` handles several types the same way |
| 03 | try-except | Parent class | `except LookupError` catches `IndexError` and `KeyError` |
| 03 | try-except | Bare `except:` | Avoid; it also catches Ctrl+C and `sys.exit()` |
| 03 | try-except | Re-raise | A bare `raise` inside `except` passes the same exception on |
| 03 | try-except | Style | Keep the `try` block small; EAFP (try it, handle failure) is common in Python |
| 03 | try-except | `suppress` | `with suppress(FileNotFoundError):` ignores one error on purpose |
| 04 | try-finally | `finally` | Runs ALWAYS: success, error, `return`, `break`, `continue` |
| 04 | try-finally | Use | Cleanup: close files, release locks and buses |
| 04 | try-finally | Unwinding | Every `finally` on the way up runs |
| 04 | try-finally | Trap | `return` inside `finally` replaces the result and swallows exceptions |
| 04 | try-finally | `with` | The shorter, safer form of try/finally for resources |
| 04 | try-finally | `@contextmanager` | Makes your own `with` block from a generator |
| 05 | Raising | `raise` | `raise ValueError("message")` or `raise ValueError` |
| 05 | Raising | Right type | `ValueError` wrong value, `TypeError` wrong type, `OSError` family for the outside world |
| 05 | Raising | Guard clauses | Raise early so the rest of the function stays simple |
| 05 | Raising | Bare `raise` | Outside an `except` block it raises `RuntimeError` |
| 05 | Raising | Data | `OSError(5, "text")` gives `.errno` and `.strerror` |
| 05 | Raising | `NotImplementedError` | Marks a method that children must write |
| 05 | Raising | `SystemExit` | `sys.exit(code)` raises it; `e.code` is the code |
| 05 | Raising | Groups | `ExceptionGroup` and `except*` (3.11+) |
| 06 | Chaining | Explicit | `raise New from old` sets `__cause__` (the direct cause) |
| 06 | Chaining | Implicit | An error raised while handling another sets `__context__` |
| 06 | Chaining | Hide | `raise New from None` suppresses the old error |
| 06 | Chaining | Layers | Translate low-level errors into the errors of your own layer, keeping the cause |
| 06 | Chaining | Notes | `e.add_note("text")` and `e.__notes__` (3.11+) |
| 07 | Nested try | Propagation | An inner handler that does not match passes the error to the outer one |
| 07 | Nested try | Where | `try` can sit inside `try`, `except` or `finally` |
| 07 | Nested try | Cleanup | Wrap cleanup that may fail in its own `try` |
| 07 | Nested try | Readability | Too much nesting: move the inner part into a function |
| 07 | Nested try | Fallbacks | A primary source, then a backup source |
| 08 | User-defined | Create | `class MyError(Exception): pass` |
| 08 | User-defined | Base class | One base per application; callers catch it to get every child |
| 08 | User-defined | Data | Store `field`, `code`, `shortfall` on the object; call `super().__init__(...)` |
| 08 | User-defined | Names | End with `Error` |
| 08 | User-defined | When | Only when callers must tell the errors apart; otherwise use built-in types |
| 09 | Logging | Levels | DEBUG 10, INFO 20, WARNING 30, ERROR 40, CRITICAL 50 |
| 09 | Logging | Threshold | The logger level drops lower messages; the root default is WARNING |
| 09 | Logging | Setup | `logging.basicConfig(level=..., format=..., stream=...)` once; `getLogger(__name__)` per module |
| 09 | Logging | Arguments | `log.info("user %s", name)`, not an f-string |
| 09 | Logging | `exception` | `log.exception("text")` inside `except` adds the traceback |
| 09 | Logging | Handlers | `StreamHandler`, `FileHandler`; each handler has its own level and format |
| 09 | Logging | Hierarchy | `"app.db"` is a child of `"app"` and shares its handlers |
| 09 | Logging | Choose | `print` for quick checks; `logging` for real programs |
| 10 | Assertions | `assert cond, msg` | Raises `AssertionError` if the condition is false |
| 10 | Assertions | Use | Internal checks and invariants (bugs), tests |
| 10 | Assertions | Never | For user input or outside data: use `if` + `raise` |
| 10 | Assertions | `-O` | Removes every assert (`__debug__` becomes `False`) |
| 10 | Assertions | Trap | `assert (cond, "msg")` is a tuple, so it is always true |
| 11 | Warnings | `warnings.warn` | Reports a problem but the program continues |
| 11 | Warnings | Categories | `UserWarning` (default), `DeprecationWarning`, `RuntimeWarning`, `SyntaxWarning` |
| 11 | Warnings | Filters | `simplefilter("ignore" / "error" / "always" / "default")` |
| 11 | Warnings | Capture | `catch_warnings(record=True)` collects them in a list |
| 11 | Warnings | Deprecate | `warn(..., DeprecationWarning, stacklevel=2)` points at the caller |
| 11 | Warnings | Command line | `python -W error` turns warnings into exceptions |
| 12 | Built-in | Root | `BaseException` -> `Exception` -> specific errors |
| 12 | Built-in | Do not catch | `KeyboardInterrupt`, `SystemExit`, `GeneratorExit` are not `Exception` subclasses |
| 12 | Built-in | Families | `ArithmeticError`, `LookupError`, `OSError` (with `FileNotFoundError` etc.), `ValueError` (with `UnicodeError`), `RuntimeError` (with `RecursionError`) |
| 12 | Built-in | Aliases | `IOError` and `EnvironmentError` are `OSError` |
| 12 | Built-in | OSError data | `e.errno`, `e.filename`, `e.strerror` |
| 12 | Built-in | Catch | The most specific type that fits; `except Exception` only at the top of a program |
| 13 | Debugger | Start | `breakpoint()`, `python -m pdb script.py`, `pdb.post_mortem()` |
| 13 | Debugger | Move | `n` next, `s` step into, `r` return, `c` continue, `q` quit |
| 13 | Debugger | Look | `p expr`, `pp expr`, `l` / `ll`, `w` (stack), `u` / `d` |
| 13 | Debugger | Breakpoints | `b line` or `b function`, `tbreak`, `cl` |
| 13 | Debugger | Change | `!total = 0` runs a statement |
| 13 | Debugger | Switch off | `PYTHONBREAKPOINT=0` |
| 13 | Debugger | Quick look | `print(f"{x=}")` |
| 13 | Debugger | VS Code | Click the gutter for a breakpoint, `F5` run, `F10` over, `F11` into, `Shift+F11` out |
| 14 | Examples | Retry | Loop with `except`, keep the last error, then `raise ... from last` |
| 14 | Examples | Collect | Gather every error, then raise one `ValidationError` or `ExceptionGroup` |
| 14 | Examples | Release | `lock()` then `try ... finally: unlock()` |
| 14 | Examples | Top level | `main()` returns exit codes: 0 success, 2 user error, 1 bug |
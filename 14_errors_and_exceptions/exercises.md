Write the questions as # comments and your solutions as code below each one.

Write five lines of code that each cause a different built-in exception (ZeroDivisionError, ValueError, KeyError, IndexError, TypeError), catch each one separately, and print the type and the message.
Write safe_divide(a, b) that returns the result, or None and a printed message when b is zero or an argument is not a number.
Read a number from input() in a loop until the user types a valid whole number between 1 and 10. Report the exact reason for each rejection.
Write read_first_line(path) that handles FileNotFoundError, PermissionError and UnicodeDecodeError with different messages, and an else and a finally branch that print what happened.
Write average_from_file(path) that reads one number per line, skips the lines that are not numbers (and counts them), and returns the average and the number of skipped lines.
Show the try/except/else/finally order of execution with four runs of the same function (success, handled error, unhandled error, return inside try) and print a marker at each step.
Write a function with a return inside try and one inside finally, and explain the result in a comment. Then write a function that uses finally to restore a global variable that it changed.
Create a custom ValidationError hierarchy (AppError -> ValidationError -> MissingFieldError, RangeError) and a validate_user(data) function that raises the right one, and catch them at different levels of detail.
Write parse_config(text) that turns KEY=VALUE lines into a dictionary, and raises a ConfigError (with the line number) for a bad line. Chain the original error with from.
Write retry(times, delay) as a plain function (not a decorator) that calls another function, retrying only on ConnectionError, and returns the result or raises RuntimeError from the last error.
Write a function that processes 10 items, collects the errors of the failing ones, and at the end raises one ExceptionGroup (3.11+). Catch it with except* and print how many failed of each type.
Show implicit chaining, explicit chaining and from None with the same two exceptions, and print __cause__, __context__ and __suppress_context__ for each.
Set up a logger with a console handler (WARNING and above) and a file handler (DEBUG and above) with different formats. Log one message of each level, then print the file’s content and delete the file.
Write a function that logs with log.exception() when it catches an error, and show with StringIO that the traceback is part of the log.
Add assert statements for the preconditions of a circle_area(radius) function and if/raise for validating the same value when it comes from user input. Explain with a comment what happens under python -O.
Use warnings.warn to mark a function as deprecated, capture the warning, and then turn warnings into errors with simplefilter("error") and show the difference.
Write a context manager with @contextmanager called timer(label) that prints how long a block took (use time.perf_counter()), and prints the time even when the block raises an error.
Write a class-based context manager (__enter__ and __exit__) for a fake Spi bus that selects the chip on entry, deselects on exit, and returns False so errors are not swallowed. Test it with and without an error.
Explain with code why except Exception does not catch KeyboardInterrupt and SystemExit, and write a main() that catches SystemExit to print the exit code.
Debug practice: copy 13_debugger_pdb.py, add a third bug (for example an if condition with the wrong comparison), and find all three bugs using breakpoint() or the VS Code debugger. Write down the commands you used.
Embedded exercise: write a read_sensor() simulation that randomly (with a fixed seed) returns a value, raises TimeoutError or raises CrcError (your own class). Write a polling loop that retries on timeouts, logs CRC errors and gives up after 5 failures in a row.
Predict first, then run, and explain each result in a comment:
python
def f():
    try:
        return "try"
    finally:
        print("finally")

def g():
    for i in range(3):
        try:
            if i == 1:
                continue
            if i == 2:
                break
        finally:
            print("cleanup", i)
    return "done"

print(f(), g())

try:
    try:
        int("x")
    except KeyError:
        print("wrong handler")
    finally:
        print("inner finally")
except ValueError as e:
    print("outer:", type(e).__name__)

try:
    raise KeyError("a")
except (ValueError, KeyError) as e:
    print(type(e).__mro__[1].__name__, e.args)

class E(Exception):
    pass

try:
    try:
        raise E("first")
    except E as first:
        raise ValueError("second") from first
except ValueError as e:
    print(e.__cause__, e.__context__ is e.__cause__)
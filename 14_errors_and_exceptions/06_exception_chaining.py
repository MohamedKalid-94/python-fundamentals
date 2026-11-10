import traceback

# When one exception leads to another, Python links them in the traceback.

# 1. EXPLICIT chaining:  raise NewError(...) from original
def load_config(text):
    try:
        return int(text)
    except ValueError as e:
        raise RuntimeError("config is invalid") from e

try:
    load_config("abc")
except RuntimeError as err:
    print(err)                                  # config is invalid
    print(type(err.__cause__).__name__, err.__cause__)
    # ValueError invalid literal for int() with base 10: 'abc'
    print(err.__context__ is err.__cause__)     # True
    text = "".join(traceback.format_exception(err))
print("direct cause" in text)                   # True
# The traceback says: "The above exception was the direct cause of the following exception"

# 2. IMPLICIT chaining: a new error raised while handling another one
try:
    try:
        1 / 0
    except ZeroDivisionError:
        raise KeyError("x")                     # no "from"
except KeyError as err:
    print(type(err.__context__).__name__, err.__cause__)    # ZeroDivisionError None
    print(err.__suppress_context__)             # False
    text = "".join(traceback.format_exception(err))
print("During handling" in text)                # True
# The traceback says: "During handling of the above exception, another exception occurred"

# 3. "from None" hides the original (when it is only noise for the caller)
try:
    try:
        1 / 0
    except ZeroDivisionError:
        raise RuntimeError("clean") from None
except RuntimeError as err:
    print(err, err.__cause__, err.__suppress_context__, type(err.__context__).__name__)
    # clean None True ZeroDivisionError

# 4. Translate low-level errors into the errors of YOUR layer
class DatabaseError(Exception):
    pass

USERS = {"1": "Ann"}

def get_user(user_id):
    try:
        return USERS[user_id]
    except KeyError as e:
        raise DatabaseError(f"user {user_id} not found") from e

try:
    get_user("2")
except DatabaseError as err:
    print(err, "|", type(err.__cause__).__name__)       # user 2 not found | KeyError

# 5. Add context to an exception with notes (Python 3.11+)
e = ValueError("bad")
e.add_note("while reading config.txt")
print(e.__notes__)                              # ['while reading config.txt']

# RULES
#   raise New from old   the old error is the DIRECT CAUSE: use it when you translate errors
#   raise New            the old error is just the CONTEXT (happened while handling)
#   raise New from None  hide the old error from the traceback
import sys

# Every built-in exception inherits from BaseException.
# Almost all of them inherit from Exception, which is what you normally catch.
#
#   BaseException
#    +-- SystemExit, KeyboardInterrupt, GeneratorExit      (not errors: do not catch them)
#    +-- Exception
#         +-- ArithmeticError      ZeroDivisionError, OverflowError, FloatingPointError
#         +-- AssertionError
#         +-- AttributeError
#         +-- EOFError
#         +-- ImportError          ModuleNotFoundError
#         +-- LookupError          IndexError, KeyError
#         +-- MemoryError
#         +-- NameError            UnboundLocalError
#         +-- OSError              FileNotFoundError, FileExistsError, PermissionError,
#         |                        IsADirectoryError, TimeoutError, ConnectionError (+ children)
#         +-- RuntimeError         NotImplementedError, RecursionError
#         +-- StopIteration
#         +-- SyntaxError          IndentationError, TabError
#         +-- TypeError
#         +-- ValueError           UnicodeError (UnicodeDecodeError, UnicodeEncodeError)
#         +-- Warning              (UserWarning, DeprecationWarning, ...)

counter = 0

def unbound():
    counter += 1                                # assigning makes "counter" local

def deep():
    deep()

def not_done():
    raise NotImplementedError

def failed():
    assert False

def interrupt():
    raise KeyboardInterrupt

tests = [
    lambda: 1 / 0,
    lambda: int(float("inf")),
    lambda: [][0],
    lambda: {}["k"],
    lambda: missing_name,
    unbound,
    lambda: None.x,
    lambda: __import__("nothing_here"),
    lambda: open("nofile.txt"),
    lambda: int("x"),
    lambda: b"\xff".decode("utf-8"),
    lambda: len(5),
    lambda: next(iter([])),
    deep,
    not_done,
    failed,
    lambda: sys.exit(),
    interrupt,
]

for test in tests:
    try:
        test()
    except BaseException as e:
        parents = " <- ".join(c.__name__ for c in type(e).__mro__[1:-1])
        print(f"{type(e).__name__} <- {parents}")
# ZeroDivisionError <- ArithmeticError <- Exception <- BaseException
# OverflowError <- ArithmeticError <- Exception <- BaseException
# IndexError <- LookupError <- Exception <- BaseException
# KeyError <- LookupError <- Exception <- BaseException
# NameError <- Exception <- BaseException
# UnboundLocalError <- NameError <- Exception <- BaseException
# AttributeError <- Exception <- BaseException
# ModuleNotFoundError <- ImportError <- Exception <- BaseException
# FileNotFoundError <- OSError <- Exception <- BaseException
# ValueError <- Exception <- BaseException
# UnicodeDecodeError <- UnicodeError <- ValueError <- Exception <- BaseException
# TypeError <- Exception <- BaseException
# StopIteration <- Exception <- BaseException
# RecursionError <- RuntimeError <- Exception <- BaseException
# NotImplementedError <- RuntimeError <- Exception <- BaseException
# AssertionError <- Exception <- BaseException
# SystemExit <- BaseException
# KeyboardInterrupt <- BaseException

# These three are NOT subclasses of Exception, so "except Exception" lets them through
print(issubclass(KeyboardInterrupt, Exception),
      issubclass(SystemExit, Exception),
      issubclass(GeneratorExit, Exception))     # False False False

# Old names that are now aliases of OSError
print(IOError is OSError, EnvironmentError is OSError)      # True True

# The OSError family has many children
print(issubclass(ConnectionRefusedError, ConnectionError),
      issubclass(ConnectionRefusedError, OSError))          # True True

# OSError objects carry the error number and the file name
try:
    open("nofile.txt")
except OSError as e:
    print(e.errno, e.filename)                  # 2 nofile.txt

# CHOOSING WHAT TO CATCH
#   - Catch the most SPECIFIC type that makes sense (FileNotFoundError, not Exception).
#   - Catch a parent (LookupError, OSError, ArithmeticError) when any child gets the same handling.
#   - "except Exception" only at the top of a program (and log the error).
#   - Let KeyboardInterrupt and SystemExit pass.

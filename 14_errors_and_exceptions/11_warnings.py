import warnings

# A WARNING reports something suspicious or outdated, but the program keeps running.
# By default it is printed to stderr, once per location.

# 1. The built-in categories
#    UserWarning (default), DeprecationWarning, FutureWarning, RuntimeWarning,
#    SyntaxWarning, ResourceWarning, ImportWarning, UnicodeWarning, BytesWarning

# 2. Capture warnings to see them
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")             # show every warning
    warnings.warn("low battery")                # UserWarning is the default category
    warnings.warn("old API", DeprecationWarning)
    warnings.warn("slow path", RuntimeWarning)

print([(w.category.__name__, str(w.message)) for w in caught])
# [('UserWarning', 'low battery'), ('DeprecationWarning', 'old API'), ('RuntimeWarning', 'slow path')]

# 3. Turn warnings into exceptions (good for tests)
with warnings.catch_warnings():
    warnings.simplefilter("error")
    try:
        warnings.warn("x")
    except UserWarning as e:
        print("raised:", e)                     # raised: x

# 4. Ignore warnings
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("ignore")
    warnings.warn("hidden")
print(len(caught))                              # 0

# 5. Your own warning category
class LowBatteryWarning(UserWarning):
    pass

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    warnings.warn("battery 10%", LowBatteryWarning)
print(caught[0].category.__name__, caught[0].message)       # LowBatteryWarning battery 10%

# 6. Ignore only one category
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    warnings.simplefilter("ignore", LowBatteryWarning)
    warnings.warn("battery 5%", LowBatteryWarning)
    warnings.warn("something else")
print([str(w.message) for w in caught])         # ['something else']

# 7. The default action shows a warning once per place in the code
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("default")
    for _ in range(3):
        warnings.warn("repeat")                 # the same line three times
print(len(caught))                              # 1

# 8. The standard way to deprecate a function: stacklevel=2 points at the CALLER
def new_api():
    return 1

def old_api():
    warnings.warn("old_api() is deprecated, use new_api()", DeprecationWarning, stacklevel=2)
    return new_api()

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    result = old_api()
print(result, (caught[0].category.__name__, str(caught[0].message)))
# 1 ('DeprecationWarning', 'old_api() is deprecated, use new_api()')

# 9. Python itself warns about suspicious code, for example "is" with a literal
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    compile("x = 1\nif x is 1:\n    pass", "<demo>", "exec")
print(caught[0].category.__name__)              # SyntaxWarning

# COMMAND LINE CONTROL
#   python -W error script.py     every warning becomes an exception
#   python -W ignore script.py    hide all warnings
#   PYTHONWARNINGS=error          the same, through an environment variable
#
# EXCEPTION vs WARNING vs LOG
#   exception   the caller must react, the operation failed
#   warning     the code still works, but the programmer should change something
#   log         a record of what happened, for later reading
# THREE KINDS OF ERRORS
#
#   Syntax error     the code is not valid Python. Found BEFORE anything runs.
#   Runtime error    valid code that fails while running (an EXCEPTION).
#   Logic error      runs without any error but gives a wrong answer. Python cannot see it.

# 1. A syntax error stops the program before the first line runs
source = "print('this line never runs')\nx = (1 +"
try:
    exec(source)
except SyntaxError:
    print("SyntaxError: nothing was executed")        # SyntaxError: nothing was executed

# 2. A runtime error happens AFTER the earlier lines have run
source = "print('this line runs')\nx = 1 / 0"
try:
    exec(source)
except ZeroDivisionError:
    print("ZeroDivisionError after the first line ran")
# this line runs
# ZeroDivisionError after the first line ran

# 3. The most common syntax errors, and where Python reports them
cases = [
    ("missing colon", "if True\n    pass"),
    ("unclosed bracket", "print('hi'"),
    ("bad indentation", "def f():\nprint(1)"),
    ("unexpected indent", "x = 1\n  y = 2"),
    ("assign to literal", "1 = x"),
    ("keyword as name", "class = 5"),
    ("return outside", "return 5"),
    ("break outside loop", "break"),
    ("tabs and spaces", "if True:\n\tx = 1\n        y = 2"),
]

for label, code in cases:
    try:
        compile(code, "<demo>", "exec")
    except SyntaxError as e:                # IndentationError and TabError are subclasses
        print(label, "->", type(e).__name__, "line", e.lineno)
# missing colon -> SyntaxError line 1
# unclosed bracket -> SyntaxError line 1
# bad indentation -> IndentationError line 2
# unexpected indent -> IndentationError line 2
# assign to literal -> SyntaxError line 1
# keyword as name -> SyntaxError line 1
# return outside -> SyntaxError line 1
# break outside loop -> SyntaxError line 1
# tabs and spaces -> TabError line 3

# 4. A logic error: no message at all, just a wrong result
def average(numbers):
    return sum(numbers) / len(numbers) + 1      # the "+ 1" is a bug

print(average([2, 4, 6]))                       # 5.0     (it should be 4.0)

# HOW TO READ A SYNTAX ERROR MESSAGE
#   File "script.py", line 3
#       if x > 5
#               ^
#   SyntaxError: expected ':'
#
#  - Look at the line it points to, AND at the line BEFORE it (an unclosed bracket
#    there is reported on the next line).
#  - The caret ^ shows roughly where Python got confused.
#  - Recent Python versions say what is missing ("'(' was never closed").

# HOW TO FIND THEM EARLY
#   python -m py_compile script.py     checks the syntax without running the file
#   your editor (VS Code underlines errors) and linters such as ruff or flake8
#   import ast; ast.parse(source)      checks a string of code
import argparse
import contextlib
import io
import os
import shlex
import sys

# sys.argv: the raw list of words typed after "python"
#   python 14_command_line_arguments.py data.txt -n 3   ->  sys.argv == [script, "data.txt", "-n", "3"]
print(sys.argv[0].endswith(".py"), len(sys.argv) >= 1)         # True True
print(shlex.split("tool 'my file.txt' -n 3"))   # ['tool', 'my file.txt', '-n', '3']    split like a shell

# argparse reads sys.argv for you. In this lesson we pass a LIST to parse_args(),
# so the output is the same every time (and so you can test your parser).

# 1. Positional and optional arguments
def build_parser():
    parser = argparse.ArgumentParser(prog="tool", description="Demo tool")
    parser.add_argument("filename")                                     # required, by position
    parser.add_argument("-n", "--count", type=int, default=1, help="how many times")
    parser.add_argument("-v", "--verbose", action="store_true")         # a flag: present or not
    return parser

parser = build_parser()
print(parser.parse_args(["data.txt", "-n", "3", "-v"]))
# Namespace(filename='data.txt', count=3, verbose=True)
print(parser.parse_args(["x"]))                 # Namespace(filename='x', count=1, verbose=False)
print(parser.format_usage().strip())            # usage: tool [-h] [-n COUNT] [-v] filename

# 2. Errors: argparse prints a usage message to STDERR and exits with code 2
def parse_error(parser, argv):
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            parser.parse_args(argv)
        except SystemExit as e:
            return e.code, err.getvalue().strip().splitlines()[-1]

print(parse_error(parser, []))
# (2, 'tool: error: the following arguments are required: filename')
print(parse_error(parser, ["x", "-n", "abc"]))
# (2, "tool: error: argument -n/--count: invalid int value: 'abc'")

# 3. More kinds of arguments
p = argparse.ArgumentParser(prog="tool")
p.add_argument("--level", choices=["debug", "info", "warn"], default="info")
p.add_argument("files", nargs="*")                                      # zero or more values
p.add_argument("-i", "--include", action="append", default=[])          # can be repeated
p.add_argument("-q", "--quiet", action="count", default=0)              # -q -q  or  -qq
p.add_argument("--no-color", dest="color", action="store_false")        # a flag that turns OFF
print(p.parse_args(["a.txt", "b.txt", "-i", "x", "-i", "y", "-qq", "--level", "debug", "--no-color"]))
# Namespace(level='debug', files=['a.txt', 'b.txt'], include=['x', 'y'], quiet=2, color=False)
print(parse_error(p, ["--level", "loud"])[0])   # 2     not one of the choices

# 4. Either-or options
q = argparse.ArgumentParser(prog="tool")
group = q.add_mutually_exclusive_group()
group.add_argument("--json", action="store_true")
group.add_argument("--csv", action="store_true")
print(parse_error(q, ["--json", "--csv"]))
# (2, 'tool: error: argument --csv: not allowed with argument --json')

# 5. Your own type checker
def port(text):
    number = int(text)
    if not 0 < number < 65536:
        raise argparse.ArgumentTypeError(f"{number} is not a valid port")
    return number

r = argparse.ArgumentParser(prog="tool")
r.add_argument("-p", "--port", type=port, default=8080)
print(r.parse_args(["-p", "502"]).port)         # 502
print(parse_error(r, ["-p", "70000"]))
# (2, 'tool: error: argument -p/--port: 70000 is not a valid port')

# 6. Sub-commands, like "git add" and "git commit"
main = argparse.ArgumentParser(prog="tool")
sub = main.add_subparsers(dest="command", required=True)
add = sub.add_parser("add", help="add two numbers")
add.add_argument("x", type=int)
add.add_argument("y", type=int)
add.set_defaults(func=lambda a: a.x + a.y)
neg = sub.add_parser("neg", help="negate a number")
neg.add_argument("x", type=int)
neg.set_defaults(func=lambda a: -a.x)

a = main.parse_args(["add", "1", "2"])
print(a.command, a.x, a.y, a.func(a))           # add 1 2 3
b = main.parse_args(["neg", "5"])
print(b.func(b))                                # -5

# 7. --version
v = argparse.ArgumentParser(prog="tool")
v.add_argument("--version", action="version", version="tool 1.0")
out = io.StringIO()
code = None
with contextlib.redirect_stdout(out):
    try:
        v.parse_args(["--version"])
    except SystemExit as e:
        code = e.code
print(repr(out.getvalue()), code)               # 'tool 1.0\n' 0

# THE STANDARD SHAPE OF A COMMAND-LINE PROGRAM
#
#   def main(argv=None):
#       args = build_parser().parse_args(argv)     # argv=None means "use sys.argv"
#       ...do the work...
#       return 0                                   # 0 = success, 1 = error, 2 = usage error
#
#   if __name__ == "__main__":
#       sys.exit(main())
#
# Defaults from the environment:  default=os.environ.get("TOOL_LEVEL", "info")
# Pipes:  cat data.txt | python tool.py       read with sys.stdin
# Other tools: getopt (old, C-like), click and typer (third-party, based on decorators / type hints).
#   import typer
#   def main(name: str, count: int = 1): ...        typer.run(main)
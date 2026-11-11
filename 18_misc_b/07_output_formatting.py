import contextlib
import io
import pprint
import reprlib

# 1. print() options
print("a", "b", "c", sep="-", end="!\n")        # a-b-c!
print(1, 2, 3, sep="")                          # 123
# print("error", file=sys.stderr)               sends text to the error stream
# print("working...", end="", flush=True)       no newline, show it at once (progress messages)

# Capture what a piece of code prints
buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    print("hi")
print(repr(buffer.getvalue()))                  # 'hi\n'

# 2. str() is for people, repr() is for programmers
print(repr("a\n"))                              # 'a\n'
print(f"{'x'!r} {'x'!s}")                       # 'x' x

# 3. Number formats (format spec:  [fill][align][sign][#][0][width][,][.precision][type])
for n in (5, 255):
    print(f"{n:>3} {n:08b} {n:#04x}")
#   5 00000101 0x05
# 255 11111111 0xff
print(f"${1234567.891:,.2f}")                   # $1,234,567.89
print(f"{0.256:.1%} {12345.6789:.2e} {1e-5}")   # 25.6% 1.23e+04 1e-05
print(f"{1234567:_}", format(1234.5, ",.1f"))   # 1_234_567 1,234.5
print("title".center(11, "="))                  # ===title===

# 4. A table with column widths worked out from the data
rows = [("Apple", 1.5, 3), ("Banana", 0.25, 12)]
w = max(len("Item"), max(len(r[0]) for r in rows))
print(f"{'Item':<{w}} {'Price':>5} {'Qty':>3}")
print(f"{'-' * w} {'-' * 5} {'-' * 3}")
for name, price, qty in rows:
    print(f"{name:<{w}} {price:>5.2f} {qty:>3}")
# Item   Price Qty
# ------ ----- ---
# Apple   1.50   3
# Banana  0.25  12

# 5. pprint: readable output for nested data
data = {"name": "Ann", "scores": [90, 85, 77], "address": {"city": "Pune", "zip": "411001"}}
print(pprint.pformat(data, width=60))
# {'address': {'city': 'Pune', 'zip': '411001'},
#  'name': 'Ann',
#  'scores': [90, 85, 77]}
print(pprint.pformat(data, width=60, sort_dicts=False).splitlines()[0])     # {'name': 'Ann',

# 6. reprlib: a short repr of big objects
print(reprlib.repr(list(range(100))))           # [0, 1, 2, 3, 4, 5, ...]

# 7. Your own objects can define how they are formatted: __format__
class Temp:
    def __init__(self, celsius):
        self.celsius = celsius

    def __format__(self, spec):
        if spec == "f":
            return f"{self.celsius * 9 / 5 + 32:.1f}F"
        return f"{self.celsius:.1f}C"

print(f"{Temp(100):f}", f"{Temp(36.6)}")        # 212.0F 36.6C

# 8. Other tools
#   str.ljust / rjust / center / zfill   alignment
#   textwrap                             wrapping long text (file 06)
#   locale.format_string                 numbers in the user's local style (1.234,56 in some countries)
#   rich (pip install rich)              colours, tables, progress bars in the terminal
#   tabulate (pip install tabulate)      ready-made text tables
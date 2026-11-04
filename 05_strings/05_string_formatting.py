name = "Ann"
age = 30

# ---------- 1. f-strings (Python 3.6+): the default choice ----------
print(f"{name} is {age}")                       # Ann is 30
print(f"{age + 1}")                             # 31
print(f"{name.upper()}")                        # ANN
print(f"{'yes' if age >= 18 else 'no'}")        # yes
print(f"{age=}")                                # age=30
print(f"{name=}")                               # name='Ann'
print(f"{name!r}")                              # 'Ann'
print(f"{{literal}} {age}")                     # {literal} 30

# Format specs:  {value:[fill][align][sign][0][width][,][.precision][type]}
pi = 3.14159265
print(f"{pi:.2f}")                              # 3.14
print(f"[{pi:8.3f}]")                           # [   3.142]
print(f"[{pi:<10.1f}]")                         # [3.1       ]
print(f"[{42:05d}]")                            # [00042]
print(f"[{42:>6}]")                             # [    42]
print(f"[{'hi':^8}]")                           # [   hi   ]
print(f"[{'hi':*^8}]")                          # [***hi***]
print(f"{1234567:,}")                           # 1,234,567
print(f"{1234567.891:,.2f}")                    # 1,234,567.89
print(f"{0.256:.1%}")                           # 25.6%
print(f"{255:b} {255:x} {255:X} {255:#x} {5:08b}")
# 11111111 ff FF 0xff 00000101
print(f"{12345.6789:.2e}")                      # 1.23e+04
print(f"{42:+d} {-3.14159:.2f}")                # +42 -3.14

# Width and precision can come from variables
width = 10
print(f"[{'x':>{width}}]")                      # [         x]
print(f"{pi:.{3}f}")                            # 3.142

# A formatted table
print(f"{'Item':<10}{'Price':>8}{'Qty':>5}")
print("-" * 23)
for item, price, qty in [("Apple", 1.5, 3), ("Banana", 0.25, 12)]:
    print(f"{item:<10}{price:>8.2f}{qty:>5}")

# ---------- 2. str.format() ----------
print("{} is {}".format("Ann", 30))             # Ann is 30
print("{0} {1} {0}".format("a", "b"))           # a b a
print("{name} is {age}".format(name="Ann", age=30))     # Ann is 30
print("{:.2f}".format(3.14159))                 # 3.14
print("[{:>6}]".format("hi"))                   # [    hi]
print("{:,}".format(1234567))                   # 1,234,567

# ---------- 3. % operator (old style, still seen in older code and logging) ----------
print("%s is %d" % ("Ann", 30))                 # Ann is 30
print("%.2f" % 3.14159)                         # 3.14
print("[%5d]" % 42)                             # [   42]
print("%05.1f" % 3.14159)                       # 003.1
print("%d%%" % 50)                              # 50%

# Rules of thumb
# - Use f-strings by default.
# - Use .format() when the template is stored separately from the data.
# - Use % only to read old code (and logging's lazy "%s" style).
# - Inside an f-string, use a different quote than the outer one (before Python 3.12).
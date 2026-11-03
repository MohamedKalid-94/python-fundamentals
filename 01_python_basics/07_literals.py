# Integer literals
dec, b, o, h = 255, 0b1111_1111, 0o377, 0xFF
print(dec, b, o, h)                   # 255 255 255 255
big = 1_000_000                       # underscores for readability
print(big)                            # 1000000

# Float and complex literals
print(3.14, 1.5e3, 2E-2)              # 3.14 1500.0 0.02
c = 3 + 4j
print(c.real, c.imag, abs(c))         # 3.0 4.0 5.0

# String literals
s1 = 'single'
s2 = "double"
s3 = '''multi
line'''
raw = r"C:\new\table"                 # raw: backslashes are not escapes
print(s3)                             # multi / line (on two lines)
print(raw)                            # C:\new\table
print(f"{dec=}")                      # dec=255
print(b"hello")                       # b'hello'

# Special literals
print(True, False, None)              # True False None

# Collection literals
print([1, 2], (1, 2), {1, 2}, {"a": 1})
print(type((5)), type((5,)))          # <class 'int'> <class 'tuple'>
print(type({}), type(set()))          # <class 'dict'> <class 'set'>
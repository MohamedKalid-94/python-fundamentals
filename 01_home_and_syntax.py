import sys
import keyword

# How Python runs your code:
# source (.py) -> compiled to bytecode -> executed by the Python Virtual Machine
print("Hello, Python!")
print(sys.version)                    # varies by installation

# Blocks are defined by INDENTATION (no { } like C). Use 4 spaces.
if True:
    print("inside the block")
print("outside the block")

# One statement per line is the norm; ';' is allowed but discouraged
a = 1; b = 2

# Long lines: explicit continuation with \ ...
total = 1 + 2 + \
        3
# ...or implicit continuation inside (), [], {}
values = [1, 2,
          3]
print(total, values)                  # 6 [1, 2, 3]

# Keywords are reserved words and cannot be used as names
print(keyword.iskeyword("for"))       # True
print(keyword.iskeyword("name"))      # False
print(keyword.kwlist[:5])             # ['False', 'None', 'True', 'and', 'as']
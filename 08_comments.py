#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Line 1 above is a "shebang" (used on Linux/macOS to run the file directly).

# Single-line comment
x = 5  # inline comment

# There is no true multi-line comment. Use # on each line:
# line one
# line two

def add(a, b):
    """Return the sum of a and b."""   # docstring: documentation, not a comment
    return a + b

print(add.__doc__)                    # Return the sum of a and b.
print(add(2, 3))                      # 5

# TODO: conventions like TODO / FIXME / NOTE help editors highlight work items
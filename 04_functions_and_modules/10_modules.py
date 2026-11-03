# A module is a .py file. "import" loads it so you can reuse its code.

# 1. import the whole module
import math
print(math.sqrt(16))            # 4.0
print(math.pi)                  # 3.141592653589793

# 2. import specific names
from math import sqrt, floor
print(sqrt(25), floor(2.7))     # 5.0 2

# 3. import with an alias
import math as m
print(m.ceil(2.1))              # 3

# 4. alias a single name
from math import factorial as fact
print(fact(5))                  # 120

# Avoid "from math import *": it floods your namespace and hides where names come from.

# YOUR OWN MODULE (mymath.py in this folder)
import mymath                   # prints: mymath loaded, __name__ = mymath
print(mymath.square(5))         # 25
print(mymath.circle_area(2))    # 12.56636
print(mymath.__name__)          # mymath

# A module is executed only ONCE. Importing again does nothing.
import mymath

# See what a module contains
print([n for n in dir(mymath) if not n.startswith("__")])
# ['PI', '_private_helper', 'circle_area', 'square']

# __name__ is "__main__" in the file you run directly
print(__name__)                 # __main__

# Where does Python look for modules?  sys.path, in this order:
#   1. the folder of the script you ran
#   2. installed packages (site-packages)
#   3. the standard library
import sys
print(sys.version_info >= (3, 10))    # True (on Python 3.10 or newer)

# DO NOT name your file after a standard module (math.py, random.py, json.py).
# Your file would hide the real one and break imports.

# A taste of the standard library (more in Module 17 and 18)
import statistics
import string
from collections import Counter
print(statistics.mean([1, 2, 3, 4]))  # 2.5
print(string.ascii_lowercase[:5])      # abcde
print(Counter("banana"))               # Counter({'a': 3, 'n': 2, 'b': 1})

# Third-party packages are installed with pip (Module 18).
# A folder of modules with an __init__.py is a package (Module 13).

# Standard pattern for runnable files:
#   if __name__ == "__main__":
#       main()
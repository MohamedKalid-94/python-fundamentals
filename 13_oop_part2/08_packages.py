import importlib
import os
import sys

# A MODULE is one .py file. A PACKAGE is a FOLDER of modules with an __init__.py file.
#
#   geometry/               the package
#       __init__.py         runs when the package is imported
#       shapes.py           a module   -> geometry.shapes
#       tools/              a sub-package
#           __init__.py
#           units.py        -> geometry.tools.units

# 1. Import the package: its __init__.py runs ONCE
import geometry                             # prints: geometry package loaded
print(geometry.__version__)                 # 1.0

# __init__.py re-exported Circle, so you can use it directly
print(geometry.Circle(1).area())            # 3.14

# 2. Import a name from the package
from geometry import Rectangle
print(Rectangle(2, 3).area())               # 6

# 3. Import a module of the package
import geometry.shapes
print(geometry.shapes.Circle(2).area())     # 12.57

# 4. Import a module of a sub-package
from geometry.tools import units
print(units.cm_to_inch(10))                 # 3.94

# 5. Import one function, with an alias
from geometry.tools.units import cm_to_inch as c2i
print(c2i(25.4))                            # 10.0

# 6. Names
print(geometry.__name__, geometry.shapes.__name__)      # geometry geometry.shapes
print(os.path.basename(geometry.__path__[0]))           # geometry
print("geometry.tools.units" in sys.modules)             # True     imported modules are cached

# 7. Import by a name stored in a string
mod = importlib.import_module("geometry.shapes")
print(mod is geometry.shapes)               # True

# RULES
# - Inside a package, use RELATIVE imports:   from .shapes import Circle   (same folder)
#                                             from ..shapes import Circle (one level up)
# - Outside the package, use ABSOLUTE imports: from geometry.shapes import Circle
# - __all__ lists the names that "from geometry import *" exports.
# - A folder without __init__.py also works as a "namespace package", but add the file
#   for normal packages.
# - Run a module that lives in a package with:  python -m geometry.shapes
# - Avoid circular imports (a imports b and b imports a): move shared code to a third module.
# - Installing and publishing packages (pip, pyproject.toml) is covered in Module 18.
import sys

import numpy as np

# NUMPY: the base library for numerical work in Python.
#   - ndarray: a fixed-size, one-type, N-dimensional array stored in ONE block of memory
#   - operations on whole arrays run in compiled C code (no Python loop): "vectorized"
#   - pandas, scikit-learn, PyTorch, Matplotlib and most AI tools are built on it
#   - embeddings, images, audio, sensor frames and datasets are all arrays
#
# ENVIRONMENT (PowerShell, inside your virtual environment)
#   pip install numpy
#   python -c "import numpy as np; print(np.__version__)"
#   The usual import is  import numpy as np.   This course uses NumPy 2.x.

print("NumPy major version:", np.__version__.split(".")[0])
print("Python 3.11 or newer:", sys.version_info >= (3, 11))

# 1. A list and an array behave differently
values = [1, 2, 3]
array = np.array(values)
print(values * 2)                   # lists repeat
print(array * 2)                    # arrays calculate, element by element
print(values + [4])                 # lists join
print(array + 4)                    # arrays add 4 to EVERY element (broadcasting, Module 26)

# 2. Memory: a list stores pointers to separate Python objects, an array stores raw numbers side by side
big = np.arange(1000)
print(big.dtype, big.itemsize, big.nbytes)      # 8 bytes per int64, 8000 bytes in total

# 3. Vectorized code replaces a loop
squares_loop = [x * x for x in range(5)]
squares_array = np.arange(5) ** 2
print(squares_loop, squares_array.tolist() == squares_loop)

# 4. Where NumPy is used from here on
#   Modules 25 to 28: NumPy.   Modules 29 to 31: pandas.   Later: scikit-learn, PyTorch, embeddings for RAG.

# EXPECTED OUTPUT
# NumPy major version: 2
# Python 3.11 or newer: True
# [1, 2, 3, 1, 2, 3]
# [2 4 6]
# [1, 2, 3, 4]
# [5 6 7]
# int64 8 8000
# [0, 1, 4, 9, 16] True
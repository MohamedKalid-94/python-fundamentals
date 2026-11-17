import io
import tempfile
from pathlib import Path

import numpy as np

# READING AND WRITING TEXT FILES (CSV and similar)
#   np.loadtxt(file, delimiter, skiprows, usecols, dtype, unpack, ndmin, max_rows, comments)   fast, strict
#   np.genfromtxt(file, delimiter, names=True, filling_values, missing_values)                  tolerates missing values
#   np.savetxt(file, a, fmt, delimiter, header, comments)
# The file may be a path or any text stream, for example io.StringIO(text), which is used here.
#
# FILE FORMATS you will meet                   READ/WRITE WITH
#   .npy .npz        NumPy only, exact, fast       np.save, np.load, np.savez
#   .csv .txt        text, any program             np.loadtxt, np.genfromtxt, np.savetxt (or pandas, Module 30)
#   raw .bin         device dumps, no header       np.fromfile, np.frombuffer, np.memmap
#   .json            small structured data         the json module, or a.tolist()
#   .parquet .xlsx   tables                        pandas (Module 30)
#   .h5 (HDF5)       big labelled arrays           the h5py package (outside this course)

text = "# a comment line\ntime,temp,count\n0,21.5,3\n1,22.0,4\n2,22.5,5\n"
print(np.loadtxt(io.StringIO(text), delimiter=",", skiprows=2))               # the comment line is skipped on its own
print(np.loadtxt(io.StringIO(text), delimiter=",", skiprows=2, usecols=(0, 2), dtype=int))
time, temp, count = np.loadtxt(io.StringIO(text), delimiter=",", skiprows=2, unpack=True)
print(time, temp, count)
print(np.loadtxt(io.StringIO(text), delimiter=",", skiprows=2, max_rows=2).shape)
print(np.loadtxt(io.StringIO("5\n6\n"), ndmin=2).shape)                        # a single column stays 2-D

# A table with names: a structured array
table = np.genfromtxt(io.StringIO(text), delimiter=",", names=True, skip_header=1)
print(table.dtype.names, table["temp"], table["count"].astype(int))

# Missing values: loadtxt refuses, genfromtxt fills them
gaps = "t,v\n0,1.5\n1,\n2,3.5\n"
try:
    np.loadtxt(io.StringIO(gaps), delimiter=",", skiprows=1)
except ValueError as error:
    print("ValueError:", str(error)[:44])
print(np.genfromtxt(io.StringIO(gaps), delimiter=",", skip_header=1))
print(np.genfromtxt(io.StringIO(gaps), delimiter=",", skip_header=1, filling_values=-1)[:, 1])
sentinel = "1,-999,3\n"
print(np.genfromtxt(io.StringIO(sentinel), delimiter=",", missing_values="-999", filling_values=np.nan))

# Mixed types
rows = "ann,25,55.5\nbo,31,70.2\n"
people = np.genfromtxt(io.StringIO(rows), delimiter=",", dtype=[("name", "U8"), ("age", "i4"), ("kg", "f4")])
print(people["name"], people["age"], people.dtype.names)

# Writing
data = np.array([[1.0, 2.5], [3.25, 4.0]])
with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "out.csv"
    np.savetxt(path, data, delimiter=",", fmt="%.2f", header="x,y", comments="")
    print(path.read_text(), end="")
    print(np.loadtxt(path, delimiter=",", skiprows=1).tolist() == data.tolist())
    np.savetxt(path, data)                                                       # the default format: long, exact
    print(path.read_text().splitlines()[0])
    np.savetxt(path, np.array([[1, 2], [3, 4]]), fmt="%d", delimiter="\t")
    print(repr(path.read_text()))

# Round trip precision: the default format keeps every digit, "%.2f" does not
buffer = io.StringIO()
np.savetxt(buffer, [1 / 3], fmt="%.2f")
print(buffer.getvalue().strip(), float(buffer.getvalue()) == 1 / 3)

# EXPECTED OUTPUT
# [[ 0.  21.5  3. ]
#  [ 1.  22.   4. ]
#  [ 2.  22.5  5. ]]
# [[0 3]
#  [1 4]
#  [2 5]]
# [0. 1. 2.] [21.5 22.  22.5] [3. 4. 5.]
# (2, 3)
# (2, 1)
# ('time', 'temp', 'count') [21.5 22.  22.5] [3 4 5]
# ValueError: could not convert string '' to float64 at ro
# [[0.  1.5]
#  [1.  nan]
#  [2.  3.5]]
# [ 1.5 -1.   3.5]
# [   1. -999.    3.]
# ['ann' 'bo'] [25 31] ('name', 'age', 'kg')
# x,y
# 1.00,2.50
# 3.25,4.00
# True
# 1.000000000000000000e+00 2.500000000000000000e+00
# '1\t2\n3\t4\n'
# 0.33 False
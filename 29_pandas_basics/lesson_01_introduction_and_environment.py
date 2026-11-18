import numpy as np
import pandas as pd

# PANDAS: labelled data for Python. Two main structures:
#   Series      one labelled column: a 1-D array together with an INDEX of labels
#   DataFrame   a table: columns (Series) that share one row index
# pandas is built on NumPy: every column is a NumPy array (or a pandas "extension" array) underneath.
# Install: pip install pandas        import: import pandas as pd        This course uses pandas 3.x.
#
# PANDAS 3 CHANGES (older tutorials show the old behaviour; lesson 11 has the details)
#   - text columns get their own "str" dtype (they used to be "object")
#   - COPY-ON-WRITE is always on: changing a result never changes the table it came from,
#     and chained assignment such as df["a"][0] = 1 no longer works
#
# WHY pandas on top of NumPy?
#   NumPy                          pandas
#   position numbers               labels AND positions
#   one dtype for the whole array  one dtype per column
#   no missing-value tools         NaN / NA handling everywhere
#   alignment is up to you         arithmetic aligns on the labels
#   arrays                         tables, time series, files (CSV, Excel, JSON, SQL, Parquet)

print("pandas major version:", pd.__version__.split(".")[0])

s = pd.Series([10, 20, 30], index=["a", "b", "c"], name="reading")
print(s)
df = pd.DataFrame({"name": ["Ann", "Bo", "Cy"], "age": [25, 31, 19], "weight": [55.5, 70.2, 62.0]})
print(df)
print(type(df).__name__, type(df["age"]).__name__, df.shape)
print(df.dtypes)

# From NumPy to pandas and back
a = np.array([[1, 2], [3, 4]])
frame = pd.DataFrame(a, columns=["x", "y"])
print(frame)
print(frame.to_numpy().tolist(), frame["x"].to_numpy())

# Labels make arithmetic safe: values are matched by label, not by position
first = pd.Series([1, 2, 3], index=["x", "y", "z"])
second = pd.Series([10, 20, 30], index=["z", "y", "x"])
print((first + second).tolist(), (first.to_numpy() + second.to_numpy()).tolist())

# What happened to Panel? The 3-D "Panel" was removed from pandas long ago.
print(hasattr(pd, "Panel"))
# Use a DataFrame with a MultiIndex (Module 31) for 3-D labelled data, or the xarray package for N-D arrays.

# Options change how tables are shown (they do not change the data)
print(pd.get_option("display.max_rows"), pd.get_option("display.width"))
with pd.option_context("display.precision", 2):
    print(pd.Series([3.14159, 2.71828]))

# EXPECTED OUTPUT
# pandas major version: 3
# a    10
# b    20
# c    30
# Name: reading, dtype: int64
#   name  age  weight
# 0  Ann   25    55.5
# 1   Bo   31    70.2
# 2   Cy   19    62.0
# DataFrame Series (3, 3)
# name          str
# age         int64
# weight    float64
# dtype: object
#    x  y
# 0  1  2
# 1  3  4
# [[1, 2], [3, 4]] [1 3]
# [31, 22, 13] [11, 22, 33]
# False
# 60 80
# 0    3.14
# 1    2.72
# dtype: float64
import io

import numpy as np
import pandas as pd

# A DATAFRAME: pd.DataFrame(data, index=None, columns=None, dtype=None)
#   from a dict of lists / Series / arrays          (keys = column names)
#   from a list of dicts                            (one dict per row)
#   from a 2-D NumPy array (give the column names)  from a list of tuples / records
#   attributes: shape size ndim columns index dtypes values (to_numpy) T empty axes memory_usage()
#   first look: head tail info describe

df = pd.DataFrame({"name": ["Ann", "Bo", "Cy", "Di"], "age": [25, 31, 19, 44], "kg": [55.5, 70.2, 62.0, 81.3], "member": [True, False, True, True]})
print(df)
print(df.shape, df.size, df.ndim, df.columns.tolist(), df.index)
print(df.dtypes)

# Other ways to build a table
print(pd.DataFrame([{"a": 1, "b": 2}, {"a": 3, "c": 4}]))                         # missing keys become NaN
print(pd.DataFrame(np.arange(6).reshape(2, 3), columns=["x", "y", "z"], index=["r1", "r2"]))
print(pd.DataFrame([("Ann", 25), ("Bo", 31)], columns=["name", "age"]))
print(pd.DataFrame({"a": pd.Series([1, 2], index=["x", "y"]), "b": pd.Series([3, 4, 5], index=["y", "z", "w"])}))   # aligned on the labels
print(pd.DataFrame({"a": [1, 2, 3], "b": "same"}))                                # a single value is repeated
records = np.array([(1, 2.5), (2, 3.5)], dtype=[("id", "i4"), ("v", "f8")])
print(pd.DataFrame(records))
print(pd.DataFrame(columns=["a", "b"]).shape, pd.DataFrame().empty)
try:
    pd.DataFrame({"a": [1, 2], "b": [1, 2, 3]})
except ValueError as error:
    print("ValueError:", error)

# Attributes
print(df.T)
print(df.to_numpy().dtype, df[["age", "kg"]].to_numpy().shape, df.axes[1].tolist())
print(df["age"].nbytes, df["kg"].memory_usage(index=False))       # bytes of one numeric column

# A first look at the data
print(df.head(2))
print(df.tail(2))
print(df.describe())
print(df.describe(include="all").loc[["count", "unique", "top", "freq"], ["name", "member"]])
print(df.describe().loc[["mean", "std"], "age"].round(3).tolist(), df["age"].describe()["50%"])

buffer = io.StringIO()
df.info(buf=buffer, memory_usage=False)
print(buffer.getvalue().rstrip())

# dtype control
typed = pd.DataFrame({"a": [1, 2], "b": [1.5, 2.5]}, dtype="float32")
print(typed.dtypes.tolist())
print(df.astype({"age": "float64"}).dtypes["age"], [str(t) for t in df.convert_dtypes().dtypes])
print(df.select_dtypes(include="number").columns.tolist(), df.select_dtypes(exclude="number").columns.tolist())

# EXPECTED OUTPUT
#   name  age    kg  member
# 0  Ann   25  55.5    True
# 1   Bo   31  70.2   False
# 2   Cy   19  62.0    True
# 3   Di   44  81.3    True
# (4, 4) 16 2 ['name', 'age', 'kg', 'member'] RangeIndex(start=0, stop=4, step=1)
# name          str
# age         int64
# kg        float64
# member       bool
# dtype: object
#    a    b    c
# 0  1  2.0  NaN
# 1  3  NaN  4.0
#     x  y  z
# r1  0  1  2
# r2  3  4  5
#   name  age
# 0  Ann   25
# 1   Bo   31
#      a    b
# w  NaN  5.0
# x  1.0  NaN
# y  2.0  3.0
# z  NaN  4.0
#    a     b
# 0  1  same
# 1  2  same
# 2  3  same
#    id    v
# 0   1  2.5
# 1   2  3.5
# (0, 2) True
# ValueError: All arrays must be of the same length
#            0      1     2     3
# name     Ann     Bo    Cy    Di
# age       25     31    19    44
# kg      55.5   70.2  62.0  81.3
# member  True  False  True  True
# object (4, 2) ['name', 'age', 'kg', 'member']
# 32 32
#   name  age    kg  member
# 0  Ann   25  55.5    True
# 1   Bo   31  70.2   False
#   name  age    kg  member
# 2   Cy   19  62.0    True
# 3   Di   44  81.3    True
#              age         kg
# count   4.000000   4.000000
# mean   29.750000  67.250000
# std    10.688779  11.131487
# min    19.000000  55.500000
# 25%    23.500000  60.375000
# 50%    28.000000  66.100000
# 75%    34.250000  72.975000
# max    44.000000  81.300000
#        name member
# count     4      4
# unique    4      2
# top     Ann   True
# freq      1      3
# [29.75, 10.689] 28.0
# <class 'pandas.DataFrame'>
# RangeIndex: 4 entries, 0 to 3
# Data columns (total 4 columns):
#  #   Column  Non-Null Count  Dtype
# ---  ------  --------------  -----
#  0   name    4 non-null      str
#  1   age     4 non-null      int64
#  2   kg      4 non-null      float64
#  3   member  4 non-null      bool
# dtypes: bool(1), float64(1), int64(1), str(1)
# [dtype('float32'), dtype('float32')]
# float64 ['string', 'Int64', 'Float64', 'boolean']
# ['age', 'kg'] ['name', 'member']
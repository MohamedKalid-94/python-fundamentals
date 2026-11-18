import numpy as np
import pandas as pd

# A SERIES: pd.Series(data, index=None, dtype=None, name=None)
#   data can be a list, an ndarray, a dict (the keys become the index) or a single value
#   attributes: values index dtype name shape size ndim nbytes empty is_unique hasnans axes T

s = pd.Series([3, 1, 4, 1, 5])
print(s)
print(s.index, s.dtype)
named = pd.Series([21.5, 22.0, 23.1], index=["mon", "tue", "wed"], name="temp")
print(named)

# From a dictionary, an ndarray and a single value
print(pd.Series({"a": 1, "b": 2, "c": 3}))
print(pd.Series({"a": 1, "b": 2}, index=["b", "c"]))                 # the index picks and orders the keys; "c" is missing
print(pd.Series(np.arange(3.0)).tolist(), pd.Series(7, index=["x", "y"]).tolist())
print(pd.Series(["a", "b"]).dtype, pd.Series([1, 2.5]).dtype, pd.Series([1, "a"]).dtype, pd.Series([True, False]).dtype)
print(pd.Series([1, 2, 3], dtype="float32").dtype, pd.Series([1, None, 3]).dtype)    # a missing value turns ints into floats

# Attributes
print(named.values, named.index.tolist(), named.dtype, named.name)
print(named.shape, named.size, named.ndim, named.nbytes, named.empty)
print(s.is_unique, named.is_unique, s.hasnans, pd.Series([1.0, np.nan]).hasnans)
print(named.is_monotonic_increasing, named.axes[0].tolist(), named.T.equals(named))

# The data as NumPy, and copies
array = named.to_numpy()
print(type(array).__name__, array.dtype, array.flags.writeable)       # the NumPy array of a Series is read-only
editable = named.to_numpy(copy=True)
editable[0] = -1
print(named.iloc[0], editable[0])
print(len(named), list(named), "tue" in named, 22.0 in named.values)

# Naming and renaming
print(named.rename("temperature").name, named.rename({"mon": "MON"}).index.tolist())
print(named.rename_axis("day").index.name)
print(pd.Series(range(5), index=pd.RangeIndex(5, 10)).index.tolist())
print(pd.Series([1, 2, 3]).sum(), pd.Series([], dtype=float).empty)

# EXPECTED OUTPUT
# 0    3
# 1    1
# 2    4
# 3    1
# 4    5
# dtype: int64
# RangeIndex(start=0, stop=5, step=1) int64
# mon    21.5
# tue    22.0
# wed    23.1
# Name: temp, dtype: float64
# a    1
# b    2
# c    3
# dtype: int64
# b    2.0
# c    NaN
# dtype: float64
# [0.0, 1.0, 2.0] [7, 7]
# str float64 object bool
# float32 float64
# [21.5 22.  23.1] ['mon', 'tue', 'wed'] float64 temp
# (3,) 3 1 24 False
# False True False True
# True ['mon', 'tue', 'wed'] True
# ndarray float64 False
# 21.5 -1.0
# 3 [21.5, 22.0, 23.1] True True
# temperature ['MON', 'tue', 'wed']
# day
# [5, 6, 7, 8, 9]
# 6 True
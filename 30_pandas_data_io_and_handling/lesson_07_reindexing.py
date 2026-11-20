import numpy as np
import pandas as pd

# REINDEXING: make a Series or DataFrame follow a NEW set of labels
#   s.reindex(labels)                      labels that do not exist become NaN (or fill_value); labels you leave out are dropped
#   df.reindex(index=..., columns=..., fill_value=...)
#   method="ffill" | "bfill" | "nearest"   fill the new labels from the neighbours (the OLD index must be sorted); limit=, tolerance=
#   df.reindex_like(other)   s1.align(s2, join=...)   df.set_axis(labels, axis=...)   df.rename(...)
# reindex is not the same as loc: loc[["a", "z"]] raises KeyError for "z", reindex gives NaN.

s = pd.Series([1, 2, 3], index=["a", "b", "c"])
print(s.reindex(["c", "a", "z"]).tolist(), s.reindex(["c", "a", "z"], fill_value=0).tolist(), s.reindex(["b"]).tolist())
try:
    s.loc[["a", "z"]]
except KeyError as error:
    print("KeyError:", str(error)[:40])

df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]}, index=["r1", "r2", "r3"])
print(df.reindex(index=["r3", "r1", "r9"], columns=["y", "z"]))
print(df.reindex(columns=["y", "x", "z"], fill_value=0).values.tolist(), df.reindex(df.index[::-1]).index.tolist())
print(df.reindex(sorted(df.columns, reverse=True), axis=1).columns.tolist())

# Making a table follow a fixed schema (a common safety net when files change)
schema = ["id", "name", "temp"]
incoming = pd.DataFrame({"temp": [21.5], "name": ["Ann"], "extra": [1]})
print(incoming.reindex(columns=schema).columns.tolist(), incoming.reindex(columns=schema).isna().values.tolist())
print(df.reindex_like(pd.DataFrame(index=["r2", "r3", "r4"], columns=["x", "w"])))

# Filling from the neighbours (the original index must be sorted)
sparse = pd.Series([10, 20, 30], index=[0, 5, 10])
print(sparse.reindex(range(0, 11, 2)).tolist())
print(sparse.reindex(range(0, 11, 2), method="ffill").tolist(), sparse.reindex(range(0, 11, 2), method="bfill").tolist())
print(sparse.reindex([1, 4, 6, 9], method="nearest").tolist(), sparse.reindex([1, 4, 6, 9], method="nearest", tolerance=1).tolist())
print(sparse.reindex(range(0, 11, 2), method="ffill", limit=1).tolist())

# Gaps in a time series: reindex to the full set of times, then fill
readings = pd.Series([1.0, 2.0, 4.0], index=pd.to_datetime(["2026-11-15 10:00", "2026-11-15 11:00", "2026-11-15 13:00"]))
full_range = pd.date_range("2026-11-15 10:00", "2026-11-15 13:00", freq="h")
complete = readings.reindex(full_range)
print(complete.tolist(), complete.isna().sum(), complete.interpolate().tolist(), complete.ffill().tolist(), complete.fillna(0).tolist())
print(full_range.difference(readings.index).strftime("%H:%M").tolist())

# Duplicate labels cannot be reindexed
duplicated = pd.Series([1, 2], index=["a", "a"])
try:
    duplicated.reindex(["a"])
except ValueError as error:
    print("ValueError:", error)

# Aligning two objects
a = pd.Series([1, 2, 3], index=["x", "y", "z"])
b = pd.Series([10, 20, 30], index=["y", "z", "w"])
left, right = a.align(b)
print(left.tolist(), right.tolist(), left.index.tolist())
left, right = a.align(b, join="inner")
print(left.tolist(), right.tolist())
left, right = a.align(b, join="left", fill_value=0)
print(left.index.tolist(), right.tolist())

# Replacing labels without changing the data
print(a.set_axis(["p", "q", "r"]).index.tolist(), df.set_axis(["A", "B"], axis=1).columns.tolist(), df.rename(index=str.upper, columns={"x": "X"}).index.tolist())
print(df.reset_index().columns.tolist(), df.reset_index(drop=True).index.tolist(), df.rename_axis("row").index.name)

# A table of results for ALL the categories, even the ones that did not occur
counts = pd.Series(["b", "a", "b"]).value_counts()
print(counts.reindex(["a", "b", "c"], fill_value=0).to_dict())

# EXPECTED OUTPUT
# [3.0, 1.0, nan] [3, 1, 0] [2]
# KeyError: "['z'] not in index"
#       y   z
# r3  6.0 NaN
# r1  4.0 NaN
# r9  NaN NaN
# [[4, 1, 0], [5, 2, 0], [6, 3, 0]] ['r3', 'r2', 'r1']
# ['y', 'x']
# ['id', 'name', 'temp'] [[True, False, False]]
#       x   w
# r2  2.0 NaN
# r3  3.0 NaN
# r4  NaN NaN
# [10.0, nan, nan, nan, nan, 30.0]
# [10, 10, 10, 20, 20, 30] [10, 20, 20, 30, 30, 30]
# [10, 20, 20, 30] [10, 20, 20, 30]
# [10.0, 10.0, nan, 20.0, nan, 30.0]
# [1.0, 2.0, nan, 4.0] 1 [1.0, 2.0, 3.0, 4.0] [1.0, 2.0, 2.0, 4.0] [1.0, 2.0, 0.0, 4.0]
# ['12:00']
# ValueError: cannot reindex on an axis with duplicate labels
# [nan, 1.0, 2.0, 3.0] [30.0, nan, 10.0, 20.0] ['w', 'x', 'y', 'z']
# [2, 3] [10, 20]
# ['x', 'y', 'z'] [0.0, 10.0, 20.0]
# ['p', 'q', 'r'] ['A', 'B'] ['R1', 'R2', 'R3']
# ['index', 'x', 'y'] [0, 1, 2] row
# {'a': 1, 'b': 2, 'c': 0}
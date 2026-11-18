import numpy as np
import pandas as pd

# ARITHMETIC ON SERIES aligns on the INDEX LABELS (not on positions):
#   a + b, a - b, a * b, a / b, a // b, a % b, a ** b     labels found in only one Series give NaN
#   a.add(b, fill_value=0)  .sub  .mul  .div  .pow           the method forms can fill the missing side
#   a + 5, a * 2, np.sqrt(a)                                 scalars and NumPy functions keep the index
#   a > 2, a == b (same labels needed), (a > 1) & (a < 3), a.isna()
# CONVERSIONS: to_list  to_dict  to_numpy  to_frame  to_csv  to_json  to_string  astype  pd.to_numeric  pd.to_datetime

a = pd.Series([1, 2, 3], index=["x", "y", "z"])
b = pd.Series([10, 20, 30], index=["y", "z", "w"])
print(a + b)
print(a.add(b, fill_value=0))
print(a * 2, 100 - a, a / 4, a // 2, a % 2, a ** 2, sep="\n")
print(np.sqrt(a).round(3).tolist(), np.exp(a).round(2).tolist(), (-a).tolist(), abs(-a).tolist())

# Comparisons and logic
print((a > 1).tolist(), ((a > 1) & (a < 3)).tolist(), (a == pd.Series([1, 0, 3], index=["x", "y", "z"])).tolist())
try:
    a == b
except ValueError as error:
    print("ValueError:", error)
print(a.equals(a.copy()), a.eq(2).tolist(), a.gt(1).tolist(), a.isin([2, 3]).tolist())

# Reductions and running calculations
print(a.sum(), a.mean(), a.max(), a.std(), a.cumsum().tolist(), a.diff().tolist(), a.pct_change().round(3).tolist())
print(a.map(lambda v: v * 10).tolist(), a.map({1: "one", 2: "two"}).tolist(), a.apply(lambda v: v ** 2).tolist())
print(a.clip(2, 3).tolist(), a.rank().tolist(), a.shift(1).tolist(), a.abs().tolist())

# Missing values in the result
c = pd.Series([1.0, np.nan, 3.0])
print(c.sum(), c.mean(), c.isna().tolist(), c.fillna(0).tolist(), (c + 1).tolist())

# CONVERSIONS
named = a.rename("v")
print(named.to_list(), named.to_dict(), named.to_numpy())
print(named.to_frame())
print(named.to_csv(), end="")
print(named.to_json(), named.to_string().splitlines()[0], named.astype(float).tolist(), named.astype(str).tolist())
print(named.reset_index())
print(pd.to_numeric(pd.Series(["1", "2.5", "x"]), errors="coerce").tolist())
print(pd.to_datetime(pd.Series(["2026-11-15", "2026-12-25"])).dt.month.tolist())
print(pd.Series([1, 2, 3]).to_frame("n").T)
print(pd.Series({"a": 1}).to_frame().columns.tolist(), pd.Series([1, 2], name="k").to_frame().columns.tolist())
print(pd.Series(list("abc")).to_numpy(), pd.Series([1, 2]).to_numpy().dtype)

# EXPECTED OUTPUT
# w     NaN
# x     NaN
# y    12.0
# z    23.0
# dtype: float64
# w    30.0
# x     1.0
# y    12.0
# z    23.0
# dtype: float64
# x    2
# y    4
# z    6
# dtype: int64
# x    99
# y    98
# z    97
# dtype: int64
# x    0.25
# y    0.50
# z    0.75
# dtype: float64
# x    0
# y    1
# z    1
# dtype: int64
# x    1
# y    0
# z    1
# dtype: int64
# x    1
# y    4
# z    9
# dtype: int64
# [1.0, 1.414, 1.732] [2.72, 7.39, 20.09] [-1, -2, -3] [1, 2, 3]
# [False, True, True] [False, True, False] [True, False, True]
# ValueError: Can only compare identically-labeled Series objects
# True [False, True, False] [False, True, True] [False, True, True]
# 6 2.0 3 1.0 [1, 3, 6] [nan, 1.0, 1.0] [nan, 1.0, 0.5]
# [10, 20, 30] ['one', 'two', nan] [1, 4, 9]
# [2, 2, 3] [1.0, 2.0, 3.0] [nan, 1.0, 2.0] [1, 2, 3]
# 4.0 2.0 [False, True, False] [1.0, 0.0, 3.0] [2.0, nan, 4.0]
# [1, 2, 3] {'x': 1, 'y': 2, 'z': 3} [1 2 3]
#    v
# x  1
# y  2
# z  3
# ,v
# x,1
# y,2
# z,3
# {"x":1,"y":2,"z":3} x    1 [1.0, 2.0, 3.0] ['1', '2', '3']
#   index  v
# 0     x  1
# 1     y  2
# 2     z  3
# [1.0, 2.5, nan]
# [11, 12]
#    0  1  2
# n  1  2  3
# [0] ['k']
# ['a' 'b' 'c'] int64
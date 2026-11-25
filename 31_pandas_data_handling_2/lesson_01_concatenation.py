import io

import numpy as np
import pandas as pd

# CONCATENATION: stack tables on top of each other (axis=0) or side by side (axis=1)
#   pd.concat([a, b, ...], axis=0, join="outer", ignore_index=False, keys=None, verify_integrity=False)
#   axis=0   add ROWS: columns are matched by name, missing columns become NaN (join="inner" keeps only the common ones)
#   axis=1   add COLUMNS: rows are matched by INDEX label
#   keys=[...]   label where each piece came from (a MultiIndex, Module 32)
#   ignore_index=True   renumber the rows 0, 1, 2 ...
# DataFrame.append was removed from pandas: use concat. Build a LIST of tables and call concat ONCE (it copies the data each time).

a = pd.DataFrame({"id": [1, 2], "v": [10, 20]})
b = pd.DataFrame({"id": [3, 4], "v": [30, 40]})
c = pd.DataFrame({"id": [5], "w": [0.5]})
print(pd.concat([a, b]))
print(pd.concat([a, b], ignore_index=True).index.tolist())
print(pd.concat([a, c]))
print(pd.concat([a, c], join="inner").columns.tolist(), pd.concat([a, c], sort=True).columns.tolist())

# Where did each row come from?
both = pd.concat([a, b], keys=["jan", "feb"])
print(both.index.tolist())
print(both.loc["feb"])
print(pd.concat([a, b], keys=["jan", "feb"], names=["month", "row"]).index.names)
labelled = pd.concat([a.assign(source="jan"), b.assign(source="feb")], ignore_index=True)
print(labelled["source"].tolist())

# Duplicate index values
try:
    pd.concat([a, b], verify_integrity=True)
except ValueError as error:
    print("ValueError:", error)
print(pd.concat([a, b]).loc[0].shape, pd.concat([a, b], ignore_index=True).loc[0].shape)

# Side by side: rows are matched by the index
left = pd.DataFrame({"x": [1, 2, 3]}, index=["r1", "r2", "r3"])
right = pd.DataFrame({"y": [10, 20, 30]}, index=["r2", "r3", "r4"])
print(pd.concat([left, right], axis=1))
print(pd.concat([left, right], axis=1, join="inner"))
print(pd.concat([pd.Series([1, 2], name="p"), pd.Series([3, 4], name="q")], axis=1).columns.tolist(), pd.concat([pd.Series([1, 2]), pd.Series([3, 4])], axis=1, keys=["m", "n"]).columns.tolist())
print(pd.concat([pd.Series([1, 2]), pd.Series([3])]).tolist(), pd.concat([pd.Series([1, 2]), pd.Series([3])], ignore_index=True).index.tolist())

# Types of the result
print(pd.concat([pd.DataFrame({"n": [1]}), pd.DataFrame({"n": [2.5]})])["n"].dtype, pd.concat([pd.DataFrame({"n": [1]}), pd.DataFrame({"n": [None]})])["n"].dtype)
print(pd.concat([pd.DataFrame({"n": [1]}), pd.DataFrame({"n": ["x"]})])["n"].dtype)

# Many files: a list of tables, one concat. The text stands in for the files.
files = ["id,v\n1,10\n2,20\n", "id,v\n3,30\n", "id,v\n4,40\n5,50\n"]
tables = [pd.read_csv(io.StringIO(text)) for text in files]
combined = pd.concat(tables, keys=["f1", "f2", "f3"], names=["file", "row"]).reset_index(level="file")
print(combined)
print(len(combined), combined["v"].sum(), combined["file"].value_counts().sort_index().to_dict())

# Adding one row (a new table with one row, then concat)
more = pd.concat([a, pd.DataFrame([{"id": 9, "v": 90}])], ignore_index=True)
print(more.values.tolist(), hasattr(pd.DataFrame, "append"))

# combine_first and update: fill the gaps of one table from another
x = pd.DataFrame({"a": [1.0, np.nan], "b": [np.nan, 4.0]})
y = pd.DataFrame({"a": [9.0, 9.0], "b": [8.0, 8.0]})
print(x.combine_first(y).values.tolist())
z = x.copy()
z.update(pd.DataFrame({"a": [np.nan, 7.0]}))                         # only non-missing values of the other table are used
print(z.values.tolist())
print(x.fillna(y).values.tolist(), x.where(x.notna(), y).equals(x.fillna(y)))

# The pieces are copies: changing the result does not change the originals
result = pd.concat([a, b], ignore_index=True)
result.loc[0, "v"] = -1
print(a.loc[0, "v"], result.loc[0, "v"])

# EXPECTED OUTPUT
#    id   v
# 0   1  10
# 1   2  20
# 0   3  30
# 1   4  40
# [0, 1, 2, 3]
#    id     v    w
# 0   1  10.0  NaN
# 1   2  20.0  NaN
# 0   5   NaN  0.5
# ['id'] ['id', 'v', 'w']
# [('jan', 0), ('jan', 1), ('feb', 0), ('feb', 1)]
#    id   v
# 0   3  30
# 1   4  40
# ['month', 'row']
# ['jan', 'jan', 'feb', 'feb']
# ValueError: Indexes have overlapping values: Index([0, 1], dtype='int64')
# (2, 2) (2,)
#       x     y
# r1  1.0   NaN
# r2  2.0  10.0
# r3  3.0  20.0
# r4  NaN  30.0
#     x   y
# r2  2  10
# r3  3  20
# ['p', 'q'] ['m', 'n']
# [1, 2, 3] [0, 1, 2]
# float64 object
# object
#     file  id   v
# row
# 0     f1   1  10
# 1     f1   2  20
# 0     f2   3  30
# 0     f3   4  40
# 1     f3   5  50
# 5 150 {'f1': 2, 'f2': 1, 'f3': 2}
# [[1, 10], [2, 20], [9, 90]] False
# [[1.0, 8.0], [9.0, 4.0]]
# [[1.0, nan], [7.0, 4.0]]
# [[1.0, 8.0], [9.0, 4.0]] True
# 10 -1
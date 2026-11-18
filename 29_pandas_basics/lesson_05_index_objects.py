import pandas as pd

# INDEX OBJECTS: the labels of the rows (and the columns) of a Series or a DataFrame.
#   pd.Index([...], name=...)     labels of any type            pd.RangeIndex(start, stop, step)   the default, 0 1 2 ...
#   pd.date_range(...)            a DatetimeIndex (dates and times)     pd.MultiIndex                 several levels (Module 31)
# An Index is IMMUTABLE: you replace it, you do not change one label.
#   idx.union / intersection / difference / symmetric_difference      set operations
#   idx.get_loc(label)  idx.get_indexer(labels)  idx.isin(labels)  idx.is_unique  idx.name  idx.dtype  idx.size
#   df.set_index("col")  df.reset_index()  df.rename_axis("name")  df.index = [...]  df.columns = [...]

idx = pd.Index(["a", "b", "c"], name="letters")
print(idx, idx.name, idx.dtype, idx.size, idx.shape)
print(idx[0], idx[1:].tolist(), "b" in idx, idx.is_unique, idx.is_monotonic_increasing)
try:
    idx[0] = "z"
except TypeError as error:
    print("TypeError:", error)

ranged = pd.RangeIndex(5)
print(ranged, ranged.start, ranged.stop, ranged.step, pd.RangeIndex(10, 20, 5).tolist())
print(pd.Series([1, 2, 3]).index, pd.DataFrame({"a": [1, 2]}).index)

# Set operations
x = pd.Index([1, 2, 3, 4])
y = pd.Index([3, 4, 5])
print(x.union(y).tolist(), x.intersection(y).tolist(), x.difference(y).tolist(), x.symmetric_difference(y).tolist())
print(x.append(y).tolist(), x.insert(1, 99).tolist(), x.delete(0).tolist(), x.drop(2).tolist())

# Looking up labels
print(idx.get_loc("b"), idx.get_indexer(["c", "a", "z"]), idx.isin(["a", "z"]), idx.map(str.upper).tolist())
print(idx.str.upper().tolist(), idx.sort_values(ascending=False).tolist(), idx.astype(str).tolist())

# Duplicate labels are allowed (but make lookups return several rows)
dup = pd.Series([1, 2, 3], index=["a", "a", "b"])
print(dup.index.is_unique, dup["a"].tolist(), dup.loc["b"], dup.index.get_loc("a"))

# Replacing the index of a table
df = pd.DataFrame({"id": [101, 102, 103], "name": ["Ann", "Bo", "Cy"]})
by_id = df.set_index("id")
print(by_id)
print(by_id.loc[102, "name"], by_id.index.name, by_id.reset_index().columns.tolist())
print(by_id.rename_axis("employee").index.name, by_id.rename_axis(None).index.name)
df.index = ["r1", "r2", "r3"]
df.columns = ["ID", "NAME"]
print(df)
print(df.rename(index={"r1": "first"}, columns={"ID": "id"}))
print(df.index.tolist(), df.columns.tolist(), df.columns)

# Dates as an index
days = pd.date_range("2026-11-15", periods=4, freq="D")
series = pd.Series([1.0, 2.0, 3.0, 4.0], index=days)
print(days.day_name().tolist(), days.month.tolist(), days.dayofweek.tolist(), days.strftime("%d/%m").tolist())
print(series.loc["2026-11-16":"2026-11-17"].tolist(), series.index.is_monotonic_increasing)

# Names of the axes and levels (MultiIndex preview)
pairs = pd.MultiIndex.from_tuples([("A", 1), ("A", 2), ("B", 1)], names=["group", "n"])
print(pairs.names, pairs.nlevels, len(pairs))

# EXPECTED OUTPUT
# Index(['a', 'b', 'c'], dtype='str', name='letters') letters str 3 (3,)
# a ['b', 'c'] True True True
# TypeError: Index does not support mutable operations
# RangeIndex(start=0, stop=5, step=1) 0 5 1 [10, 15]
# RangeIndex(start=0, stop=3, step=1) RangeIndex(start=0, stop=2, step=1)
# [1, 2, 3, 4, 5] [3, 4] [1, 2] [1, 2, 5]
# [1, 2, 3, 4, 3, 4, 5] [1, 99, 2, 3, 4] [2, 3, 4] [1, 3, 4]
# 1 [ 2  0 -1] [ True False False] ['A', 'B', 'C']
# ['A', 'B', 'C'] ['c', 'b', 'a'] ['a', 'b', 'c']
# False [1, 2] 3 slice(0, 2, None)
#     name
# id
# 101  Ann
# 102   Bo
# 103   Cy
# Bo id ['id', 'name']
# employee None
#      ID NAME
# r1  101  Ann
# r2  102   Bo
# r3  103   Cy
#         id NAME
# first  101  Ann
# r2     102   Bo
# r3     103   Cy
# ['r1', 'r2', 'r3'] ['ID', 'NAME'] Index(['ID', 'NAME'], dtype='str')
# ['Sunday', 'Monday', 'Tuesday', 'Wednesday'] [11, 11, 11, 11] [6, 0, 1, 2] ['15/11', '16/11', '17/11', '18/11']
# [2.0, 3.0] True
# ['group', 'n'] 2 3
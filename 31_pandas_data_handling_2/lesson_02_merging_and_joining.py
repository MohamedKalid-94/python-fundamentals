import numpy as np
import pandas as pd

# MERGING AND JOINING: combine tables by matching the VALUES of key columns (like a SQL JOIN)
#   left.merge(right, on="key", how="inner" | "left" | "right" | "outer" | "cross")
#   on="k"  /  on=["k1", "k2"]  /  left_on="a", right_on="b"  /  left_index=True, right_index=True
#   suffixes=("_x", "_y")   for columns with the same name      indicator=True   adds a "_merge" column
#   validate="one_to_one" | "one_to_many" | "many_to_one" | "many_to_many"    raises an error if the keys are not what you expect
#   left.join(right, on=... / how=..., lsuffix=, rsuffix=)    joins on the INDEX of the right table
#   pd.merge_asof(...)   match to the NEAREST earlier (or later) key, for times   pd.merge_ordered(...)
# how:  inner = only keys in both   left = all rows of the left table   right = all of the right   outer = all of both

people = pd.DataFrame({"id": [1, 2, 3, 4], "name": ["Ann", "Bo", "Cy", "Di"], "dept": ["IT", "HR", "IT", "Ops"]})
depts = pd.DataFrame({"dept": ["IT", "HR", "Fin"], "boss": ["Zed", "Yu", "Xi"]})
for how in ["inner", "left", "right", "outer"]:
    merged = people.merge(depts, on="dept", how=how)
    print(f"{how:<6}", len(merged), merged["name"].tolist(), merged["boss"].tolist())
print(people.merge(depts, on="dept", how="outer", sort=True)["dept"].tolist())

# Different key names, and keeping track of where the rows matched
orders = pd.DataFrame({"order": [10, 11, 12], "who": [2, 9, 1], "total": [5.5, 3.0, 8.25]})
by_name = orders.merge(people, left_on="who", right_on="id", how="left")
print(by_name[["order", "who", "id", "name"]])
print(orders.merge(people, left_on="who", right_on="id", how="outer", indicator=True)["_merge"].astype(str).tolist())
print(people.merge(depts, on="dept", how="left", indicator="where")["where"].astype(str).value_counts().to_dict())
anti = people.merge(depts, on="dept", how="left", indicator=True).query("_merge == 'left_only'")["name"].tolist()
print(anti, people[~people["dept"].isin(depts["dept"])]["name"].tolist())

# Columns with the same name
a = pd.DataFrame({"k": [1, 2], "v": [10, 20]})
b = pd.DataFrame({"k": [1, 2], "v": [100, 200]})
print(a.merge(b, on="k").columns.tolist(), a.merge(b, on="k", suffixes=("_old", "_new")).columns.tolist())

# Several keys, duplicate keys and validation
left = pd.DataFrame({"k1": ["a", "a", "b"], "k2": [1, 2, 1], "x": [1, 2, 3]})
right = pd.DataFrame({"k1": ["a", "b", "b"], "k2": [1, 1, 2], "y": [10, 20, 30]})
print(left.merge(right, on=["k1", "k2"]).values.tolist())
many = pd.DataFrame({"k": [1, 1, 2], "p": ["x", "y", "z"]})
other = pd.DataFrame({"k": [1, 1, 2], "q": ["a", "b", "c"]})
print(len(many.merge(other, on="k")))                                           # 2 x 2 + 1 = 5 rows: duplicate keys multiply
for rule in ["one_to_one", "many_to_one"]:
    try:
        many.merge(other.drop_duplicates("k"), on="k", validate=rule)
        print(rule, "ok")
    except pd.errors.MergeError as error:
        print(rule, "MergeError:", str(error)[:46])

# Merging on the index, and join
indexed = depts.set_index("dept")
print(people.join(indexed, on="dept")[["name", "boss"]].values.tolist())
print(people.set_index("dept").join(indexed, how="inner")["name"].tolist())
print(a.merge(b, left_index=True, right_index=True, suffixes=("_l", "_r")).columns.tolist(), a.join(b, lsuffix="_l", rsuffix="_r").columns.tolist())
print(a.merge(b, how="cross").shape, pd.DataFrame({"x": [1, 2]}).merge(pd.DataFrame({"y": ["a", "b", "c"]}), how="cross").shape)

# Missing keys: NaN matches NaN in pandas (in SQL, NULL never matches anything)
n_left = pd.DataFrame({"k": [1.0, np.nan], "a": ["p", "q"]})
n_right = pd.DataFrame({"k": [np.nan, 2.0], "b": ["r", "s"]})
print(n_left.merge(n_right, on="k").values.tolist())

# Keys of different types do not match
text_key = pd.DataFrame({"id": ["1", "2"], "t": ["x", "y"]})
number_key = pd.DataFrame({"id": [1, 2], "n": [5, 6]})
try:
    text_key.merge(number_key, on="id")
except ValueError as error:
    print("ValueError:", str(error)[:50])
print(text_key.assign(id=text_key["id"].astype(int)).merge(number_key, on="id").shape)

# merge_asof: for each trade, the latest quote at or before it
trades = pd.DataFrame({"time": pd.to_datetime(["2026-11-15 10:00:01", "2026-11-15 10:00:05", "2026-11-15 10:00:09"]), "qty": [100, 200, 50]})
quotes = pd.DataFrame({"time": pd.to_datetime(["2026-11-15 10:00:00", "2026-11-15 10:00:04", "2026-11-15 10:00:20"]), "price": [10.0, 10.5, 11.0]})
print(pd.merge_asof(trades, quotes, on="time")["price"].tolist())
print(pd.merge_asof(trades, quotes, on="time", direction="forward")["price"].tolist())
print(pd.merge_asof(trades, quotes, on="time", direction="nearest")["price"].tolist())
print(pd.merge_asof(trades, quotes, on="time", tolerance=pd.Timedelta("2s"))["price"].tolist())
sensors = pd.DataFrame({"t": [1, 3, 5], "s": ["a", "b", "a"], "reading": [1.0, 2.0, 3.0]})
calibration = pd.DataFrame({"t": [0, 2, 4], "s": ["a", "b", "a"], "offset": [0.1, 0.2, 0.3]})
print(pd.merge_asof(sensors, calibration, on="t", by="s")[["t", "s", "offset"]].values.tolist())
print(pd.merge_ordered(pd.DataFrame({"t": [1, 3], "a": [10, 30]}), pd.DataFrame({"t": [2, 3], "b": [2, 3]}), on="t", fill_method="ffill").values.tolist())

# Left join and the row count: check that you did not multiply or lose rows
checked = people.merge(depts, on="dept", how="left", validate="many_to_one")
print(len(checked) == len(people), checked["boss"].isna().sum())

# EXPECTED OUTPUT
# inner  3 ['Ann', 'Bo', 'Cy'] ['Zed', 'Yu', 'Zed']
# left   4 ['Ann', 'Bo', 'Cy', 'Di'] ['Zed', 'Yu', 'Zed', nan]
# right  4 ['Ann', 'Cy', 'Bo', nan] ['Zed', 'Zed', 'Yu', 'Xi']
# outer  5 [nan, 'Bo', 'Ann', 'Cy', 'Di'] ['Xi', 'Yu', 'Zed', 'Zed', nan]
# ['Fin', 'HR', 'IT', 'IT', 'Ops']
#    order  who   id name
# 0     10    2  2.0   Bo
# 1     11    9  NaN  NaN
# 2     12    1  1.0  Ann
# ['both', 'both', 'right_only', 'right_only', 'left_only']
# {'both': 3, 'left_only': 1}
# ['Di'] ['Di']
# ['k', 'v_x', 'v_y'] ['k', 'v_old', 'v_new']
# [['a', 1, 1, 10], ['b', 1, 3, 20]]
# 5
# one_to_one MergeError: Merge keys are not unique in left dataset; not
# many_to_one ok
# [['Ann', 'Zed'], ['Bo', 'Yu'], ['Cy', 'Zed'], ['Di', nan]]
# ['Ann', 'Bo', 'Cy']
# ['k_l', 'v_l', 'k_r', 'v_r'] ['k_l', 'v_l', 'k_r', 'v_r']
# (4, 4) (6, 2)
# [[nan, 'q', 'r']]
# ValueError: You are trying to merge on str and int64 columns f
# (2, 3)
# [10.0, 10.5, 10.5]
# [10.5, 11.0, 11.0]
# [10.0, 10.5, 10.5]
# [10.0, 10.5, nan]
# [[1, 'a', 0.1], [3, 'b', 0.2], [5, 'a', 0.3]]
# [[1.0, 10.0, nan], [2.0, 10.0, 2.0], [3.0, 30.0, 3.0]]
# True 1
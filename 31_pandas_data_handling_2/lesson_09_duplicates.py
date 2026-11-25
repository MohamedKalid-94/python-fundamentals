import numpy as np
import pandas as pd

# DUPLICATES: duplicated ROWS and duplicated LABELS
#   df.duplicated(subset=None, keep="first" | "last" | False)   a bool mask: True for the rows that repeat an earlier one
#   df.drop_duplicates(subset=None, keep="first", ignore_index=False)
#   s.unique()  s.nunique()  s.value_counts()  s.duplicated()
#   index.duplicated()  index.is_unique   df.columns.duplicated()   df.set_flags(allows_duplicate_labels=False)
# keep="first" marks every repeat after the first;  keep="last" marks every repeat before the last;  keep=False marks ALL copies.

df = pd.DataFrame({
    "id": [1, 2, 2, 3, 3, 3],
    "name": ["Ann", "Bo", "Bo", "Cy", "Cy", "Cy2"],
    "v": [10, 20, 20, 30, 31, 30],
})
print(df.duplicated().tolist(), df.duplicated().sum(), df.duplicated(keep="last").tolist(), df.duplicated(keep=False).tolist())
print(df.duplicated(subset=["id"]).tolist(), df.duplicated(subset=["id", "name"]).tolist(), df.duplicated(subset="v", keep=False).sum())
print(df.drop_duplicates().index.tolist(), df.drop_duplicates(keep="last").index.tolist(), df.drop_duplicates(keep=False).index.tolist())
print(df.drop_duplicates(subset="id")["name"].tolist(), df.drop_duplicates(subset="id", keep="last")["name"].tolist(), df.drop_duplicates(subset=["id"], ignore_index=True).index.tolist())
print(df[df.duplicated(keep=False)]["name"].tolist(), df[df.duplicated("id", keep=False)]["name"].tolist(), df.shape, df.drop_duplicates().shape)

# Counting the repeats
print(df["id"].value_counts().sort_index().to_dict(), df["id"].nunique(), df["id"].unique().tolist(), df["id"].duplicated().sum(), len(df) - df["id"].nunique())
counts = df.groupby("id").size()
print(counts[counts > 1].to_dict(), df.value_counts(subset=["id", "name"]).sort_index().to_dict())
print(df["id"].is_unique, df.drop_duplicates("id")["id"].is_unique, df.index.is_unique)

# Choosing WHICH row to keep: sort first, then keep the first
best = df.sort_values("v", ascending=False).drop_duplicates("id").sort_index()
print(best[["id", "v"]].values.tolist())
latest = df.sort_values("v").drop_duplicates("id", keep="last").sort_values("id")
print(latest[["id", "v"]].values.tolist())

# Near-duplicates: text that differs by case or spaces
people = pd.DataFrame({"email": ["a@x.com", "A@x.com ", "b@x.com", " a@X.com"], "n": [1, 2, 3, 4]})
print(people["email"].duplicated().sum(), people["email"].str.strip().str.lower().duplicated().sum())
tidy = people.assign(email=people["email"].str.strip().str.lower()).drop_duplicates("email")
print(tidy.values.tolist())

# Duplicates between two tables
old = pd.DataFrame({"id": [1, 2, 3]})
new = pd.DataFrame({"id": [3, 4, 5]})
print(new[new["id"].isin(old["id"])]["id"].tolist(), new[~new["id"].isin(old["id"])]["id"].tolist(), pd.concat([old, new]).drop_duplicates()["id"].tolist())
print(new.merge(old, on="id", how="left", indicator=True)["_merge"].astype(str).tolist())

# DUPLICATED LABELS
dup = pd.Series([10, 20, 30, 40], index=["a", "b", "a", "c"])
print(dup.index.is_unique, dup.index.duplicated().tolist(), dup["a"].tolist(), dup["b"], dup.loc[["a", "c"]].tolist())
print(dup[~dup.index.duplicated(keep="first")].tolist(), dup[~dup.index.duplicated(keep="last")].tolist(), dup.reset_index(drop=True).index.is_unique)
print(dup.index.get_loc("b"), dup.index.get_loc("a").tolist(), dup.groupby(level=0).sum().to_dict(), dup.groupby(level=0).first().to_dict())
try:
    dup.reindex(["a", "b"])
except ValueError as error:
    print("ValueError:", error)
print(dup.rename_axis("label").reset_index().values.tolist()[:2])

# Duplicated column names
wide = pd.DataFrame([[1, 2, 3]], columns=["x", "y", "x"])
print(wide.columns.duplicated().tolist(), wide["x"].values.tolist(), wide.loc[:, ~wide.columns.duplicated()].columns.tolist())
wide.columns = [f"{name}_{i}" for i, name in enumerate(wide.columns)]
print(wide.columns.tolist())
renamed = pd.concat([pd.DataFrame({"x": [1]}), pd.DataFrame({"x": [2]})], axis=1)
print(renamed.columns.tolist(), renamed["x"].shape)

# Refuse duplicate labels completely
safe = pd.DataFrame({"v": [1, 2]}, index=["a", "b"]).set_flags(allows_duplicate_labels=False)
print(safe.flags.allows_duplicate_labels)
try:
    safe.rename(index={"b": "a"})
except pd.errors.DuplicateLabelError as error:
    print("DuplicateLabelError:", str(error).splitlines()[0])
try:
    pd.concat([safe, safe])
except pd.errors.DuplicateLabelError as error:
    print("DuplicateLabelError:", str(error).splitlines()[0])

# EXPECTED OUTPUT
# [False, False, True, False, False, False] 1 [False, True, False, False, False, False] [False, True, True, False, False, False]
# [False, False, True, False, True, True] [False, False, True, False, True, False] 4
# [0, 1, 3, 4, 5] [0, 2, 3, 4, 5] [0, 3, 4, 5]
# ['Ann', 'Bo', 'Cy'] ['Ann', 'Bo', 'Cy2'] [0, 1, 2]
# ['Bo', 'Bo'] ['Bo', 'Bo', 'Cy', 'Cy', 'Cy2'] (6, 3) (5, 3)
# {1: 1, 2: 2, 3: 3} 3 [1, 2, 3] 3 3
# {2: 2, 3: 3} {(1, 'Ann'): 1, (2, 'Bo'): 2, (3, 'Cy'): 2, (3, 'Cy2'): 1}
# False True True
# [[1, 10], [2, 20], [3, 31]]
# [[1, 10], [2, 20], [3, 31]]
# 0 2
# [['a@x.com', 1], ['b@x.com', 3]]
# [3] [4, 5] [1, 2, 3, 4, 5]
# ['both', 'left_only', 'left_only']
# False [False, False, True, False] [10, 30] 20 [10, 30, 40]
# [10, 20, 40] [20, 30, 40] True
# 1 [True, False, True, False] {'a': 40, 'b': 20, 'c': 40} {'a': 10, 'b': 20, 'c': 40}
# ValueError: cannot reindex on an axis with duplicate labels
# [['a', 10], ['b', 20]]
# [False, False, True] [[1, 3]] ['x', 'y']
# ['x_0', 'y_1', 'x_2']
# ['x', 'x'] (1, 2)
# False
# DuplicateLabelError: Index has duplicates.
# DuplicateLabelError: Index has duplicates.
import numpy as np
import pandas as pd

# MODIFYING A DATAFRAME (every method that "changes" a table returns a NEW table: assign the result)
#   df["new"] = values         add or replace a column         df.assign(new=...)   add several, returns a copy (good for chains)
#   df.insert(pos, "new", v)   add a column at a position      df.loc[row, col] = v   change cells (a whole row or column too)
#   df.rename(columns=..., index=...)   df.astype(...)   df.replace(old, new)   df.fillna(...)   df.round(2)
# REMOVING
#   df.drop(columns=[...])  df.drop(index=[...])  df.drop(labels, axis=...)    by label
#   del df["c"]  df.pop("c")                                                     remove a column in place
#   df[mask]  df.loc[mask]                                                       keep the rows you want (the usual way to remove rows)
#   df.dropna()  df.drop_duplicates()  df.reset_index(drop=True)                 (more in Module 30)

df = pd.DataFrame({"name": ["Ann", "Bo", "Cy", "Di"], "age": [25, 31, 19, 44], "kg": [55.5, 70.2, 62.0, 81.3]})

# Adding columns
df["adult"] = df["age"] >= 21
df["bmi_like"] = (df["kg"] / 1.7 ** 2).round(1)
df["country"] = "IN"
print(df)
extra = df.assign(age_next=lambda d: d["age"] + 1, heavy=lambda d: d["kg"] > 70)
print(extra.columns.tolist(), df.columns.tolist())                               # assign leaves df alone
df.insert(1, "id", [101, 102, 103, 104])
print(df.columns.tolist())
df["rank"] = pd.Series([3, 1, 2, 4], index=[0, 1, 2, 3])
df["code"] = pd.Series({1: "x", 3: "z"})                                         # aligned on the index: others become NaN
print(df[["rank", "code"]])

# Changing values
df.loc[0, "kg"] = 56.0
df.loc[df["age"] > 40, "adult"] = True
df.loc[:, "country"] = "India"
df.loc[df["name"] == "Cy", ["age", "kg"]] = [20, 63.5]
df.iloc[3, df.columns.get_loc("name")] = "Dee"
print(df[["name", "age", "kg", "country"]])
print(df.replace({"Dee": "Di"})["name"].tolist(), df["age"].replace(19, 0).tolist(), df["age"].replace([20, 25], [1, 2]).tolist())
print(df.rename(columns={"kg": "weight"}).columns.tolist(), df.rename(index={0: "first"}).index.tolist()[:2])
print(df.astype({"age": "float64"}).dtypes["age"], df["kg"].round().astype(int).tolist(), df.round(0)["kg"].tolist())

# Removing columns
slim = df.drop(columns=["bmi_like", "country", "rank", "code", "id"])
print(slim.columns.tolist(), df.shape, slim.shape)
dropped = slim.drop(["adult"], axis=1)
print(dropped.columns.tolist())
popped = slim.pop("adult")
print(slim.columns.tolist(), popped.tolist())
del slim["kg"]
print(slim.columns.tolist())
try:
    df.drop(columns=["nope"])
except KeyError as error:
    print("KeyError:", str(error)[:46])
print(df.drop(columns=["nope"], errors="ignore").shape)

# Removing rows
people = pd.DataFrame({"name": ["Ann", "Bo", "Cy", "Di", "Ed"], "age": [25, 31, 19, 44, 38]}, index=["r1", "r2", "r3", "r4", "r5"])
print(people.drop(index=["r2", "r4"]).index.tolist(), people.drop("r1").shape, people.drop(index="r5")["name"].tolist())
print(people[people["age"] >= 30].index.tolist(), people[~people["name"].isin(["Ann", "Ed"])].index.tolist())
print(people.drop(people.index[people["age"] < 20]).index.tolist(), people.iloc[1:].index.tolist(), people.iloc[:-2].index.tolist())
print(people.drop(people.index[[0, 2]]).reset_index(drop=True))
print(people.loc[people["age"] != 44].reset_index(drop=True).index.tolist())
mixed = pd.DataFrame({"a": [1, np.nan, 3, 3], "b": [1, 2, np.nan, 3]})
print(mixed.dropna().index.tolist(), mixed.dropna(how="all").shape, mixed.dropna(subset=["a"]).index.tolist(), mixed.drop_duplicates().shape)

# inplace: it changes the object itself and returns None. Prefer reassigning: many methods are chained.
work = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
print(work.drop(columns="b", inplace=True), work.columns.tolist())
work = work.assign(c=lambda d: d["a"] * 10).rename(columns={"a": "x"})
print(work)

# Emptying and growing
print(work.iloc[0:0].shape, pd.concat([work, pd.DataFrame({"x": [9], "c": [90]})], ignore_index=True).shape)

# EXPECTED OUTPUT
#   name  age    kg  adult  bmi_like country
# 0  Ann   25  55.5   True      19.2      IN
# 1   Bo   31  70.2   True      24.3      IN
# 2   Cy   19  62.0  False      21.5      IN
# 3   Di   44  81.3   True      28.1      IN
# ['name', 'age', 'kg', 'adult', 'bmi_like', 'country', 'age_next', 'heavy'] ['name', 'age', 'kg', 'adult', 'bmi_like', 'country']
# ['name', 'id', 'age', 'kg', 'adult', 'bmi_like', 'country']
#    rank code
# 0     3  NaN
# 1     1    x
# 2     2  NaN
# 3     4    z
#   name  age    kg country
# 0  Ann   25  56.0   India
# 1   Bo   31  70.2   India
# 2   Cy   20  63.5   India
# 3  Dee   44  81.3   India
# ['Ann', 'Bo', 'Cy', 'Di'] [25, 31, 20, 44] [2, 31, 1, 44]
# ['name', 'id', 'age', 'weight', 'adult', 'bmi_like', 'country', 'rank', 'code'] ['first', 1]
# float64 [56, 70, 64, 81] [56.0, 70.0, 64.0, 81.0]
# ['name', 'age', 'kg', 'adult'] (4, 9) (4, 4)
# ['name', 'age', 'kg']
# ['name', 'age', 'kg'] [True, True, False, True]
# ['name', 'age']
# KeyError: "['nope'] not found in axis"
# (4, 9)
# ['r1', 'r3', 'r5'] (4, 2) ['Ann', 'Bo', 'Cy', 'Di']
# ['r2', 'r4', 'r5'] ['r2', 'r3', 'r4']
# ['r1', 'r2', 'r4', 'r5'] ['r2', 'r3', 'r4', 'r5'] ['r1', 'r2', 'r3']
#   name  age
# 0   Bo   31
# 1   Di   44
# 2   Ed   38
# [0, 1, 2, 3]
# [0, 3] (4, 2) [0, 2, 3] (4, 2)
# None ['a']
#    x   c
# 0  1  10
# 1  2  20
# (0, 2) (3, 2)
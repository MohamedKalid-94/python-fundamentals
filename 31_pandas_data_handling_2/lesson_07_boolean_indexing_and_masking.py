import functools

import numpy as np
import pandas as pd

# BOOLEAN INDEXING AND MASKING: a True/False Series (a MASK) chooses rows or cells
#   mask = df["age"] > 30                      comparisons give a bool Series (a missing value compares False)
#   (m1) & (m2)   (m1) | (m2)   ~m   m1 ^ m2    combine masks: ALWAYS use parentheses and & | ~, never and / or / not
#   df[mask]   df.loc[mask, "col"]   df.loc[mask, "col"] = value        choose, read one column, assign
#   isin  between  str.contains  isna  notna  eq ne lt le gt ge  any(axis=1)  all(axis=1)
#   where(cond, other)  keeps values where cond is True; mask(cond, other) replaces where it is True
#   np.where  np.select  df.query("age > 30 and city == 'Pune'")
#   mask.sum() counts, mask.mean() is the share

df = pd.DataFrame({
    "name": ["Ann", "Bo", "Cy", "Di", "Ed", "Fay"],
    "age": [25, 31, 19, 44, 38, np.nan],
    "city": ["Pune", "Goa", "Pune", "Delhi", "Goa", "Pune"],
    "score": [88, 92, 75, 60, 95, 70],
})
mask = df["age"] > 30
print(mask.tolist(), mask.dtype, mask.sum(), mask.mean().round(3), mask.any(), mask.all())
print(df[mask]["name"].tolist(), df.loc[mask, ["name", "score"]].values.tolist(), df.loc[mask, "score"].mean())
print(df[(df["age"] > 30) & (df["score"] > 90)]["name"].tolist(), df[(df["age"] < 20) | (df["score"] > 94)]["name"].tolist())
print(df[~(df["age"] > 30)]["name"].tolist(), df[(df["age"] > 30) ^ (df["score"] > 90)]["name"].tolist())

# The classic mistakes
try:
    df[df["age"] > 30 & df["score"] > 80]
except (TypeError, ValueError) as error:
    print(type(error).__name__, "(missing parentheses)")
try:
    df[(df["age"] > 30) and (df["score"] > 80)]
except ValueError as error:
    print("ValueError:", str(error)[:48])
print(df[~df["age"].isna() & ~(df["age"] > 30)]["name"].tolist(), df[df["age"].notna() & (df["age"] <= 30)]["name"].tolist())      # a missing age is not "<= 30" and not "> 30"

# Useful tests
print(df[df["city"].isin(["Goa", "Delhi"])]["name"].tolist(), df[~df["city"].isin(["Goa", "Delhi"])]["name"].tolist())
print(df[df["score"].between(70, 90)]["name"].tolist(), df[df["score"].between(70, 90, inclusive="neither")]["name"].tolist(), df[df["score"].between(70, 90, inclusive="left")]["name"].tolist())
print(df[df["name"].str.startswith("F") | df["name"].str.contains("y$")]["name"].tolist(), df[df["age"].isna()]["name"].tolist())
print(df["city"].eq("Pune").sum(), df["city"].ne("Pune").sum(), df["score"].gt(80).sum(), df["score"].le(70).sum(), df["score"].lt(df["score"].mean()).tolist())

# Whole-table masks
numbers = df[["age", "score"]]
print((numbers > 90).any(axis=1).tolist(), (numbers > 20).all(axis=1).tolist(), (numbers > 90).sum().to_dict(), numbers.isna().any(axis=1).sum())
print(df[(df[["age", "score"]] > 40).any(axis=1)]["name"].tolist(), df.loc[:, df.dtypes.map(pd.api.types.is_numeric_dtype)].columns.tolist(), df.loc[:, df.notna().all()].columns.tolist())
print(df.columns[df.columns.str.contains("a")].tolist(), df.filter(regex="^[ac]").columns.tolist())

# Changing values through a mask
copy = df.copy()
copy.loc[copy["score"] < 70, "score"] = 70
copy.loc[copy["age"].isna(), "age"] = copy["age"].mean()
copy.loc[copy["city"] == "Goa", ["city", "score"]] = ["GOA", 0]
print(copy["score"].tolist(), copy["age"].round(1).tolist(), copy["city"].tolist())
copy["band"] = "mid"
copy.loc[copy["score"] >= 90, "band"] = "high"
copy.loc[copy["score"] <= 70, "band"] = "low"
print(copy["band"].tolist())

# where, mask, np.where, np.select, clip
score = df["score"]
print(score.where(score >= 70).tolist(), score.where(score >= 70, 70).tolist(), score.mask(score >= 90, 90).tolist(), score.clip(70, 90).tolist())
print(np.where(score >= 90, "high", np.where(score >= 70, "mid", "low")).tolist(), np.select([score >= 90, score >= 70], ["high", "mid"], default="low").tolist())
print(df.where(df["score"] > 80)["name"].tolist(), df["age"].where(df["age"] > 30, 0).tolist())

# query: the same filters as a string
min_age = 30
print(df.query("age > @min_age and city == 'Goa'")["name"].tolist(), df.query("city in ['Pune', 'Delhi'] and score >= 70")["name"].tolist())
print(df.query("20 < age < 40")["name"].tolist(), df.query("not (age > 30)")["name"].tolist(), df.query("name.str.startswith('A')", engine="python")["name"].tolist())
print(df.query("index % 2 == 0")["name"].tolist(), df.rename(columns={"score": "total score"}).query("`total score` > 90")["name"].tolist())

# Masks on the index, and many conditions at once
print(df[df.index % 2 == 0]["name"].tolist(), df[df.index.isin([1, 3])]["name"].tolist(), df.loc[df.index > 3, "name"].tolist(), df.loc[lambda d: d["score"] > 90, "name"].tolist())
conditions = [df["score"] > 60, df["city"] == "Pune", df["age"].notna()]
print(df[functools.reduce(lambda a, b: a & b, conditions)]["name"].tolist(), df[np.logical_and.reduce(conditions)]["name"].tolist(), df[np.logical_or.reduce(conditions)].shape[0])

# A filtered table is a new table (copy-on-write): changing it leaves the original alone
subset = df[df["score"] > 90].copy()
subset.loc[:, "score"] = 0
print(df["score"].tolist(), subset["score"].tolist())

# Counting patterns: how many rows pass each rule, and which rows fail all of them
rules = pd.DataFrame({"adult": df["age"] >= 21, "good": df["score"] >= 80, "local": df["city"] == "Pune"})
print(rules.sum().to_dict(), rules.all(axis=1).sum(), rules.any(axis=1).sum(), df[~rules.any(axis=1)]["name"].tolist(), rules.sum(axis=1).tolist())

# EXPECTED OUTPUT
# [False, True, False, True, True, False] bool 3 0.5 True False
# ['Bo', 'Di', 'Ed'] [['Bo', 92], ['Di', 60], ['Ed', 95]] 82.33333333333333
# ['Bo', 'Ed'] ['Cy', 'Ed']
# ['Ann', 'Cy', 'Fay'] ['Di']
# ValueError (missing parentheses)
# ValueError: The truth value of a Series is ambiguous. Use a.
# ['Ann', 'Cy'] ['Ann', 'Cy']
# ['Bo', 'Di', 'Ed'] ['Ann', 'Cy', 'Fay']
# ['Ann', 'Cy', 'Fay'] ['Ann', 'Cy'] ['Ann', 'Cy', 'Fay']
# ['Cy', 'Fay'] ['Fay']
# 3 3 3 2 [False, False, True, True, False, True]
# [False, True, False, False, True, False] [True, True, False, True, True, False] {'age': 0, 'score': 2} 1
# ['Ann', 'Bo', 'Cy', 'Di', 'Ed', 'Fay'] ['age', 'score'] ['name', 'city', 'score']
# ['name', 'age'] ['age', 'city']
# [88, 0, 75, 70, 0, 70] [25.0, 31.0, 19.0, 44.0, 38.0, 31.4] ['Pune', 'GOA', 'Pune', 'Delhi', 'GOA', 'Pune']
# ['mid', 'low', 'mid', 'low', 'low', 'low']
# [88.0, 92.0, 75.0, nan, 95.0, 70.0] [88, 92, 75, 70, 95, 70] [88, 90, 75, 60, 90, 70] [88, 90, 75, 70, 90, 70]
# ['mid', 'high', 'mid', 'low', 'high', 'mid'] ['mid', 'high', 'mid', 'low', 'high', 'mid']
# ['Ann', 'Bo', nan, nan, 'Ed', nan] [0.0, 31.0, 0.0, 44.0, 38.0, 0.0]
# ['Bo', 'Ed'] ['Ann', 'Cy', 'Fay']
# ['Ann', 'Bo', 'Ed'] ['Ann', 'Cy', 'Fay'] ['Ann']
# ['Ann', 'Cy', 'Ed'] ['Bo', 'Ed']
# ['Ann', 'Cy', 'Ed'] ['Bo', 'Di'] ['Ed', 'Fay'] ['Bo', 'Ed']
# ['Ann', 'Cy'] ['Ann', 'Cy'] 6
# [88, 92, 75, 60, 95, 70] [0, 0]
# {'adult': 4, 'good': 3, 'local': 3} 1 6 [] [3, 2, 1, 1, 2, 1]
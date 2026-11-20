import numpy as np
import pandas as pd

# SORTING
#   df.sort_values(by, ascending=True, na_position="last", ignore_index=False, key=None, kind=...)
#   df.sort_index(axis=0 / 1, ascending=...)       s.sort_values()   s.sort_index()
#   s.rank(method="average" | "min" | "max" | "first" | "dense", ascending, pct)     s.argsort()
#   nlargest(n, columns, keep=)  nsmallest      s.searchsorted(values) on a SORTED series
# Ties: only kind="stable" promises that equal values keep their original order. A sort on several columns
# is stable for the columns after the first one.

df = pd.DataFrame(
    {"name": ["bo", "Ann", "cy", "Di", "Ed"], "dept": ["IT", "HR", "IT", "HR", "IT"], "salary": [50, 41, np.nan, 40, 60], "age": [31, 25, 44, 19, 38]},
    index=list("vwxyz"),
)
print(df.sort_values("age")["name"].tolist(), df.sort_values("age", ascending=False).index.tolist())
print(df.sort_values(["dept", "salary"], ascending=[True, False])["name"].tolist())
print(df.sort_values("salary")["name"].tolist(), df.sort_values("salary", na_position="first")["name"].tolist(), df.sort_values("salary", ascending=False)["name"].tolist())
print(df.sort_values("age", ignore_index=True).index.tolist())

# Sorting with a rule (key= is applied to the column before comparing; the data stay as they are)
print(df.sort_values("name")["name"].tolist(), df.sort_values("name", key=lambda s: s.str.lower())["name"].tolist())
print(df.sort_values("dept", key=lambda s: s.map({"IT": 0, "HR": 1}), kind="stable")["name"].tolist())
print(df.sort_values("dept", kind="stable")["name"].tolist(), df.sort_values(["dept", "age"])["name"].tolist())

# The index and the columns
print(df.sort_index(ascending=False).index.tolist(), df.sort_index(axis=1).columns.tolist(), df.sort_index(axis=1, ascending=False).columns.tolist())
scrambled = pd.Series([1, 2, 3], index=["b", "c", "a"])
print(scrambled.sort_index().tolist(), scrambled.sort_values(ascending=False).index.tolist(), scrambled.index.is_monotonic_increasing, scrambled.sort_index().index.is_monotonic_increasing)

# The largest and smallest
print(df.nlargest(2, "age")["name"].tolist(), df.nsmallest(2, "salary")["name"].tolist(), df.nlargest(2, ["salary", "age"])["name"].tolist())
tied = pd.DataFrame({"v": [3, 5, 5, 1]}, index=list("abcd"))
print(tied.nlargest(1, "v", keep="first").index.tolist(), tied.nlargest(1, "v", keep="all").index.tolist(), tied.nlargest(1, "v", keep="last").index.tolist())

# Ranks
scores = pd.Series([30, 10, 20, 10, 40], index=list("abcde"))
for method in ["average", "min", "max", "first", "dense"]:
    print(f"{method:<8}", scores.rank(method=method).tolist())
print(scores.rank(ascending=False, method="min").astype(int).tolist(), scores.rank(pct=True).round(2).tolist())
print(pd.Series([2.0, np.nan, 1.0]).rank().tolist(), pd.Series([2.0, np.nan, 1.0]).rank(na_option="bottom").tolist())

# argsort and searchsorted
print(scores.argsort(kind="stable").tolist(), scores.sort_values(kind="stable").index.tolist())
ordered = scores.sort_values()
print(ordered.searchsorted([5, 10, 25, 99]).tolist(), ordered.searchsorted(10, side="right"))
print(df["age"].is_monotonic_increasing, df.sort_values("age")["age"].is_monotonic_increasing)

# Sort dates as dates, not as text
dates = pd.DataFrame({"when": ["15/11/2026", "01/02/2027", "20/10/2026"]})
print(dates.sort_values("when")["when"].tolist())
print(dates.assign(when=pd.to_datetime(dates["when"], format="%d/%m/%Y")).sort_values("when")["when"].dt.strftime("%d/%m/%Y").tolist())

# Sort once, then slice by label (a sorted index is fast to search)
by_age = df.set_index("age").sort_index()
print(by_age.loc[25:38, "name"].tolist(), by_age.index.is_monotonic_increasing)

# EXPECTED OUTPUT
# ['Di', 'Ann', 'bo', 'Ed', 'cy'] ['x', 'z', 'v', 'w', 'y']
# ['Ann', 'Di', 'Ed', 'bo', 'cy']
# ['Di', 'Ann', 'bo', 'Ed', 'cy'] ['cy', 'Di', 'Ann', 'bo', 'Ed'] ['Ed', 'bo', 'Ann', 'Di', 'cy']
# [0, 1, 2, 3, 4]
# ['Ann', 'Di', 'Ed', 'bo', 'cy'] ['Ann', 'bo', 'cy', 'Di', 'Ed']
# ['bo', 'cy', 'Ed', 'Ann', 'Di']
# ['Ann', 'Di', 'bo', 'cy', 'Ed'] ['Di', 'Ann', 'bo', 'Ed', 'cy']
# ['z', 'y', 'x', 'w', 'v'] ['age', 'dept', 'name', 'salary'] ['salary', 'name', 'dept', 'age']
# [3, 1, 2] ['a', 'c', 'b'] False True
# ['cy', 'Ed'] ['Di', 'Ann'] ['Ed', 'bo']
# ['b'] ['b', 'c'] ['c']
# average  [4.0, 1.5, 3.0, 1.5, 5.0]
# min      [4.0, 1.0, 3.0, 1.0, 5.0]
# max      [4.0, 2.0, 3.0, 2.0, 5.0]
# first    [4.0, 1.0, 3.0, 2.0, 5.0]
# dense    [3.0, 1.0, 2.0, 1.0, 4.0]
# [2, 4, 3, 4, 1] [0.8, 0.3, 0.6, 0.3, 1.0]
# [2.0, nan, 1.0] [2.0, 3.0, 1.0]
# [1, 3, 2, 0, 4] ['b', 'd', 'c', 'a', 'e']
# [0, 0, 3, 5] 2
# False True
# ['01/02/2027', '15/11/2026', '20/10/2026']
# ['20/10/2026', '15/11/2026', '01/02/2027']
# ['Ann', 'bo', 'Ed'] True
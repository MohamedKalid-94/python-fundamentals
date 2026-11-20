import numpy as np
import pandas as pd

# FUNCTION APPLICATION AND AGGREGATIONS
#   s.map(dict_or_function)            element by element on a Series (the dict form is a lookup table)
#   df.map(function)                   element by element on a whole DataFrame   (the old applymap was removed in pandas 3)
#   s.apply(function)                  the same for functions of one value
#   df.apply(function, axis=0)         the function gets each COLUMN (a Series)     axis=1: each ROW
#   df.agg(...) / s.agg(...)           several summaries at once: names, functions or a dict per column
#   df.transform(function)             the result has the SAME SHAPE as the input (for example centering)
#   df.pipe(function, *args)           pass the whole table through your own function (a clean chain)
#   Always try a vectorized expression first: apply with a Python function runs a Python loop.

df = pd.DataFrame({"name": ["Ann", "Bo", "Cy", "Di"], "a": [1, 4, 9, 16], "b": [10.0, 20.0, 30.0, 40.0]})

# map and apply on a Series
print(df["a"].map(lambda v: v + 1).tolist(), df["name"].map({"Ann": "A", "Bo": "B"}).tolist(), df["name"].map(str.upper).tolist())
print(df["a"].apply(np.sqrt).tolist(), df["a"].apply(lambda v, k: v * k, k=10).tolist(), df["name"].apply(len).tolist())
print(pd.Series([1, None, 3]).map(lambda v: v * 2, na_action="ignore").tolist())
print(df["a"].map("{:03d}".format).tolist(), df["b"].map("{:.1f}%".format).tolist())

# DataFrame.map: every cell
print(df[["a", "b"]].map(lambda v: v * 2).values.tolist(), df.map(lambda v: len(str(v))).values.tolist())

# apply on columns and on rows
numbers = df[["a", "b"]]
print(numbers.apply(np.sum).to_dict(), numbers.apply(lambda column: column.max() - column.min()).to_dict())
print(numbers.apply(lambda row: row["a"] * row["b"], axis=1).tolist(), numbers.apply(np.sum, axis=1).tolist())
print(numbers.apply(lambda column: column / column.sum()).round(3).values.tolist())
print(numbers.apply(lambda row: pd.Series({"total": row["a"] + row["b"], "ratio": row["b"] / row["a"]}), axis=1).round(2).values.tolist())
print(df.apply(lambda row: f"{row['name']}={row['a']}", axis=1).tolist())
print(numbers.apply(lambda column: [column.min(), column.max()]).values.tolist(), numbers.apply(lambda column: column.min(), result_type="reduce").to_dict())
print(numbers.apply(np.sqrt, raw=True).round(2).values.tolist(), numbers.apply(lambda row: row.sum(), axis=1, raw=True).tolist())
print(numbers.apply(np.sum).equals(numbers.sum()), numbers.apply(lambda column: column - column.mean()).equals(numbers - numbers.mean()))

# AGGREGATIONS: agg / aggregate
print(numbers.agg("sum").to_dict(), numbers.agg(["min", "max"]).values.tolist())
print(numbers.agg({"a": "sum", "b": ["min", "max"]}))
print(numbers.agg(["mean", "std", lambda column: column.max() - column.min()]).round(2))
print(df["a"].agg(["min", "max", "mean"]).to_dict(), df["a"].agg("median"), df["a"].agg(lambda s: s.iloc[-1] - s.iloc[0]))
print(numbers.agg("sum", axis=1).tolist(), numbers.agg(np.mean).to_dict())
print(df.agg({"a": "sum", "name": "count"}).to_dict(), df.agg({"name": ["count", "nunique"]})["name"].to_dict())
named = numbers.agg(total_a=("a", "sum"), top_b=("b", "max"))
print(named)

# transform: same shape as the input
print(numbers.transform(lambda column: column - column.mean()).values.tolist())
print(numbers.transform(["sqrt", "exp"]).columns.tolist(), numbers.transform({"a": "sqrt", "b": lambda s: s / 10}).values.tolist())
print(numbers.transform(lambda column: (column - column.min()) / (column.max() - column.min())).round(2).values.tolist())
print(numbers.transform("cumsum").values.tolist(), numbers.transform("rank").values.tolist())

# pipe and assign: readable chains of steps
def add_ratio(frame, top, bottom):
    return frame.assign(ratio=frame[top] / frame[bottom])


def keep_large(frame, column, limit):
    return frame[frame[column] > limit]


result = (
    df
    .pipe(add_ratio, "b", "a")
    .pipe(keep_large, "ratio", 2.0)
    .assign(label=lambda d: d["name"].str.upper())
    .reset_index(drop=True)
)
print(result.round(3).values.tolist())

# eval: a formula for a whole column (fast for big tables)
print(df.eval("a * 2 + b").tolist(), df.assign(c=df.eval("b / a"))["c"].round(2).tolist(), df.eval("a > 3 and b < 40").tolist())

# Choosing the right tool
print((df["a"] * 2 + df["b"]).equals(df.eval("a * 2 + b")), df["a"].apply(lambda v: v * 2).equals(df["a"] * 2), np.sqrt(df["a"]).tolist() == df["a"].apply(np.sqrt).tolist())
vectorised_if = np.where(df["a"] > 5, "big", "small")
looped_if = df["a"].apply(lambda v: "big" if v > 5 else "small")
print(vectorised_if.tolist(), looped_if.tolist() == vectorised_if.tolist())

# EXPECTED OUTPUT
# [2, 5, 10, 17] ['A', 'B', nan, nan] ['ANN', 'BO', 'CY', 'DI']
# [1.0, 2.0, 3.0, 4.0] [10, 40, 90, 160] [3, 2, 2, 2]
# [2.0, nan, 6.0]
# ['001', '004', '009', '016'] ['10.0%', '20.0%', '30.0%', '40.0%']
# [[2.0, 20.0], [8.0, 40.0], [18.0, 60.0], [32.0, 80.0]] [[3, 1, 4], [2, 1, 4], [2, 1, 4], [2, 2, 4]]
# {'a': 30.0, 'b': 100.0} {'a': 15.0, 'b': 30.0}
# [10.0, 80.0, 270.0, 640.0] [11.0, 24.0, 39.0, 56.0]
# [[0.033, 0.1], [0.133, 0.2], [0.3, 0.3], [0.533, 0.4]]
# [[11.0, 10.0], [24.0, 5.0], [39.0, 3.33], [56.0, 2.5]]
# ['Ann=1', 'Bo=4', 'Cy=9', 'Di=16']
# [[1.0, 10.0], [16.0, 40.0]] {'a': 1.0, 'b': 10.0}
# [[1.0, 3.16], [2.0, 4.47], [3.0, 5.48], [4.0, 6.32]] [11.0, 24.0, 39.0, 56.0]
# True True
# {'a': 30.0, 'b': 100.0} [[1.0, 10.0], [16.0, 40.0]]
#         a     b
# sum  30.0   NaN
# min   NaN  10.0
# max   NaN  40.0
#               a      b
# mean       7.50  25.00
# std        6.56  12.91
# <lambda>  15.00  30.00
# {'min': 1.0, 'max': 16.0, 'mean': 7.5} 6.5 15
# [11.0, 24.0, 39.0, 56.0] {'a': 7.5, 'b': 25.0}
# {'a': 30, 'name': 4} {'count': 4, 'nunique': 4}
#             a     b
# total_a  30.0   NaN
# top_b     NaN  40.0
# [[-6.5, -15.0], [-3.5, -5.0], [1.5, 5.0], [8.5, 15.0]]
# [('a', 'sqrt'), ('a', 'exp'), ('b', 'sqrt'), ('b', 'exp')] [[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]]
# [[0.0, 0.0], [0.2, 0.33], [0.53, 0.67], [1.0, 1.0]]
# [[1.0, 10.0], [5.0, 30.0], [14.0, 60.0], [30.0, 100.0]] [[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]]
# [['Ann', 1, 10.0, 10.0, 'ANN'], ['Bo', 4, 20.0, 5.0, 'BO'], ['Cy', 9, 30.0, 3.333, 'CY'], ['Di', 16, 40.0, 2.5, 'DI']]
# [12.0, 28.0, 48.0, 72.0] [10.0, 5.0, 3.33, 2.5] [False, True, True, False]
# True True True
# ['small', 'small', 'big', 'big'] True
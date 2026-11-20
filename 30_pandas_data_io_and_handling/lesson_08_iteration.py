import timeit

import numpy as np
import pandas as pd

# ITERATION
#   for column in df                      the COLUMN NAMES (like a dict)         for value in series       the VALUES
#   df.items()                            (column name, Series) pairs            series.items()            (label, value) pairs
#   df.iterrows()                         (index, row as a Series): slow, and the row has ONE dtype
#   df.itertuples(index=True, name=...)   named tuples: much faster than iterrows, keeps the types
#   zip(df["a"], df["b"])                 fastest plain loop over several columns
#   df.to_dict("records")                 a list of dicts
# Prefer WHOLE-COLUMN operations. Loop only when each step really depends on the previous one, or for output.

df = pd.DataFrame({"id": [1, 2, 3], "name": ["Ann", "Bo", "Cy"], "score": [9.5, 7.25, 8.0]})
for column in df:
    print(column, end=" ")
print()
for name, values in df.items():
    print(name, values.dtype, values.tolist())
for value in df["name"]:
    print(value, end=" ")
print()
for label, value in df["score"].items():
    print(label, value, end="; ")
print()

# iterrows: a Series per row, so the types are mixed together
for index, row in df.iterrows():
    print(index, row["name"], row["score"], type(row["id"]).__name__)
print(next(df.iterrows())[1].dtype, next(df[["id", "score"]].iterrows())[1].dtype)           # ints become floats when mixed with floats

# itertuples: named tuples
for row in df.itertuples():
    print(row, row.Index, row.name, row.score)
for row in df.itertuples(index=False, name="Record"):
    print(row._asdict())
for row in df.itertuples(index=False, name=None):
    print(row, end=" ")
print()
odd = pd.DataFrame({"a b": [1], "class": [2], "ok": [3]})
print(next(odd.itertuples(index=False))._fields)                                             # names that are not valid identifiers are renamed

# zip, records, enumerate
for ident, name, score in zip(df["id"], df["name"], df["score"]):
    print(f"{ident}:{name}:{score}", end=" ")
print()
print(df.to_dict("records")[0], [record["name"] for record in df.to_dict("records")])
for position, (label, value) in enumerate(df["name"].items()):
    print(position, label, value, end="; ")
print()

# Changing a table while looping does not change it: build a new column instead
bonus = []
for score in df["score"]:
    bonus.append(score * 1.1)
df["bonus_loop"] = bonus
df["bonus_vector"] = df["score"] * 1.1
print(df["bonus_loop"].round(3).tolist(), df["bonus_loop"].equals(df["bonus_vector"]))
for index, row in df.iterrows():
    row["score"] = 0                                    # changes the temporary row only (copy-on-write)
print(df["score"].tolist())

# A loop that really needs the previous step: a running balance with a limit
amounts = pd.Series([50, -20, -100, 30, -10])
balance, history = 0, []
for amount in amounts:
    balance = max(0, balance + amount)
    history.append(balance)
print(history, amounts.cumsum().tolist())

# Speed: the vectorized form against iterrows and itertuples (prints True/False because times differ)
n = 20_000
table = pd.DataFrame({"a": np.arange(n), "b": np.arange(n) * 2})


def with_iterrows():
    return [row["a"] + row["b"] for _, row in table.iterrows()]


def with_itertuples():
    return [row.a + row.b for row in table.itertuples()]


def with_zip():
    return [a + b for a, b in zip(table["a"], table["b"])]


def vectorized():
    return (table["a"] + table["b"]).tolist()


times = {fn.__name__: min(timeit.repeat(fn, number=1, repeat=2)) for fn in (with_iterrows, with_itertuples, with_zip, vectorized)}
print(with_iterrows() == with_itertuples() == with_zip() == vectorized())
print(times["with_iterrows"] > 5 * times["with_itertuples"], times["with_itertuples"] > times["vectorized"], times["with_iterrows"] > 50 * times["vectorized"])

# EXPECTED OUTPUT
# id name score
# id int64 [1, 2, 3]
# name str ['Ann', 'Bo', 'Cy']
# score float64 [9.5, 7.25, 8.0]
# Ann Bo Cy
# 0 9.5; 1 7.25; 2 8.0;
# 0 Ann 9.5 int
# 1 Bo 7.25 int
# 2 Cy 8.0 int
# object float64
# Pandas(Index=0, id=1, name='Ann', score=9.5) 0 Ann 9.5
# Pandas(Index=1, id=2, name='Bo', score=7.25) 1 Bo 7.25
# Pandas(Index=2, id=3, name='Cy', score=8.0) 2 Cy 8.0
# {'id': 1, 'name': 'Ann', 'score': 9.5}
# {'id': 2, 'name': 'Bo', 'score': 7.25}
# {'id': 3, 'name': 'Cy', 'score': 8.0}
# (1, 'Ann', 9.5) (2, 'Bo', 7.25) (3, 'Cy', 8.0)
# ('_0', '_1', 'ok')
# 1:Ann:9.5 2:Bo:7.25 3:Cy:8.0
# {'id': 1, 'name': 'Ann', 'score': 9.5} ['Ann', 'Bo', 'Cy']
# 0 0 Ann; 1 1 Bo; 2 2 Cy;
# [10.45, 7.975, 8.8] True
# [9.5, 7.25, 8.0]
# [50, 30, 0, 30, 20] [50, 30, -70, -40, -50]
# True
# True True True
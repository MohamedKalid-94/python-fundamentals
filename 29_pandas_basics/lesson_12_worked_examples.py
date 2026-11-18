import numpy as np
import pandas as pd

# WORKED EXAMPLES that combine the lessons of this module

# 1. Clean a sensor table: ADC counts to volts and degrees, flag readings stuck at the rails
raw = pd.DataFrame({
    "time": ["10:00", "10:05", "10:10", "10:15", "10:20", "10:25"],
    "channel": ["a", "a", "a", "b", "b", "b"],
    "adc": [512, 530, 4095, 548, 560, 0],
})
table = raw.assign(
    volts=lambda d: (d["adc"] * 3.3 / 4095).round(3),
    valid=lambda d: ~d["adc"].isin([0, 4095]),
)
table["celsius"] = (table["volts"] * 100 - 50).where(table["valid"])
print(table)
good = table[table["valid"]].drop(columns="valid").reset_index(drop=True)
print(good.shape, round(float(good["celsius"].mean()), 3), round(float(good["celsius"].max()), 2))
print(table["valid"].sum(), (~table["valid"]).sum(), table.loc[~table["valid"], "time"].tolist())

# 2. Two sensors that report at different times: arithmetic aligns on the labels
a = pd.Series([20.1, 20.4, 20.9], index=[1, 2, 3], name="a")
b = pd.Series([20.0, 20.5, 21.0, 21.2], index=[2, 3, 4, 5], name="b")
difference = a - b
print(difference.round(2).to_dict())
print(a.sub(b, fill_value=0).round(2).to_dict(), difference.dropna().round(2).to_dict())
both = pd.DataFrame({"a": a, "b": b})
print(both)
print(both.dropna().mean().round(3).to_dict(), both["a"].combine_first(both["b"]).tolist())

# 3. One table, many formats
people = pd.DataFrame({"name": ["Ann", "Bo"], "age": [25, 31]})
print(people.to_dict(orient="records"), people.to_dict(orient="list"))
print(people.to_csv(index=False).splitlines(), people.to_json(orient="records"))
print(pd.DataFrame.from_records([("Cy", 19), ("Di", 44)], columns=["name", "age"]).to_numpy().tolist())
print(pd.DataFrame.from_dict({"x": {"r1": 1, "r2": 2}, "y": {"r1": 3, "r2": 4}}))
print(pd.DataFrame.from_dict({"r1": [1, 2], "r2": [3, 4]}, orient="index", columns=["x", "y"]).T.shape)

# 4. Rankings and filters
scores = pd.DataFrame({"team": list("ABCDE"), "points": [31, 25, 31, 18, 27], "games": [10, 9, 12, 8, 10]})
scores["per_game"] = (scores["points"] / scores["games"]).round(2)
print(scores.nlargest(3, "per_game")["team"].tolist(), scores.sort_values(["points", "team"], ascending=[False, True])["team"].tolist())
print(scores.query("points > 25 and games >= 10")["team"].tolist(), scores.loc[scores["per_game"].idxmax(), "team"])
print(scores.set_index("team").loc[["C", "A"], "points"].to_dict(), scores["points"].rank(method="min", ascending=False).astype(int).tolist())

# 5. A feature table for machine learning: scale the columns, then hand NumPy the numbers
features = pd.DataFrame({"height": [150, 160, 170, 180], "weight": [50, 60, 80, 90]})
scaled = (features - features.mean()) / features.std()
print(scaled.round(3))
matrix = scaled.to_numpy(copy=True)
print(matrix.shape, matrix.dtype, np.allclose(matrix.mean(axis=0), 0), np.allclose(matrix.std(axis=0, ddof=1), 1))
labels = pd.Series(["low", "high", "high", "low"], name="class")
print(labels.value_counts().to_dict(), labels.map({"low": 0, "high": 1}).tolist())

# EXPECTED OUTPUT
#     time channel   adc  volts  valid  celsius
# 0  10:00       a   512  0.413   True     -8.7
# 1  10:05       a   530  0.427   True     -7.3
# 2  10:10       a  4095  3.300  False      NaN
# 3  10:15       b   548  0.442   True     -5.8
# 4  10:20       b   560  0.451   True     -4.9
# 5  10:25       b     0  0.000  False      NaN
# (4, 5) -6.675 -4.9
# 4 2 ['10:10', '10:25']
# {1: nan, 2: 0.4, 3: 0.4, 4: nan, 5: nan}
# {1: 20.1, 2: 0.4, 3: 0.4, 4: -21.0, 5: -21.2} {2: 0.4, 3: 0.4}
#       a     b
# 1  20.1   NaN
# 2  20.4  20.0
# 3  20.9  20.5
# 4   NaN  21.0
# 5   NaN  21.2
# {'a': 20.65, 'b': 20.25} [20.1, 20.4, 20.9, 21.0, 21.2]
# [{'name': 'Ann', 'age': 25}, {'name': 'Bo', 'age': 31}] {'name': ['Ann', 'Bo'], 'age': [25, 31]}
# ['name,age', 'Ann,25', 'Bo,31'] [{"name":"Ann","age":25},{"name":"Bo","age":31}]
# [['Cy', 19], ['Di', 44]]
#     x  y
# r1  1  3
# r2  2  4
# (2, 2)
# ['A', 'B', 'E'] ['A', 'C', 'E', 'B', 'D']
# ['A', 'C', 'E'] A
# {'C': 31, 'A': 31} [1, 4, 1, 5, 3]
#    height  weight
# 0  -1.162  -1.095
# 1  -0.387  -0.548
# 2   0.387   0.548
# 3   1.162   1.095
# (4, 2) float64 True True
# {'low': 2, 'high': 2} [0, 1, 1, 0]
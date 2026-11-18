import numpy as np
import pandas as pd

# BASIC FUNCTIONALITY: the first things you do with any table
#   look      head tail info describe shape dtypes columns index len
#   counts    count value_counts nunique unique duplicated isna notna
#   summary   sum mean median min max std var quantile idxmin idxmax cumsum cummax (axis=0 columns, axis=1 rows)
#   order     sort_values(by=) sort_index() rank() nlargest()
#   copying   copy() equals()   iterating: items() iterrows() itertuples()   (loops are slow: prefer whole-column operations)
#   rounding  round() clip() abs()      pipe(function)

df = pd.DataFrame({
    "sensor": ["A", "B", "A", "C", "B", "A"],
    "temp": [21.5, 19.0, np.nan, 25.5, 19.5, 22.0],
    "ok": [True, True, False, True, True, True],
    "reads": [10, 7, 3, 9, 8, 12],
})
print(df)
print(len(df), df.shape, df.size, df.empty, df.columns.tolist(), df.dtypes.astype(str).to_dict())

# Counting
print(df.count().to_dict(), df["sensor"].value_counts().to_dict(), df["sensor"].nunique(), df["sensor"].unique().tolist())
print(df["sensor"].value_counts(normalize=True).round(3).to_dict(), df["ok"].value_counts().to_dict())
print(df.isna().sum().to_dict(), df["temp"].notna().sum(), df.isna().any(axis=1).tolist(), df.duplicated(subset="sensor").tolist())

# Summary numbers (missing values are skipped by default)
print(df["temp"].sum(), df["temp"].mean(), df["temp"].median(), df["temp"].min(), df["temp"].max(), round(df["temp"].std(), 3))
print(df["temp"].sum(skipna=False), df["temp"].quantile([0.25, 0.75]).tolist(), df["temp"].idxmax(), df["temp"].idxmin())
print(df[["temp", "reads"]].mean().round(2).to_dict(), df[["temp", "reads"]].sum(axis=1).tolist())
print(df.sum(numeric_only=True).to_dict())
print(df["reads"].cumsum().tolist(), df["reads"].cummax().tolist(), df["reads"].diff().tolist())
print(df.agg({"temp": ["min", "max"], "reads": ["sum", "mean"]}))
print(df[["temp", "reads"]].agg(["min", "max"]).round(1).values.tolist())

# Order
print(df.sort_values("reads")["reads"].tolist(), df.sort_values("reads", ascending=False).index.tolist())
print(df.sort_values(["sensor", "reads"], ascending=[True, False])["reads"].tolist(), df.sort_values("temp", na_position="first").index.tolist())
print(df.sort_index(ascending=False).index.tolist(), df["reads"].rank(ascending=False).tolist(), df.nlargest(2, "reads").index.tolist())

# Changing the numbers
print(df["temp"].round().tolist(), df["temp"].clip(20, 24).tolist(), (df["temp"] - 21).abs().round(1).tolist())
print(df["temp"].fillna(df["temp"].mean()).round(2).tolist(), df["temp"].between(20, 25).tolist())

# Copies and comparison
copy = df.copy()
copy.loc[0, "reads"] = 99
print(df.loc[0, "reads"], copy.loc[0, "reads"], df.equals(df.copy()), df.equals(copy))

# Iterating (to see the idea; prefer vectorized code)
for name, value in df[["sensor", "reads"]].items():
    print(name, value.tolist()[:2])
for row in df.head(2).itertuples():
    print(row.Index, row.sensor, row.temp)
for index, row in df.head(1).iterrows():
    print(index, row["sensor"], row["reads"])

# pipe: chain your own functions
def normalise(frame, column):
    return frame.assign(**{column + "_z": (frame[column] - frame[column].mean()) / frame[column].std()})

print(df.pipe(normalise, "reads")["reads_z"].round(3).tolist())
print(df.columns.str.upper().tolist(), df.select_dtypes("number").columns.tolist(), df["sensor"].str.lower().tolist())

# EXPECTED OUTPUT
#   sensor  temp     ok  reads
# 0      A  21.5   True     10
# 1      B  19.0   True      7
# 2      A   NaN  False      3
# 3      C  25.5   True      9
# 4      B  19.5   True      8
# 5      A  22.0   True     12
# 6 (6, 4) 24 False ['sensor', 'temp', 'ok', 'reads'] {'sensor': 'str', 'temp': 'float64', 'ok': 'bool', 'reads': 'int64'}
# {'sensor': 6, 'temp': 5, 'ok': 6, 'reads': 6} {'A': 3, 'B': 2, 'C': 1} 3 ['A', 'B', 'C']
# {'A': 0.5, 'B': 0.333, 'C': 0.167} {True: 5, False: 1}
# {'sensor': 0, 'temp': 1, 'ok': 0, 'reads': 0} 5 [False, False, True, False, False, False] [False, False, True, False, True, True]
# 107.5 21.5 21.5 19.0 25.5 2.574
# nan [19.5, 22.0] 3 1
# {'temp': 21.5, 'reads': 8.17} [31.5, 26.0, 3.0, 34.5, 27.5, 34.0]
# {'temp': 107.5, 'ok': 5.0, 'reads': 49.0}
# [10, 17, 20, 29, 37, 49] [10, 10, 10, 10, 10, 12] [nan, -3.0, -4.0, 6.0, -1.0, 4.0]
#       temp      reads
# min   19.0        NaN
# max   25.5        NaN
# sum    NaN  49.000000
# mean   NaN   8.166667
# [[19.0, 3.0], [25.5, 12.0]]
# [3, 7, 8, 9, 10, 12] [5, 0, 3, 4, 1, 2]
# [12, 10, 3, 8, 7, 9] [2, 1, 4, 0, 5, 3]
# [5, 4, 3, 2, 1, 0] [2.0, 5.0, 6.0, 3.0, 4.0, 1.0] [5, 0]
# [22.0, 19.0, nan, 26.0, 20.0, 22.0] [21.5, 20.0, nan, 24.0, 20.0, 22.0] [0.5, 2.0, nan, 4.5, 1.5, 1.0]
# [21.5, 19.0, 21.5, 25.5, 19.5, 22.0] [True, False, False, False, False, True]
# 10 99 True False
# sensor ['A', 'B']
# reads [10, 7]
# 0 A 21.5
# 1 B 19.0
# 0 A 10
# [0.599, -0.381, -1.688, 0.272, -0.054, 1.253]
# ['SENSOR', 'TEMP', 'OK', 'READS'] ['temp', 'reads'] ['a', 'b', 'a', 'c', 'b', 'a']
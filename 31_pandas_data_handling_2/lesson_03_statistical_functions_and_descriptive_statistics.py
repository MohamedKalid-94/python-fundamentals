import numpy as np
import pandas as pd

# STATISTICAL FUNCTIONS AND DESCRIPTIVE STATISTICS
#   centre     mean  median  mode        spread   std  var  sem  min  max  ptp-like: max - min  IQR
#   position   quantile  describe(percentiles=)  nlargest  idxmax        shape   skew  kurt
#   relation   corr (pearson, spearman)  cov  corrwith  autocorr
#   counts     count  nunique  value_counts(normalize=)  mode
#   change     diff  pct_change  cumsum  cumprod  cummax  rank
#   options    skipna=True (missing values are ignored)  numeric_only=True  ddof=1 (std and var use n - 1)  min_count=
# Unlike NumPy, pandas uses ddof=1 (the SAMPLE standard deviation) by default.

df = pd.DataFrame({
    "temp": [21.0, 22.5, 19.0, 25.0, 22.5, 30.0, np.nan],
    "hum": [40, 42, 45, 38, 41, 30, 44],
    "site": ["a", "a", "b", "b", "a", "b", "a"],
})
print(df.describe().round(2))
print(df.describe(percentiles=[0.1, 0.5, 0.9]).loc[["10%", "50%", "90%"], "temp"].tolist())
print([str(v) for v in df.describe(include="all").loc[["count", "unique", "top", "freq"], "site"]], df.describe(exclude="number").columns.tolist())

# Centre and spread
t = df["temp"]
print(t.mean(), t.median(), t.mode().tolist(), t.min(), t.max(), t.max() - t.min())
print(round(t.std(), 4), round(t.std(ddof=0), 4), round(t.var(), 4), round(t.sem(), 4), np.std(t.dropna()), round(t.dropna().std(), 4))
print(t.quantile(0.5), t.quantile([0.25, 0.75]).tolist(), t.quantile(0.75) - t.quantile(0.25), t.quantile(0.5, interpolation="lower"))
print(round(t.skew(), 4), round(t.kurt(), 4), t.count(), t.size, t.nunique(), t.isna().sum())
print(t.sum(), t.sum(skipna=False), pd.Series([np.nan, np.nan]).sum(), pd.Series([np.nan, np.nan]).sum(min_count=1), t.prod())
print(df[["temp", "hum"]].mean().round(2).to_dict(), df[["temp", "hum"]].mean(axis=1).round(2).tolist()[:3], df.mean(numeric_only=True).round(2).to_dict())
print(df[["temp", "hum"]].agg(["mean", "median", "std"]).round(2).values.tolist())
print(df["site"].mode().tolist(), df["site"].value_counts().to_dict(), df["site"].value_counts(normalize=True).round(3).to_dict(), df["hum"].mode().tolist())

# Position and extremes
print(t.idxmax(), t.idxmin(), df.loc[t.idxmax(), "site"], t.nlargest(2).tolist(), t.nsmallest(2).tolist(), t.rank(method="min").tolist())
print(df["hum"].between(40, 44).sum(), (df["hum"] > df["hum"].mean()).mean().round(3), df["hum"].is_monotonic_increasing)

# Relationships
print(df[["temp", "hum"]].corr().round(3).values.tolist(), round(df["temp"].corr(df["hum"]), 4))
print(df[["temp", "hum"]].corr(method="spearman").round(3).values.tolist(), df[["temp", "hum"]].cov().round(2).values.tolist())
print(df["temp"].corr(df["hum"], min_periods=10), round(df[["temp"]].corrwith(df["hum"]).iloc[0], 4))
steady = pd.Series([1, 2, 3, 4, 5, 6, 7, 8.0])
print(round(steady.autocorr(), 3), round(steady.autocorr(lag=2), 3), steady.corr(steady[::-1].reset_index(drop=True)))

# Change over the rows
s = pd.Series([100, 110, 99, 120.0])
print(s.diff().tolist(), s.diff(2).tolist(), s.pct_change().round(3).tolist(), s.cumsum().tolist(), s.cummax().tolist(), s.cummin().tolist())
print(s.shift(1).tolist(), (s / s.iloc[0] - 1).round(3).tolist(), s.cumprod().iloc[-1])

# Standardising and normalising a column
z = (df["hum"] - df["hum"].mean()) / df["hum"].std()
print(z.round(2).tolist(), round(z.mean(), 6) + 0.0, round(z.std(), 6))
print(((df["hum"] - df["hum"].min()) / (df["hum"].max() - df["hum"].min())).round(2).tolist())

# Outliers with the IQR rule and with the z-score
q1, q3 = df["hum"].quantile([0.25, 0.75])
low, high = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
print(low, high, df.loc[(df["hum"] < low) | (df["hum"] > high), "hum"].tolist(), df.loc[z.abs() > 1.5, "hum"].tolist())

# Same numbers as NumPy, with the ddof difference
print(round(df["hum"].std(), 4), round(np.std(df["hum"]), 4), round(np.std(df["hum"], ddof=1), 4), df["hum"].to_numpy().std() == df["hum"].std(ddof=0))

# EXPECTED OUTPUT
#         temp   hum
# count   6.00   7.0
# mean   23.33  40.0
# std     3.82   5.0
# min    19.00  30.0
# 25%    21.38  39.0
# 50%    22.50  41.0
# 75%    24.38  43.0
# max    30.00  45.0
# [20.0, 22.5, 27.5]
# ['7', '2', 'a', '4'] ['site']
# 23.333333333333332 22.5 [22.5] 19.0 30.0 11.0
# 3.8166 3.4841 14.5667 1.5581 3.4840908267278117 3.8166
# 22.5 [21.375, 24.375] 3.0 22.5
# 1.11 1.5561 6 7 5 1
# 140.0 nan 0.0 nan 151495312.5
# {'temp': 23.33, 'hum': 40.0} [30.5, 32.25, 32.0] {'temp': 23.33, 'hum': 40.0}
# [[23.33, 40.0], [22.5, 41.0], [3.82, 5.0]]
# ['a'] {'a': 4, 'b': 3} {'a': 0.571, 'b': 0.429} [30, 38, 40, 41, 42, 44, 45]
# 5 2 b [30.0, 25.0] [19.0, 21.0] [2.0, 3.0, 1.0, 5.0, 3.0, 6.0, nan]
# 4 0.571 False
# [[1.0, -0.963], [-0.963, 1.0]] -0.9628
# [[1.0, -0.812], [-0.812, 1.0]] [[14.57, -18.83], [-18.83, 25.0]]
# nan -0.9628
# 1.0 1.0 -1.0
# [nan, 10.0, -11.0, 21.0] [nan, nan, -1.0, 10.0] [nan, 0.1, -0.1, 0.212] [100.0, 210.0, 309.0, 429.0] [100.0, 110.0, 110.0, 120.0] [100.0, 100.0, 99.0, 99.0]
# [nan, 100.0, 110.0, 99.0] [0.0, 0.1, -0.01, 0.2] 130680000.0
# [0.0, 0.4, 1.0, -0.4, 0.2, -2.0, 0.8] 0.0 1.0
# [0.67, 0.8, 1.0, 0.53, 0.73, 0.0, 0.93]
# 33.0 49.0 [30] [30]
# 5.0 4.6291 5.0 True
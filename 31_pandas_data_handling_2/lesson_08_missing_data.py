import numpy as np
import pandas as pd

# MISSING DATA: NaN (float columns, text columns), None, NaT (dates), pd.NA (nullable types)
#   find      isna() notna()   isna().sum()   isna().mean()   isna().any(axis=1)         pd.isna(x)
#   fill      fillna(value | dict | Series)   ffill(limit=)  bfill(limit=)   interpolate(...)   replace(old, np.nan)
#   remove    dropna(how="any" | "all", thresh=, subset=, axis=)
#   rules     sum, mean, min, max, cumsum skip missing values (skipna=True); a comparison with NaN is False;
#             NaN == NaN is False but Series.equals treats missing values in the same place as equal
#   types     an integer column with a missing value becomes float; Int64 / boolean / string keep pd.NA
# fillna(method="ffill") was removed: call ffill() and bfill().

s = pd.Series([1.0, np.nan, 3.0, np.nan, np.nan, 6.0])
print(s.isna().tolist(), s.notna().sum(), s.isna().mean().round(3), pd.isna(None), pd.isna(np.nan), pd.isna(pd.NaT), pd.isna(""), np.nan == np.nan)
print(s.sum(), s.mean(), s.count(), s.cumsum().tolist(), (s > 2).tolist(), s.max(), s.sum(skipna=False))
print(pd.Series([1.0, np.nan]).equals(pd.Series([1.0, np.nan])), (pd.Series([1.0, np.nan]) == pd.Series([1.0, np.nan])).tolist())

# Filling
print(s.fillna(0).tolist(), s.fillna(s.mean()).tolist(), s.fillna(s.median()).round(2).tolist())
print(s.ffill().tolist(), s.bfill().tolist(), s.ffill(limit=1).tolist(), s.bfill(limit=1).tolist())
print(s.interpolate().tolist(), s.interpolate(limit=1).tolist(), s.interpolate(limit_direction="backward").tolist())
print(pd.Series([np.nan, 2.0, np.nan, 4.0, np.nan]).interpolate(limit_direction="both").tolist(), pd.Series([np.nan, 2.0, np.nan, 4.0, np.nan]).interpolate(limit_area="inside").tolist())
try:
    s.fillna(method="ffill")
except TypeError as error:
    print("TypeError:", str(error)[:40])

# Interpolating by the VALUES of the index (uneven times)
uneven = pd.Series([1.0, np.nan, np.nan, 10.0], index=[0, 1, 2, 9])
print(uneven.interpolate().tolist(), uneven.interpolate(method="index").round(3).tolist())
timed = pd.Series([1.0, np.nan, 5.0], index=pd.to_datetime(["2026-11-15 10:00", "2026-11-15 10:10", "2026-11-15 11:00"]))
print(timed.interpolate(method="time").round(3).tolist(), timed.interpolate().tolist())

# Tables
df = pd.DataFrame({"a": [1.0, np.nan, 3.0, np.nan], "b": [np.nan, 2.0, 3.0, np.nan], "c": ["x", None, "z", "w"], "d": [1, 2, 3, 4]})
print(df.isna().sum().to_dict(), df.isna().mean().round(2).to_dict(), df.isna().any(axis=1).tolist(), df.isna().all(axis=1).tolist(), int(df.isna().sum().sum()))
print(df[["a", "b", "d"]].fillna(0).values.tolist())             # fill the numbers; fill text with a word, not 0
print(df.fillna({"a": 0, "b": df["b"].mean(), "c": "unknown"}).values.tolist())
print(df.fillna(df.mean(numeric_only=True)).round(2).values.tolist(), df.fillna(df.iloc[2]).values.tolist()[0])
print(df.ffill().values.tolist()[3], df.bfill().values.tolist()[0], df[["a", "b"]].interpolate().values.tolist())
print(df["a"].fillna(df["b"]).tolist(), df["a"].combine_first(df["b"]).tolist())

# Removing
print(df.dropna().shape, df.dropna(how="all").shape, df.dropna(subset=["a"]).shape, df.dropna(subset=["a", "b"], how="all").shape, df.dropna(thresh=3).shape, df.dropna(axis=1).columns.tolist(), df.dropna(axis=1, how="all").shape)
print(df.dropna(subset=["a"]).index.tolist(), df.dropna(thresh=3).index.tolist(), df.dropna().reset_index(drop=True).shape)

# Replacing markers by real missing values
messy = pd.DataFrame({"t": [21.5, -999, 22.0], "label": ["ok", "N/A", "-"], "n": ["1", "", "3"]})
print(messy.replace(-999, np.nan)["t"].tolist(), messy.replace({"N/A": np.nan, "-": np.nan})["label"].tolist(), messy["n"].replace("", np.nan).tolist())
print(messy.replace({"t": {-999: np.nan}, "label": {"N/A": "missing", "-": "missing"}}).values.tolist(), messy.replace(r"^\s*$", np.nan, regex=True)["n"].tolist())
print(pd.to_numeric(messy["n"], errors="coerce").tolist(), messy["t"].where(messy["t"] > 0).tolist())

# Types
print(pd.Series([1, None, 3]).dtype, pd.Series([1, None, 3], dtype="Int64").tolist(), pd.Series([1, None, 3], dtype="Int64").sum(), pd.Series([1, None, 3]).convert_dtypes().dtype)
print(pd.Series([1, None, 3]).fillna(0).dtype, pd.Series([1, None, 3]).fillna(0).astype(int).tolist(), pd.Series([True, None, False]).dtype, pd.Series(pd.to_datetime(["2026-11-15", None])).isna().tolist())
print(pd.Series(["a", None]).isna().tolist(), pd.Series(["a", None], dtype="string").tolist(), pd.NA + 1, pd.Series([1.5, None], dtype="Float64").tolist())

# Keep a record of what was missing before you fill it
filled = df.assign(a_missing=df["a"].isna(), a=df["a"].fillna(df["a"].mean()))
print(filled[["a", "a_missing"]].values.tolist())
group_filled = pd.DataFrame({"g": ["p", "p", "q", "q"], "x": [1.0, np.nan, 10.0, np.nan]})
print(group_filled.groupby("g")["x"].transform(lambda part: part.fillna(part.mean())).tolist())                     # a preview of Module 32

# EXPECTED OUTPUT
# [False, True, False, True, True, False] 3 0.5 True True True False False
# 10.0 3.3333333333333335 3 [1.0, nan, 4.0, nan, nan, 10.0] [False, False, True, False, False, True] 6.0 nan
# True [True, False]
# [1.0, 0.0, 3.0, 0.0, 0.0, 6.0] [1.0, 3.3333333333333335, 3.0, 3.3333333333333335, 3.3333333333333335, 6.0] [1.0, 3.0, 3.0, 3.0, 3.0, 6.0]
# [1.0, 1.0, 3.0, 3.0, 3.0, 6.0] [1.0, 3.0, 3.0, 6.0, 6.0, 6.0] [1.0, 1.0, 3.0, 3.0, nan, 6.0] [1.0, 3.0, 3.0, nan, 6.0, 6.0]
# [1.0, 2.0, 3.0, 4.0, 5.0, 6.0] [1.0, 2.0, 3.0, 4.0, nan, 6.0] [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
# [2.0, 2.0, 3.0, 4.0, 4.0] [nan, 2.0, 3.0, 4.0, nan]
# TypeError: NDFrame.fillna() got an unexpected keywo
# [1.0, 4.0, 7.0, 10.0] [1.0, 2.0, 3.0, 10.0]
# [1.0, 1.667, 5.0] [1.0, 3.0, 5.0]
# {'a': 2, 'b': 2, 'c': 1, 'd': 0} {'a': 0.5, 'b': 0.5, 'c': 0.25, 'd': 0.0} [True, True, False, True] [False, False, False, False] 5
# [[1.0, 0.0, 1.0], [0.0, 2.0, 2.0], [3.0, 3.0, 3.0], [0.0, 0.0, 4.0]]
# [[1.0, 2.5, 'x', 1], [0.0, 2.0, 'unknown', 2], [3.0, 3.0, 'z', 3], [0.0, 2.5, 'w', 4]]
# [[1.0, 2.5, 'x', 1], [2.0, 2.0, nan, 2], [3.0, 3.0, 'z', 3], [2.0, 2.5, 'w', 4]] [1.0, 3.0, 'x', 1]
# [3.0, 3.0, 'w', 4] [1.0, 2.0, 'x', 1] [[1.0, nan], [2.0, 2.0], [3.0, 3.0], [3.0, 3.0]]
# [1.0, 2.0, 3.0, nan] [1.0, 2.0, 3.0, nan]
# (1, 4) (4, 4) (2, 4) (3, 4) (2, 4) ['d'] (4, 4)
# [0, 2] [0, 2] (1, 4)
# [21.5, nan, 22.0] ['ok', nan, nan] ['1', nan, '3']
# [[21.5, 'ok', '1'], [nan, 'missing', ''], [22.0, 'missing', '3']] ['1', nan, '3']
# [1.0, nan, 3.0] [21.5, nan, 22.0]
# float64 [1, <NA>, 3] 4 Int64
# float64 [1, 0, 3] object [False, True]
# [False, True] ['a', <NA>] <NA> [1.5, <NA>]
# [[1.0, False], [2.0, True], [3.0, False], [2.0, True]]
# [1.0, 1.0, 10.0, 10.0]
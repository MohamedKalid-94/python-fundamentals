import warnings

import numpy as np
import pandas as pd

# PANDAS 3: THE RULES THAT CHANGED (older books and videos show the old behaviour)
#
# 1. COPY-ON-WRITE (always on). A result NEVER changes the table it came from.
#      df["a"], df[mask], df.loc[...], df.drop(...) all behave like independent copies (pandas copies lazily, only when needed)
#      so there is no SettingWithCopyWarning any more, and chained assignment  df["a"][0] = 1  has NO effect.
#      Change a table with ONE step:  df.loc[row, col] = value
# 2. A "str" DTYPE for text (it was "object"). Missing text is NaN. If the pyarrow package is installed pandas
#    uses it to store the text, which is faster; the results are the same.
# 3. NULLABLE DTYPES exist next to the NumPy ones: Int64, Float64, boolean, string use pd.NA for "missing"
#    and keep integers as integers. convert_dtypes() converts a table to them.
# 4. inplace=True still works, but returns None and gives no speed advantage: reassign instead.

df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})

# 1. Copy-on-write
column = df["a"]
column.iloc[0] = 99
print(df["a"].tolist(), column.tolist())                    # df is untouched
subset = df[df["a"] > 1]
subset.loc[:, "b"] = 0
print(df["b"].tolist(), subset["b"].tolist())
alias = df                                                  # a second NAME for the same table: changes are shared
alias.loc[0, "a"] = 5
print(df["a"].tolist(), alias is df)
duplicate = df.copy()
duplicate.loc[0, "a"] = -1
print(df["a"].tolist(), duplicate["a"].tolist())

# Chained assignment: two steps, so the change goes to a temporary object and is lost
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    df["a"][0] = 100
print(df["a"].tolist(), [w.category.__name__ for w in caught])
df.loc[0, "a"] = 100                                        # the right way: one step
df.loc[df["b"] > 15, "b"] = 0
print(df["a"].tolist(), df["b"].tolist())

# The NumPy array of a column or table is read-only: copy it to change it
array = df["a"].to_numpy()
print(array.flags.writeable, df.to_numpy(copy=True).flags.writeable)
try:
    array[0] = 1
except ValueError as error:
    print("ValueError:", error)

# 2. The str dtype
names = pd.Series(["ann", "bo", None])
print(names.dtype, names.isna().tolist(), names.str.upper().tolist(), names.str.len().tolist())
print(pd.Series(["ann"], dtype=object).dtype, pd.Series(["ann"], dtype="string").dtype, pd.Series([1, "a"]).dtype)
print(names.fillna("?").tolist(), names.dropna().tolist(), (names == "bo").tolist())

# 3. Nullable dtypes: pd.NA
ints = pd.Series([1, None, 3], dtype="Int64")
print(ints.tolist(), ints.sum(), ints.isna().tolist(), ints.dtype)
print(pd.Series([1, None, 3]).dtype, pd.Series([1, None, 3]).convert_dtypes().dtype)       # NumPy: float64 with nan
print(pd.NA + 1, pd.NA == 1, pd.NA is pd.NA, np.nan == np.nan)
try:
    bool(pd.NA)
except TypeError as error:
    print("TypeError:", error)
flags = pd.Series([True, None, False], dtype="boolean")
print(flags.tolist(), (flags | True).tolist(), flags.sum())

# 4. inplace
work = pd.DataFrame({"x": [3, 1, 2]})
print(work.sort_values("x", inplace=True), work["x"].tolist())
work = work.assign(y=lambda d: d["x"] * 2)                  # the usual style: a new table each step
print(work.columns.tolist())

# What no longer exists (this depends on the pandas version)
print(hasattr(pd.errors, "ChainedAssignmentError"))

# EXPECTED OUTPUT
# [1, 2, 3] [99, 2, 3]
# [10, 20, 30] [0, 0]
# [5, 2, 3] True
# [5, 2, 3] [-1, 2, 3]
# [5, 2, 3] ['ChainedAssignmentError']
# [100, 2, 3] [10, 0, 0]
# False True
# ValueError: assignment destination is read-only
# str [False, False, True] ['ANN', 'BO', nan] [3.0, 2.0, nan]
# object string object
# ['ann', 'bo', '?'] ['ann', 'bo'] [False, True, False]
# [1, <NA>, 3] 4 [False, True, False] Int64
# float64 Int64
# <NA> <NA> True False
# TypeError: boolean value of NA is ambiguous
# [True, <NA>, False] [True, True, True] 1
# None [1, 2, 3]
# ['x', 'y']
# True

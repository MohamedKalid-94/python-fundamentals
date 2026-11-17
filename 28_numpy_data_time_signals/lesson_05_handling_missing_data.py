import numpy as np

# HANDLING MISSING DATA
#   Missing values are usually marked with np.nan (floats only), or with a sentinel such as -999.
#   IDENTIFY   np.isnan  np.isinf  np.isfinite      (never == np.nan: nan is not equal to anything)
#   REMOVE     boolean masks, np.delete, dropping whole rows with any/all
#   IMPUTE     replace with the mean, the median, the previous value (forward fill) or an interpolated value
#   MASKED ARRAYS (np.ma): the data stay as they are, a separate mask says what to ignore
# An integer array cannot hold nan: convert to float first.

temps = np.array([21.0, np.nan, 22.5, -999.0, 23.0, np.inf])
print(np.isnan(temps), np.isinf(temps), np.isfinite(temps))
print(temps == np.nan, np.nan == np.nan)

# Sentinel values become nan
clean = np.where(temps == -999.0, np.nan, temps)
print(clean)
valid = clean[np.isfinite(clean)]                      # REMOVE: keep only the finite numbers
print(valid, valid.mean())
try:
    np.array([1, 2, 3])[0] = np.nan
except ValueError as error:
    print("ValueError:", error)

# Removing rows (or columns) that contain a missing value
table = np.array([[1.0, 2.0], [np.nan, 3.0], [4.0, 5.0], [6.0, np.nan]])
print(table[~np.isnan(table).any(axis=1)])             # keep the rows with no nan
print(table[~np.isnan(table).all(axis=1)].shape)       # drop only rows that are completely empty
print(np.isnan(table).sum(axis=0))                     # how many are missing in each column
print(np.nan_to_num(np.array([1.0, np.nan, np.inf, -np.inf]), nan=0.0, posinf=999.0, neginf=-999.0))

# IMPUTING
x = np.array([1.0, np.nan, np.nan, 4.0, np.nan, 6.0])
missing = np.isnan(x)
print(np.where(missing, np.nanmean(x), x))                                       # the mean
print(np.where(missing, np.nanmedian(x), x))                                     # the median
index = np.where(~missing, np.arange(len(x)), 0)
np.maximum.accumulate(index, out=index)                                          # position of the last valid value
print(x[index])                                                                  # forward fill
good = np.flatnonzero(~missing)
print(np.interp(np.arange(len(x)), good, x[good]))                               # linear interpolation
column_means = np.nanmean(table, axis=0)
print(np.where(np.isnan(table), column_means, table))                            # the mean of every COLUMN

# MASKED ARRAYS
m = np.ma.masked_invalid(x)
print(m, m.mean(), m.count(), m.mask.sum())
print(m.filled(0.0), np.ma.masked_equal([5, -999, 7], -999).sum())
print(np.ma.masked_where(np.array([1, 5, 9]) > 4, np.array([1, 5, 9])).tolist())

# NaN-aware calculations
print(np.nanargmax(np.array([np.nan, 3.0, 9.0, 1.0])), np.nancumsum(np.array([1.0, np.nan, 2.0])))
print(np.mean([1.0, np.nan]), np.nanmean([1.0, np.nan]))

# Counting what is missing, as a report
report = {"n": x.size, "missing": int(missing.sum()), "share": round(float(missing.mean()), 3)}
print(report)

# EXPECTED OUTPUT
# [False  True False False False False] [False False False False False  True] [ True False  True  True  True False]
# [False False False False False False] False
# [21.   nan 22.5  nan 23.   inf]
# [21.  22.5 23. ] 22.166666666666668
# ValueError: cannot convert float NaN to integer
# [[1. 2.]
#  [4. 5.]]
# (4, 2)
# [1 1]
# [   1.    0.  999. -999.]
# [1.         3.66666667 3.66666667 4.         3.66666667 6.        ]
# [1. 4. 4. 4. 4. 6.]
# [1. 1. 1. 4. 4. 6.]
# [1. 2. 3. 4. 5. 6.]
# [[1.         2.        ]
#  [3.66666667 3.        ]
#  [4.         5.        ]
#  [6.         3.33333333]]
# [1.0 -- -- 4.0 -- 6.0] 3.6666666666666665 3 3
# [1. 0. 0. 4. 0. 6.] 12
# [1, None, None]
# 2 [1. 1. 3.]
# nan 1.0
# {'n': 6, 'missing': 3, 'share': 0.5}
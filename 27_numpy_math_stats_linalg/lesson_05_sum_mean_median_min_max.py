import numpy as np

# THE FIVE BASIC AGGREGATES: sum, mean, median, min, max
#   a.sum()  a.mean()  np.median(a)  a.min()  a.max()        (np.sum, np.mean ... are the same)
#   axis=      which axis disappears (None = all)            keepdims=True   keep it with length 1
#   dtype=     the type used for the calculation              where=  initial=  (see below)
#   np.argmin  np.argmax  np.ptp (max - min)                  np.nansum  np.nanmean  np.nanmedian  np.nanmin  np.nanmax

data = np.array([[4.0, 8.0, 15.0], [16.0, 23.0, 42.0]])
print(data.sum(), data.mean(), np.median(data), data.min(), data.max())
print(data.sum(axis=0), data.mean(axis=0), np.median(data, axis=0))
print(data.min(axis=0), data.max(axis=1), data.mean(axis=1, keepdims=True).shape)
print(np.argmin(data), np.argmax(data, axis=1), np.ptp(data), np.ptp(data, axis=0))

# The mean follows outliers, the median does not
vals = np.array([20.0, 21.0, 19.0, 20.5, 500.0])
print(vals.mean(), np.median(vals))

# NaN: the plain functions give nan; the nan-versions skip it
n = np.array([1.0, np.nan, 3.0, 5.0])
print(n.sum(), n.mean(), n.max(), np.nansum(n), np.nanmean(n), np.nanmedian(n), np.nanmin(n), np.nanmax(n))
print(np.isnan(n).sum(), np.count_nonzero(~np.isnan(n)))                     # how many missing, how many valid

# where= and initial=
print(data.sum(where=data > 10), np.mean(data, where=data > 10))
print(np.max(np.array([], dtype=float), initial=-1.0))                       # an empty array needs initial
try:
    np.array([]).max()
except ValueError as error:
    print("ValueError:", str(error)[:48])

# Types: the mean of integers is a float; a wider dtype avoids overflow
small = np.array([200, 100, 50], dtype=np.uint8)
print(small.mean(), small.sum(), small.sum(dtype=np.uint8), np.mean(small, dtype=np.float32))

# Row and column summaries of a table
table = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])
print(table.sum(axis=1), table.mean(axis=0), table.max(axis=0) - table.min(axis=0))
print(table.sum() == table.sum(axis=0).sum() == table.sum(axis=1).sum())

# Element-wise maximum of two arrays (not the same as max)
print(np.maximum(table[0], table[1]), np.minimum(table[0], 25))

# EXPECTED OUTPUT
# 108.0 18.0 15.5 4.0 42.0
# [20. 31. 57.] [10.  15.5 28.5] [10.  15.5 28.5]
# [ 4.  8. 15.] [15. 42.] (2, 1)
# 0 [2 2] 38.0 [12. 15. 27.]
# 116.1 20.5
# nan nan nan 9.0 3.0 3.0 1.0 5.0
# 1 3
# 96.0 24.0
# -1.0
# ValueError: zero-size array to reduction operation maximum w
# 116.66666666666667 350 94 116.666664
# [ 60 150 240] [40. 50. 60.] [60 60 60]
# True
# [40 50 60] [10 20 25]
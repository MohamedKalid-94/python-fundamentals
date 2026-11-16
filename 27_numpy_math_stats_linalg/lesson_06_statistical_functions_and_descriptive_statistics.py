import numpy as np

# STATISTICAL FUNCTIONS (descriptive statistics)
#   centre        mean  median  np.average(a, weights=w)  mode: np.unique(a, return_counts=True)
#   spread        var  std  (ddof=0 population, ddof=1 sample)  np.ptp  IQR = Q3 - Q1
#   position      np.percentile(a, q)  np.quantile(a, q)  (q = 0..100 for percentile, 0..1 for quantile)
#   relationship  np.cov  np.corrcoef
#   shape         np.histogram  np.digitize
#   all of them also have nan-versions: np.nanvar  np.nanstd  np.nanpercentile ...

x = np.array([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
print(x.mean(), np.median(x), x.var(), x.std(), np.round(x.std(ddof=1), 4), np.ptp(x))

# Population vs sample: ddof=0 divides by n, ddof=1 divides by n - 1 (use it for a SAMPLE of a larger set)
print(x.var(ddof=0), np.round(x.var(ddof=1), 4))

# Percentiles and quantiles
print(np.percentile(x, [25, 50, 75]), np.quantile(x, 0.9))
q1, q3 = np.percentile(x, [25, 75])
print("IQR:", q3 - q1)
print(np.percentile(x, 50, method="lower"), np.percentile(x, 50, method="higher"))
print(np.percentile(np.array([[1, 2], [3, 4], [5, 6]]), 50, axis=0))

# Weighted average and mode
print(np.average([1, 2, 3], weights=[3, 1, 1]))
values, counts = np.unique(x, return_counts=True)
print("mode:", values[counts.argmax()])

# Histogram
counts, edges = np.histogram(x, bins=4)
print(counts, edges)
print(np.histogram(x, bins=[0, 5, 10])[0], np.digitize(x, [3, 5, 8]))      # digitize: the bin number of each value

# Covariance and correlation
a = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
b = np.array([2.0, 4.0, 5.0, 4.0, 5.0])
print(np.cov(a, b))
print(np.round(np.corrcoef(a, b), 4))
print(np.round(np.corrcoef(a, 2 * a + 1)[0, 1], 4), np.round(np.corrcoef(a, -a)[0, 1], 4))

# Standardising (z-score) and a running mean
z = (x - x.mean()) / x.std()
print(np.round(z, 2), np.round(z.mean(), 6) + 0.0, np.round(z.std(), 6))
print(np.convolve(x, np.ones(3) / 3, mode="valid").round(3))                # moving average of 3 values
print(np.round(np.cumsum(x) / np.arange(1, len(x) + 1), 3))                  # running mean

# A summary of sensor readings with a missing value
readings = np.array([21.0, 21.5, np.nan, 22.0, 35.0, 21.8])
summary = {
    "n": int(np.count_nonzero(~np.isnan(readings))),
    "mean": round(float(np.nanmean(readings)), 3),
    "median": round(float(np.nanmedian(readings)), 3),
    "std": round(float(np.nanstd(readings, ddof=1)), 3),
    "p95": round(float(np.nanpercentile(readings, 95)), 3),
}
print(summary)

# EXPECTED OUTPUT
# 5.0 4.5 4.0 2.0 2.1381 7.0
# 4.0 4.5714
# [4.  4.5 5.5] 7.6
# IQR: 1.5
# 4.0 5.0
# [3. 4.]
# 1.6
# mode: 4.0
# [1 5 1 1] [2.   3.75 5.5  7.25 9.  ]
# [4 4] [0 1 1 1 2 2 2 3]
# [[2.5 1.5]
#  [1.5 1.5]]
# [[1.     0.7746]
#  [0.7746 1.    ]]
# 1.0 -1.0
# [-1.5 -0.5 -0.5 -0.5  0.   0.   1.   2. ] 0.0 1.0
# [3.333 4.    4.333 4.667 5.667 7.   ]
# [2.    3.    3.333 3.5   3.8   4.    4.429 5.   ]
# {'n': 5, 'mean': 24.26, 'median': 21.8, 'std': 6.016, 'p95': 32.4}
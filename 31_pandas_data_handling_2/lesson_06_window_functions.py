import numpy as np
import pandas as pd

# WINDOW FUNCTIONS: calculations over a SLIDING group of rows
#   s.rolling(window, min_periods=None, center=False, closed=...)   a fixed number of rows, or a time span like "2s"
#       .mean .sum .min .max .median .std .var .count .quantile .corr .apply(func, raw=True) .agg([...])
#   s.expanding(min_periods=1)      from the first row up to the current one (a running statistic)
#   s.ewm(alpha= | span= | halflife=, adjust=)   exponentially weighted: recent values count more
#   shift(n)  diff(n)  pct_change()  cumsum()  cummax()   (lag features, changes, running totals)
# The first window - 1 results are NaN unless min_periods is smaller.

s = pd.Series([1.0, 2.0, 6.0, 4.0, 5.0, 9.0, 3.0])
print(s.rolling(3).mean().round(2).tolist())
print(s.rolling(3, min_periods=1).mean().round(2).tolist(), s.rolling(3, center=True).mean().round(2).tolist())
print(s.rolling(3).sum().tolist(), s.rolling(3).min().tolist(), s.rolling(3).max().tolist(), s.rolling(3).median().tolist())
print(s.rolling(3).std().round(2).tolist(), s.rolling(3).count().tolist(), s.rolling(3).quantile(0.5).tolist())
print(s.rolling(3).apply(lambda w: w.max() - w.min(), raw=True).tolist(), s.rolling(3).agg(["mean", "max"]).round(2).values.tolist()[2:4])
print(s.rolling(3, closed="left").sum().tolist()[:4], s.rolling(3, step=2).mean().round(2).tolist())

# The same moving average with NumPy and with cumsum
print(np.allclose(s.rolling(3).mean().dropna(), np.convolve(s, np.ones(3) / 3, mode="valid")))
running = s.cumsum()
print(np.allclose((running - running.shift(3, fill_value=0))[2:] / 3, s.rolling(3).mean().dropna()))

# Missing values inside a window
gappy = pd.Series([1.0, np.nan, 3.0, 4.0, 5.0])
print(gappy.rolling(2).sum().tolist(), gappy.rolling(2, min_periods=1).sum().tolist(), gappy.rolling(3, min_periods=2).mean().tolist())

# Expanding: a running statistic
print(s.expanding().mean().round(2).tolist(), s.expanding().max().tolist(), s.expanding(min_periods=3).sum().tolist())
print(np.allclose(s.expanding().mean(), s.cumsum() / np.arange(1, len(s) + 1)), s.expanding().std().round(2).tolist()[:3])

# Exponentially weighted
print(s.ewm(alpha=0.5).mean().round(3).tolist())
print(s.ewm(alpha=0.5, adjust=False).mean().round(3).tolist(), s.ewm(span=3, adjust=False).mean().round(3).tolist()[:3], s.ewm(halflife=1, adjust=False).mean().round(3).tolist()[:3])
manual = [s.iloc[0]]
for value in s.iloc[1:]:
    manual.append(0.5 * value + 0.5 * manual[-1])                                  # y_t = alpha * x_t + (1 - alpha) * y_(t-1)
print(np.allclose(manual, s.ewm(alpha=0.5, adjust=False).mean()), s.ewm(alpha=0.5).std().round(3).tolist()[:3])

# Time based windows (the index must be sorted dates)
index = pd.to_datetime(["2026-11-15 10:00:00", "2026-11-15 10:00:01", "2026-11-15 10:00:03", "2026-11-15 10:00:04", "2026-11-15 10:00:10"])
events = pd.Series([1, 2, 3, 4, 5], index=index)
print(events.rolling("2s").sum().tolist(), events.rolling("2s").count().tolist(), events.rolling("5s").mean().tolist())
print(events.rolling("3s", closed="both").sum().tolist(), events.rolling(pd.Timedelta(seconds=2)).max().tolist())

# Whole tables and two columns
df = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0, 5.0], "b": [2.0, 4.0, 5.0, 4.0, 5.0]})
print(df.rolling(2).mean().round(2).values.tolist())
print(round(df["a"].rolling(3).corr(df["b"]).iloc[-1], 3), df["a"].expanding().corr(df["b"]).round(3).tolist()[1:3])
print(df.rolling(2).agg({"a": "sum", "b": "max"}).values.tolist()[1:3], df.expanding().sum().iloc[-1].tolist())

# Lag features, changes and running totals
prices = pd.Series([100.0, 102.0, 101.0, 105.0, 104.0])
print(prices.shift(1).tolist(), prices.shift(-1).tolist(), prices.diff().tolist(), prices.pct_change().round(4).tolist(), prices.cummax().tolist())
print((prices > prices.rolling(2).mean()).tolist(), (prices - prices.expanding().mean()).round(2).tolist())
print(prices.rolling(3).apply(lambda w: (w[-1] - w[0]) / w[0], raw=True).round(4).tolist())

# A simple smoothing and alarm: a noisy signal, a moving average, and samples that deviate too much
signal = pd.Series([10, 10, 11, 10, 25, 10, 9, 10, 10.0])
smooth = signal.rolling(5, center=True, min_periods=1).median()
print(smooth.tolist(), signal[(signal - smooth).abs() > 5].index.tolist())

# EXPECTED OUTPUT
# [nan, nan, 3.0, 4.0, 5.0, 6.0, 5.67]
# [1.0, 1.5, 3.0, 4.0, 5.0, 6.0, 5.67] [nan, 3.0, 4.0, 5.0, 6.0, 5.67, nan]
# [nan, nan, 9.0, 12.0, 15.0, 18.0, 17.0] [nan, nan, 1.0, 2.0, 4.0, 4.0, 3.0] [nan, nan, 6.0, 6.0, 6.0, 9.0, 9.0] [nan, nan, 2.0, 4.0, 5.0, 5.0, 5.0]
# [nan, nan, 2.65, 2.0, 1.0, 2.65, 3.06] [nan, nan, 3.0, 3.0, 3.0, 3.0, 3.0] [nan, nan, 2.0, 4.0, 5.0, 5.0, 5.0]
# [nan, nan, 5.0, 4.0, 2.0, 5.0, 6.0] [[3.0, 6.0], [4.0, 6.0]]
# [nan, nan, nan, 9.0] [nan, 3.0, 5.0, 5.67]
# True
# True
# [nan, nan, nan, 7.0, 9.0] [1.0, 1.0, 3.0, 7.0, 9.0] [nan, nan, 2.0, 3.5, 4.0]
# [1.0, 1.5, 3.0, 3.25, 3.6, 4.5, 4.29] [1.0, 2.0, 6.0, 6.0, 6.0, 9.0, 9.0] [nan, nan, 9.0, 13.0, 18.0, 27.0, 30.0]
# True [nan, 0.71, 2.65]
# [1.0, 1.667, 4.143, 4.067, 4.548, 6.81, 4.89]
# [1.0, 1.5, 3.75, 3.875, 4.438, 6.719, 4.859] [1.0, 1.5, 3.75] [1.0, 1.5, 3.75]
# True [nan, 0.707, 2.866]
# [1.0, 3.0, 3.0, 7.0, 5.0] [1.0, 2.0, 1.0, 2.0, 1.0] [1.0, 1.5, 2.0, 2.5, 5.0]
# [1.0, 3.0, 6.0, 9.0, 5.0] [1.0, 2.0, 3.0, 4.0, 5.0]
# [[nan, nan], [1.5, 3.0], [2.5, 4.5], [3.5, 4.5], [4.5, 4.5]]
# 0.0 [1.0, 0.982]
# [[3.0, 4.0], [5.0, 5.0]] [15.0, 20.0]
# [nan, 100.0, 102.0, 101.0, 105.0] [102.0, 101.0, 105.0, 104.0, nan] [nan, 2.0, -1.0, 4.0, -1.0] [nan, 0.02, -0.0098, 0.0396, -0.0095] [100.0, 102.0, 102.0, 105.0, 105.0]
# [False, True, False, True, False] [0.0, 1.0, 0.0, 3.0, 1.6]
# [nan, nan, 0.01, 0.0294, 0.0297]
# [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0] [4]
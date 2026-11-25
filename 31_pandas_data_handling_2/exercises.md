Write the questions as # comments and your solutions as code. Use assert to check your own answers, and io.StringIO for any text "files".

Build three monthly tables with the same columns (and one table with an extra column). Stack them with concat, once with keys, once with ignore_index, and once with join="inner". Show the error that verify_integrity=True raises, and put the month into a normal column with reset_index.
Put two tables side by side with axis=1 where the indexes only partly overlap, with join="outer" and join="inner". Fill the gaps of one table from another with combine_first, and explain how update differs.
For people, depts and orders tables of your own (with a department that has no people, a person with no department, and a duplicate key), run all four join types and a cross join. For each, write down the number of rows you expect before you run it.
Merge on two key columns, on keys with different names, and on the index. Use suffixes, indicator and validate, and trigger a MergeError on purpose. Write an anti-join (rows of A with no match in B) in two ways.
Show that two tables with NaN keys match each other in a pandas merge. Write the same merge in SQLite and compare the row counts (see lesson 05 of Module 30). Fix a merge where one key is text and the other is an integer.
Use merge_asof to attach to each sensor reading the latest calibration record, in all three directions, with a tolerance, and with by="sensor".
For a table of 15 rows with two numeric columns and one text column: describe() with your own percentiles, describe(include="all"), mean, median, mode, standard deviation with ddof=0 and ddof=1, skewness, the IQR, a z-score column, and the rows whose z-score is above 2. Check the standard deviation against np.std with the right ddof.
Compute Pearson and Spearman correlation for the numeric columns, the covariance matrix, autocorr with lags 1 to 3 for a time series, and pct_change, diff and running maximum. Explain why the Spearman value can differ from the Pearson value.
Clean a text column of 12 messy product names (extra spaces, mixed case, punctuation, a missing value, the same item written two ways): strip, lower, remove punctuation with a regular expression, fix two typos with replace, and count the unique names before and after.
Parse 8 log lines of the form 2026-11-15 10:00:00 [WARN] pump 3: pressure=4.2bar into columns time, level, device, value, unit with str.extract and named groups. Convert the types, count the levels, and find the lines that did not match.
Make a table with 40 columns and 30 rows. Show it with max_columns and max_rows set inside option_context, with the precision and a float_format, and with to_string. Build a Styler that formats two columns, highlights the maximum, adds a caption, and write the HTML to a string. Show that the options are restored after the with block.
For a series of 20 numbers: a rolling mean, median, standard deviation and maximum with a window of 4, centered and not centered, with min_periods=1, and with closed="left"; an expanding mean and maximum; and an exponentially weighted mean with alpha=0.3 that you check against a loop. Build a time-indexed series with uneven timestamps and compute a rolling sum over "10s".
For a table of 12 people with age, city, score and a missing value: select with masks combined by &, |, ~ and isin; between with the three inclusive choices; the same filters with query; assign a band with np.select; replace values with where and mask; and show the three common mistakes (missing parentheses, and, and chained comparison).
For a table with NaN, None, -999, empty strings and "N/A": count what is missing in every column, normalise all markers to real missing values, and then fill with the mean, the median, the previous value, and an interpolated value. Compare the four fills with the true values you started from. Drop rows with how, thresh and subset.
Take a table with exact duplicates, duplicates of a key only, and near-duplicates (case and spaces). Use duplicated with each keep option, drop them keeping the row with the highest value, count how many repeats each key has, and show the duplicated-label problems (loc, reindex, set_flags).
Embedded exercise: three CSV texts from three devices with different column orders, a -999 marker, hex status codes, device names with mixed case, and some repeated lines. Combine them, clean the text, convert the codes, remove the repeats, merge with a device table (validate it), fill short gaps by time interpolation, compute a rolling mean per device (loop over the devices), flag outliers with the IQR rule, and print a short report with to_string.
Predict first, then run, and explain each result in a comment:
python
import numpy as np
import pandas as pd

a = pd.DataFrame({"k": [1, 2, 2], "x": [10, 20, 30]})
b = pd.DataFrame({"k": [2, 2, 3], "y": ["p", "q", "r"]})
print(len(a.merge(b, on="k")), len(a.merge(b, on="k", how="left")), len(a.merge(b, on="k", how="outer")))
s = pd.Series([1.0, np.nan, 3.0, np.nan, 5.0])
print(s.rolling(2).sum().tolist(), s.rolling(2, min_periods=1).sum().tolist(), s.ffill(limit=1).tolist())
t = pd.Series(["  Ann", "ann ", None])
print(t.str.strip().str.lower().duplicated().tolist(), t.str.contains("a", na=False).tolist(), t.str.len().tolist())
d = pd.DataFrame({"v": [1, 1, 2]}, index=["a", "a", "b"])
print(d.loc["a"].shape, d.duplicated().tolist(), d.index.duplicated().tolist())
print((pd.Series([1, 2, 3]) > 1).sum(), pd.Series([1, np.nan, 3]).between(1, 3).tolist())
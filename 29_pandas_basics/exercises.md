Write the questions as # comments and your solutions as code. Use assert to check your own answers.

Build a Series from a list, from a dict and from a NumPy array, each with a different index and a name. Print every attribute (dtype, shape, size, nbytes, is_unique, hasnans). Show what happens to the dtype when you add None to a list of integers.
A Series of 10 temperatures with labels t0 to t9. Select, with loc, iloc, at and masks: the first three, the last three, every second one, the ones above the mean, the ones between 20 and 25, and the label of the maximum. Write down which of these slices include their end.
Make a Series with the integer index [10, 11, 12, 13]. Show that s[1], s.loc[1] and s.iloc[1] give three different results or errors. Explain in a comment why you should write loc or iloc.
Two Series of readings from two sensors with partly different time labels. Add them, subtract them with fill_value=0, keep only the labels present in both, and find the labels that are missing in each.
Convert a Series to a list, a dict, a NumPy array, a one-column DataFrame, CSV text and JSON text. Convert the strings ["1", "2.5", "x", "4"] to numbers with errors="coerce" and count the failures.
Create an Index of 5 labels. Show that you cannot assign one label. Use the set operations with a second Index. Make a Series with duplicate labels and show what s["a"] returns. Build a DatetimeIndex of 10 days and select a week with a label slice.
Build the same 5-row DataFrame in four ways: dict of lists, list of dicts, NumPy array with column names, and list of tuples. Check with equals that the first two are the same. Print shape, dtypes, describe(), info() and the memory of every column.
From a table of 8 people (name, age, city, salary): select columns with [], loc, iloc and filter; rows with a mask, query, isin, nlargest and iloc slices; and one cell with at. For each, print the type of the result (Series, DataFrame or scalar).
Add a column grade (use np.where or map), a column salary_k, and an inserted column at position 1. Change the salary of one person with loc, and of everyone in one city with a mask. Remove two columns three different ways, and remove the rows under age 25 three different ways. Print the final shape after each step.
Show copy-on-write: take a column and change the copy, take a filtered subset and change it, and use chained assignment once (catch the warning). Then make the same change correctly with loc. Write in a comment why df2 = df is different from df2 = df.copy().
Arithmetic on two DataFrames with different rows and columns: +, add(fill_value=0), and subtracting the column means. Scale a table to the range 0 to 1 and to a z-score. Divide by a column with axis=0. Find the correlation between two columns.
Build a table of 12 sensor readings (use np.arange, no random numbers) with some NaN. Use describe, value_counts, isna().sum(), sort_values by two columns, rank, cumsum, idxmax, nlargest, clip and agg with different functions for different columns.
Use convert_dtypes on a table with integers, text and a missing value. Compare the dtypes before and after, the result of sum on an Int64 column with a missing value, and what bool(pd.NA) does. Write down when you would choose the nullable types.
Convert a DataFrame to a list of dicts, a dict of lists, a NumPy array, CSV text and JSON text, and back with from_records and from_dict. Check that the round trip gives an equal table.
Embedded exercise: a table of 20 ADC readings (time_ms, channel, counts) with some values stuck at 0 or 4095. Flag the bad samples, convert counts to volts and degrees with assign, remove the bad rows, compute the mean and the maximum of every channel, and hand a clean NumPy array to np.fft.rfft. Print the dominant frequency.
Predict first, then run, and explain each result in a comment:
python
import pandas as pd

s = pd.Series([1, 2, 3], index=[3, 2, 1])
t = pd.Series([10, 20, 30], index=[1, 2, 4])
print(s[1], s.iloc[1], s.loc[1:3].tolist(), s[0:2].tolist())
print((s + t).to_dict())
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df["a"][0] = 100
sub = df[df["a"] > 1]
sub.loc[:, "b"] = 0
print(df["a"].tolist(), df["b"].tolist(), sub["b"].tolist())
print(df.sum().to_dict(), df.sum(axis=1).tolist(), (df > 2).sum().to_dict())
print(df.drop(columns="b").columns.tolist(), df.columns.tolist())
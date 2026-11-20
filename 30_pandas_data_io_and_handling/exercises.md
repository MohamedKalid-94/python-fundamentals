Write the questions as # comments and your solutions as code. Use assert to check your own answers. Use io.StringIO and a temporary folder, so you leave no files behind.

Write a CSV text with a comment line, a header, a decimal comma, a thousands separator, a quoted field with a comma, a -999 sentinel, a date column and a column with leading zeros. Read it correctly with one read_csv call, and check every dtype.
Read the same CSV in chunks of 3 rows and compute a running total and the maximum without ever holding the whole table. Compare with the result from reading everything at once.
Write a table to CSV with float_format, na_rep, another separator, a subset of columns and no index. Append two rows with mode="a", write a gzip copy, and compare the sizes.
Convert one table to the five JSON orients and read each back. Which orients keep the index? Write it as JSON Lines, read it in chunks, and show why JSON Lines is better for big files.
Flatten a nested JSON (customers with an address dictionary and a list of orders) with json_normalize: one table of customers, and one table of orders with the customer id and city. Make a table of 5 prompts and answers, save it as JSON Lines, reload it with precise_float=True, and check it is equal.
Write a workbook with three sheets (one with an offset header, one with a date column, one with a missing value). Read each sheet back correctly, read all sheets as a dictionary, replace one sheet, and set a column width and a frozen row with openpyxl.
Parse an HTML page with two tables, choose the second with match=, and convert the first back to HTML. Create a SQLite database from three tables, and write a parameterised query with read_sql_query. Append rows, replace a table, and show what if_exists="fail" does.
Save a table with a datetime, a nullable integer and an object column as pickle and restore it. Write down in a comment why you must not unpickle a file from an unknown source.
Translate ten SQL queries to pandas and check them against SQLite as in lesson 05: a WHERE with AND/OR, ORDER BY with two keys, LIMIT, DISTINCT, IN, LIKE, a CASE, a GROUP BY with HAVING, a JOIN and a LEFT JOIN. Explain the NULL trap in your own words, with an example.
Sort a table of 12 rows by one column, by two columns with different directions, by a case-insensitive text key, by a custom order (low, mid, high), with missing values first and last, and by the index. Show with kind="stable" which rows with ties keep their order. Rank the values with all five methods.
Take the 5 largest and 5 smallest rows by a column, and show the difference between keep="first", "last" and "all" for ties. Sort a column of date strings as text and as dates and show the difference.
Reindex a table to a new list of rows and columns, with fill_value; force a schema of five columns on a table that has three of them and two extra ones; and fill a gap in a series with ffill, bfill, nearest (with tolerance) and limit. Show the error for duplicate labels.
Build a time series with 6 missing hours, reindex it to every hour, and fill it with interpolate, ffill and a constant. Compare the three with the true values.
Loop over a table of 50,000 rows with iterrows, itertuples, zip and a vectorized expression to compute a * b + c. Check that the four results are equal and print the speed ratios (do not assert exact times). Show the dtype change that iterrows causes.
Use apply with axis=0 and axis=1, map with a dictionary and a function, DataFrame.map, agg with a list, with a dict and with named aggregation, transform for z-scores and min-max scaling, and pipe for a chain of three steps. For each, write the vectorized expression that gives the same result.
Embedded exercise: a CSV of 20 log lines time;sensor;counts;flags with a header comment, some NaN counts and flags as hexadecimal text. Read it, convert hexadecimal flags with map(lambda s: int(s, 16)), decode three flag bits into three boolean columns, convert counts to volts, sort by time, reindex each sensor to a regular 10-second grid, interpolate the gaps, and write the result to CSV, JSON Lines and SQLite. Read all three back and check that they agree.
Predict first, then run, and explain each result in a comment:
python
import io
import pandas as pd

df = pd.read_csv(io.StringIO("id,code,v\n1,007,5\n2,010,NA\n3,200,-1\n"), na_values=["NA", "-1"])
print(df["code"].tolist(), df["v"].tolist(), df.dtypes.astype(str).tolist())
s = pd.Series([3, 1, 2, 1], index=list("abcd"))
print(s.sort_values(kind="stable").index.tolist(), s.rank(method="min").tolist(), s.reindex(["d", "z"]).tolist())
t = pd.DataFrame({"a": [1, 2], "b": [3.5, 4.5]})
print(next(t.iterrows())[1].tolist(), next(t.itertuples()), t.agg(["sum", "max"]).values.tolist())
print(t.apply(lambda r: r["a"] + r["b"], axis=1).tolist(), t.map(lambda v: v * 2).values.tolist())
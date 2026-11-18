import numpy as np
import pandas as pd

# ARITHMETIC ON DATAFRAMES: element by element, ALIGNED on both the row labels and the column labels.
#   df + 10, df * 2, df ** 2, -df          a scalar is applied to every cell
#   df1 + df2                              cells whose row AND column exist in both are added; the rest become NaN
#   df1.add(df2, fill_value=0)  .sub  .mul  .div  .pow  .rsub (reversed)
#   df + series                            the Series index is matched with the COLUMNS (use axis=0 to match the rows)
#   df.sum(axis=0 / 1)  df.mean()  df.cumsum()  df.diff()  df.pct_change()  df.corr()  df.dot(...)

a = pd.DataFrame({"x": [1, 2, 3], "y": [10, 20, 30]}, index=["r1", "r2", "r3"])
b = pd.DataFrame({"x": [1, 1, 1], "z": [5, 5, 5]}, index=["r1", "r2", "r4"])
print(a + 10)
print(a * 2)
print(a / 4)
print((a ** 2).values.tolist(), (-a).values.tolist(), (a % 3).values.tolist(), (a // 2).values.tolist())
print(a + b)
print(a.add(b, fill_value=0))
print(a.mul(b, fill_value=1))

# A Series against a DataFrame: columns by default, rows with axis=0
column_values = pd.Series({"x": 100, "y": 200})
print(a + column_values)
row_values = pd.Series([1, 2, 3], index=["r1", "r2", "r3"])
print(a.add(row_values, axis=0))
print(a.sub(a.mean()))                                    # subtract each column's mean
print(a.sub(a.mean(axis=1), axis=0))                      # subtract each row's mean
print(a.div(a.max()), a.rsub(100).values.tolist(), sep="\n")

# Comparisons and tests
print((a > 15).values.tolist(), a.eq(2).values.tolist())
print((a > 1).all().to_dict(), (a > 1).any().to_dict(), (a > 1).sum().to_dict(), (a > 1).sum(axis=1).to_dict())
print(a.gt(a.mean()).values.tolist())
print(a.equals(a.copy()), (a == a).all().all())

# Calculations with NumPy and reductions
print(np.sqrt(a).round(2).values.tolist(), np.log(a).round(2).iloc[0].tolist())
print(a.sum().to_dict(), a.sum(axis=1).to_dict(), a.mean().to_dict(), a.max(axis=1).to_dict())
print(a.cumsum().values.tolist(), a.diff().values.tolist(), a.pct_change().round(2).iloc[1].tolist())
print(a.corr().round(3).values.tolist(), a.cov().values.tolist())
print((a - a.min()) / (a.max() - a.min()))                # min-max scaling of every column

# Matrix products keep the labels
print(a.T.dot(a))
print(a.dot(pd.Series({"x": 1, "y": 0.5})).to_dict())

# Division by zero
z = pd.DataFrame({"n": [1.0, -1.0, 0.0]})
print((z / 0).iloc[:, 0].tolist(), (pd.DataFrame({"i": [1, 2]}) // 1).dtypes["i"])

# Type of the result
print((a + 0.5).dtypes.tolist(), (a * 2).dtypes.tolist(), (a / 2).dtypes.tolist(), (a + b).dtypes.tolist())

# Combining tables
print(a.combine_first(b))
print(a.loc[["r1", "r2"]].add(b.loc[["r1", "r2"], ["x"]], fill_value=0))

# EXPECTED OUTPUT
#      x   y
# r1  11  20
# r2  12  30
# r3  13  40
#     x   y
# r1  2  20
# r2  4  40
# r3  6  60
#        x    y
# r1  0.25  2.5
# r2  0.50  5.0
# r3  0.75  7.5
# [[1, 100], [4, 400], [9, 900]] [[-1, -10], [-2, -20], [-3, -30]] [[1, 1], [2, 2], [0, 0]] [[0, 5], [1, 10], [1, 15]]
#       x   y   z
# r1  2.0 NaN NaN
# r2  3.0 NaN NaN
# r3  NaN NaN NaN
# r4  NaN NaN NaN
#       x     y    z
# r1  2.0  10.0  5.0
# r2  3.0  20.0  5.0
# r3  3.0  30.0  NaN
# r4  1.0   NaN  5.0
#       x     y    z
# r1  1.0  10.0  5.0
# r2  2.0  20.0  5.0
# r3  3.0  30.0  NaN
# r4  1.0   NaN  5.0
#       x    y
# r1  101  210
# r2  102  220
# r3  103  230
#     x   y
# r1  2  11
# r2  4  22
# r3  6  33
#       x     y
# r1 -1.0 -10.0
# r2  0.0   0.0
# r3  1.0  10.0
#        x     y
# r1  -4.5   4.5
# r2  -9.0   9.0
# r3 -13.5  13.5
#            x         y
# r1  0.333333  0.333333
# r2  0.666667  0.666667
# r3  1.000000  1.000000
# [[99, 90], [98, 80], [97, 70]]
# [[False, False], [False, True], [False, True]] [[False, False], [True, False], [False, False]]
# {'x': False, 'y': True} {'x': True, 'y': True} {'x': 2, 'y': 3} {'r1': 1, 'r2': 2, 'r3': 2}
# [[False, False], [False, False], [True, True]]
# True True
# [[1.0, 3.16], [1.41, 4.47], [1.73, 5.48]] [0.0, 2.3]
# {'x': 6, 'y': 60} {'r1': 11, 'r2': 22, 'r3': 33} {'x': 2.0, 'y': 20.0} {'r1': 10, 'r2': 20, 'r3': 30}
# [[1, 10], [3, 30], [6, 60]] [[nan, nan], [1.0, 10.0], [1.0, 10.0]] [1.0, 1.0]
# [[1.0, 1.0], [1.0, 1.0]] [[1.0, 10.0], [10.0, 100.0]]
#       x    y
# r1  0.0  0.0
# r2  0.5  0.5
# r3  1.0  1.0
#      x     y
# x   14   140
# y  140  1400
# {'r1': 6.0, 'r2': 12.0, 'r3': 18.0}
# [inf, -inf, nan] int64
# [dtype('float64'), dtype('float64')] [dtype('int64'), dtype('int64')] [dtype('float64'), dtype('float64')] [dtype('float64'), dtype('float64'), dtype('float64')]
#     x     y    z
# r1  1  10.0  5.0
# r2  2  20.0  5.0
# r3  3  30.0  NaN
# r4  1   NaN  5.0
#     x     y
# r1  2  10.0
# r2  3  20.0

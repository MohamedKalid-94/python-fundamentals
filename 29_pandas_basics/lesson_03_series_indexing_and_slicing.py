import pandas as pd

# SELECTING FROM A SERIES: by LABEL or by POSITION. Be explicit:
#   s.loc[label]   s.loc[a:b]     by LABEL; a slice INCLUDES both ends
#   s.iloc[i]      s.iloc[a:b]    by POSITION; a slice EXCLUDES the end (like Python lists)
#   s.at[label]    s.iat[i]       one single value, fastest
#   s[...]         works but is ambiguous with integer labels: prefer loc and iloc
#   masks:  s[s > 2]   s[s.isin([...])]   s[s.between(a, b)]       s.where(cond)   s.mask(cond)
#   s.head(n)  s.tail(n)  s.sample(n, random_state=...)  s.nlargest(n)  s.nsmallest(n)

s = pd.Series([10, 20, 30, 40, 50], index=["a", "b", "c", "d", "e"])
print(s["b"], s.loc["b"], s.iloc[1], s.at["b"], s.iat[1], s.iloc[-1])
print(s["b":"d"].tolist(), s.loc["b":"d"].tolist(), s.iloc[1:3].tolist())            # label slice includes "d", position slice stops before 3
print(s[["a", "c"]].tolist(), s.loc[["e", "a"]].tolist(), s.iloc[[0, -1]].tolist())    # lists of labels or positions
print(s[::2].tolist(), s.iloc[::-1].tolist(), s.head(2).tolist(), s.tail(2).tolist())
print(s.loc[:"b"].tolist(), s.loc["d":].tolist())

# Masks
print(s[s > 25].tolist(), s[(s > 15) & (s < 45)].index.tolist(), s[~(s > 15)].tolist())
print(s[s.isin([10, 50])].index.tolist(), s[s.between(20, 40)].tolist())
print(s.where(s > 25).tolist(), s.where(s > 25, 0).tolist(), s.mask(s > 25, -1).tolist())
print(s.nlargest(2).index.tolist(), s.nsmallest(2).tolist(), s.idxmax(), s.idxmin())

# With the default integer index, labels and positions look the same until you slice
t = pd.Series([5, 6, 7, 8], index=[2, 3, 4, 5])
print(t.loc[2], t.iloc[2])
print(t.loc[2:4].tolist(), t.iloc[2:4].tolist())
print(t[2:4].tolist())                         # [] is a POSITION slice here: another reason to write loc or iloc

# Changing values
u = s.copy()
u["a"] = 0
u.loc["b":"c"] = [1, 2]
u.iloc[-1] = 99
u[u > 30] = 30
print(u.to_dict())

# Errors and safe lookups
try:
    s["z"]
except KeyError as error:
    print("KeyError:", error)
try:
    s.iloc[10]
except IndexError as error:
    print("IndexError:", error)
print(s.get("z"), s.get("z", -1), "z" in s, s.index.get_loc("c"))

# Reindexing with a list of labels gives NaN for the missing ones
print(s.reindex(["a", "z"]).tolist())

# The position of the first element satisfying a condition, and the elements around it
first_big = (s > 25).idxmax()
print(first_big, s.index.get_loc(first_big), s.loc[first_big:].tolist())

# EXPECTED OUTPUT
# 20 20 20 20 20 50
# [20, 30, 40] [20, 30, 40] [20, 30]
# [10, 30] [50, 10] [10, 50]
# [10, 30, 50] [50, 40, 30, 20, 10] [10, 20] [40, 50]
# [10, 20] [40, 50]
# [30, 40, 50] ['b', 'c', 'd'] [10]
# ['a', 'e'] [20, 30, 40]
# [nan, nan, 30.0, 40.0, 50.0] [0, 0, 30, 40, 50] [10, 20, -1, -1, -1]
# ['e', 'd'] [10, 20] e a
# 5 7
# [5, 6, 7] [7, 8]
# [7, 8]
# {'a': 0, 'b': 1, 'c': 2, 'd': 30, 'e': 30}
# KeyError: 'z'
# IndexError: single positional indexer is out-of-bounds
# None -1 False 2
# [10.0, nan]
# c 2 [30, 40, 50]
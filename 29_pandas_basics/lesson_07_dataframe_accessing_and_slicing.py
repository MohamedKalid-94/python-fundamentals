import pandas as pd

# ACCESSING AND SLICING A DATAFRAME
#   df["col"]               one column (a Series)         df[["a", "b"]]   several columns (a DataFrame)
#   df.col                  attribute access (only for names that are valid and do not clash with a method)
#   df.loc[rows, cols]      by LABEL, slices INCLUDE the end          df.iloc[rows, cols]   by POSITION, slices exclude the end
#   df.at[row, col]         df.iat[i, j]                              one single value
#   df[1:3]                 slices ROWS by position;  df["a":"c"]  slices rows by label
#   df[mask]  df.query("...")  df.filter(items / like / regex)  df.xs(...)  df.take([...])  df.sample(...)  df.nlargest(...)

df = pd.DataFrame(
    {"name": ["Ann", "Bo", "Cy", "Di", "Ed"], "age": [25, 31, 19, 44, 38], "kg": [55.5, 70.2, 62.0, 81.3, 77.0], "city": ["Pune", "Goa", "Pune", "Delhi", "Goa"]},
    index=["r1", "r2", "r3", "r4", "r5"],
)
print(df["age"].tolist(), df.age.mean(), df[["name", "kg"]].shape, type(df[["name"]]).__name__, type(df["name"]).__name__)

# loc: labels
print(df.loc["r2"].to_dict())
print(df.loc["r2", "name"], df.loc["r2":"r4", "age"].tolist(), df.loc[["r1", "r5"], ["name", "city"]].values.tolist())
print(df.loc[:, "age":"city"].columns.tolist(), df.loc["r3":, "name"].tolist())
print(df.loc[df["age"] > 30, "name"].tolist(), df.loc[lambda d: d["kg"] < 70, "name"].tolist())

# iloc: positions
print(df.iloc[0].to_dict(), df.iloc[1, 0], df.iloc[-1, -1])
print(df.iloc[1:3, [0, 2]].values.tolist(), df.iloc[::2, 0].tolist(), df.iloc[:, 1].tolist())
print(df.at["r2", "kg"], df.iat[1, 2], df.iloc[[0, 2]].index.tolist())

# Slicing rows with []
print(df[1:3].index.tolist(), df["r2":"r3"].index.tolist(), df[:2]["name"].tolist())

# Masks and queries
adults = df[df["age"] >= 30]
print(adults["name"].tolist())
print(df[(df["city"] == "Goa") & (df["kg"] > 75)]["name"].tolist(), df[df["city"].isin(["Pune", "Delhi"])]["name"].tolist())
print(df[~df["city"].eq("Goa")]["name"].tolist(), df[df["name"].str.startswith("D")]["name"].tolist())
print(df.query("age > 30 and city == 'Goa'")["name"].tolist(), df.query("kg < @limit", local_dict={"limit": 60})["name"].tolist())
print(df.where(df["age"] > 30)["name"].tolist())

# Choosing columns and rows by rule
print(df.filter(items=["name", "age"]).columns.tolist(), df.filter(like="a").columns.tolist(), df.filter(regex="^[ck]").columns.tolist())
print(df.nlargest(2, "age")["name"].tolist(), df.nsmallest(2, "kg")["name"].tolist())
print(df.take([4, 0])["name"].tolist(), sorted(df.sample(3, random_state=0).index.tolist()) == sorted(df.sample(3, random_state=0).index.tolist()))
print(df.head(2).index.tolist(), df.tail(1).index.tolist(), len(df.sample(frac=0.4, random_state=1)))
print(df["city"].unique().tolist(), df["city"].nunique(), df["city"].value_counts().to_dict())
print(df.idxmax(numeric_only=True).to_dict())

# A single cell, a row and a column are different objects
print(type(df.loc["r1", "age"]).__name__, type(df.loc["r1"]).__name__, type(df.loc[["r1"]]).__name__)

# Errors
try:
    df["height"]
except KeyError as error:
    print("KeyError:", error)
try:
    df.loc["r9"]
except KeyError as error:
    print("KeyError:", error)
print(df.get("height"), "age" in df, "r1" in df.index, "r1" in df)

# The DataFrame as a mapping of columns
for column in list(df)[:2]:
    print(column, end=" ")
print()
for label, row in df.head(2).iterrows():
    print(label, row["name"], row["age"])

# EXPECTED OUTPUT
# [25, 31, 19, 44, 38] 31.4 (5, 2) DataFrame Series
# {'name': 'Bo', 'age': 31, 'kg': 70.2, 'city': 'Goa'}
# Bo [31, 19, 44] [['Ann', 'Pune'], ['Ed', 'Goa']]
# ['age', 'kg', 'city'] ['Cy', 'Di', 'Ed']
# ['Bo', 'Di', 'Ed'] ['Ann', 'Cy']
# {'name': 'Ann', 'age': 25, 'kg': 55.5, 'city': 'Pune'} Bo Goa
# [['Bo', 70.2], ['Cy', 62.0]] ['Ann', 'Cy', 'Ed'] [25, 31, 19, 44, 38]
# 70.2 70.2 ['r1', 'r3']
# ['r2', 'r3'] ['r2', 'r3'] ['Ann', 'Bo']
# ['Bo', 'Di', 'Ed']
# ['Ed'] ['Ann', 'Cy', 'Di']
# ['Ann', 'Cy', 'Di'] ['Di']
# ['Bo', 'Ed'] ['Ann']
# [nan, 'Bo', nan, 'Di', 'Ed']
# ['name', 'age'] ['name', 'age'] ['kg', 'city']
# ['Di', 'Ed'] ['Ann', 'Cy']
# ['Ed', 'Ann'] True
# ['r1', 'r2'] ['r5'] 2
# ['Pune', 'Goa', 'Delhi'] 3 {'Pune': 2, 'Goa': 2, 'Delhi': 1}
# {'age': 'r4', 'kg': 'r4'}
# int64 Series DataFrame
# KeyError: 'height'
# KeyError: 'r9'
# None True True False
# name age
# r1 Ann 25
# r2 Bo 31
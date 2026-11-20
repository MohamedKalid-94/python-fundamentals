import io
import sqlite3
import tempfile
from pathlib import Path

import pandas as pd

# OTHER FORMATS
#   HTML      pd.read_html(StringIO(text or url))  returns a LIST of tables       df.to_html()
#   SQL       pd.read_sql_query(sql, connection)   df.to_sql(name, connection)    (sqlite3 needs nothing extra)
#   pickle    df.to_pickle(path)   pd.read_pickle(path)      Python-only, exact types; never load a pickle you do not trust
#   fixed width  pd.read_fwf        Markdown  df.to_markdown() (needs tabulate)      plain text  df.to_string()
#   NOT RUN IN THIS COURSE (they need extra packages or a desktop session), the calls are:
#     pd.read_clipboard() / df.to_clipboard()        the clipboard of your desktop (needs pyperclip or a system tool)
#     df.to_hdf("f.h5", key="t") / pd.read_hdf(...)  HDF5, needs the PyTables package ("tables"): big labelled tables
#     df.to_parquet("f.parquet") / pd.read_parquet   Parquet, needs pyarrow: the standard format for datasets
#     df.to_feather / pd.read_feather                Feather, needs pyarrow
# Which to choose? Share with people: CSV or Excel.  Share between programs or keep types: Parquet.  Query: a database.

df = pd.DataFrame({"name": ["Ann", "Bo"], "age": [25, 31], "kg": [55.5, 70.2]})

# HTML
html = df.to_html(index=False)
print(html.splitlines()[0], html.count("<tr>"), "<td>Ann</td>" in html)
page = "<html><body><h1>Report</h1><table id='a'><tr><th>x</th><th>y</th></tr><tr><td>1</td><td>2.5</td></tr><tr><td>3</td><td>4.5</td></tr></table><table><tr><th>name</th></tr><tr><td>Ann</td></tr></table></body></html>"
tables = pd.read_html(io.StringIO(page))
print(len(tables), tables[0].values.tolist(), tables[0].dtypes.astype(str).to_dict(), tables[1].columns.tolist())
print(pd.read_html(io.StringIO(page), match="name")[0].shape, pd.read_html(io.StringIO(page), attrs={"id": "a"})[0].shape)
print(pd.read_html(io.StringIO(html))[0].equals(df))
print(df.to_html(index=False, classes="table", border=0, float_format="{:.1f}".format).splitlines()[0])

# SQL with the sqlite3 module of the standard library (an in-memory database)
conn = sqlite3.connect(":memory:")
df.to_sql("people", conn, index=False)
print(pd.read_sql_query("SELECT * FROM people", conn))
print(pd.read_sql_query("SELECT name FROM people WHERE age > ?", conn, params=(26,))["name"].tolist())
print(pd.read_sql_query("SELECT name, age FROM people", conn, index_col="name").loc["Bo", "age"])
print(pd.read_sql_query("SELECT age * 2 AS double_age, kg FROM people", conn).columns.tolist())
more = pd.DataFrame({"name": ["Cy"], "age": [19], "kg": [62.0]})
more.to_sql("people", conn, index=False, if_exists="append")
print(pd.read_sql_query("SELECT COUNT(*) AS n FROM people", conn)["n"].tolist())
df.to_sql("people", conn, index=False, if_exists="replace")
print(pd.read_sql("SELECT COUNT(*) AS n FROM people", conn)["n"].tolist())
for chunk in pd.read_sql_query("SELECT * FROM people", conn, chunksize=1):
    print(chunk["name"].tolist(), end=" ")
print()
try:
    df.to_sql("people", conn, index=False)
except ValueError as error:
    print("ValueError:", error)
print(conn.execute("SELECT typeof(name), typeof(age), typeof(kg) FROM people LIMIT 1").fetchone())
conn.close()

# Pickle: exact types, any Python object in a column, but only for Python and only for trusted files
typed = pd.DataFrame({"t": pd.to_datetime(["2026-11-15"]), "n": pd.array([1], dtype="Int64"), "obj": [{"a": 1}]})
with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "table.pkl"
    typed.to_pickle(path)
    restored = pd.read_pickle(path)
    print(restored.equals(typed), restored["t"].dt.year.tolist(), restored[["n", "obj"]].dtypes.astype(str).tolist(), restored["obj"].iloc[0])

# Fixed width text, Markdown and plain text
fixed = "name  age\nAnn   25\nBo    31\n"
print(pd.read_fwf(io.StringIO(fixed)).values.tolist())
print(df.to_markdown(index=False))
print(df.to_string(index=False).splitlines()[0])

# The readers and writers (the names to remember)
readers = sorted(name for name in dir(pd) if name.startswith("read_"))
writers = sorted(name for name in dir(pd.DataFrame) if name.startswith("to_") and name in {"to_csv", "to_json", "to_excel", "to_html", "to_sql", "to_pickle", "to_parquet", "to_hdf", "to_markdown", "to_clipboard", "to_feather", "to_xml", "to_stata", "to_latex"})
print([r for r in readers if r in {"read_csv", "read_json", "read_excel", "read_html", "read_sql", "read_pickle", "read_parquet", "read_hdf", "read_clipboard", "read_fwf", "read_xml"}])
print(writers)

# EXPECTED OUTPUT
# <table border="1" class="dataframe"> 2 True
# 2 [[1.0, 2.5], [3.0, 4.5]] {'x': 'int64', 'y': 'float64'} ['name']
# (1, 1) (2, 2)
# True
# <table class="dataframe table">
#   name  age    kg
# 0  Ann   25  55.5
# 1   Bo   31  70.2
# ['Bo']
# 31
# ['double_age', 'kg']
# [3]
# [2]
# ['Ann'] ['Bo']
# ValueError: Table 'people' already exists.
# ('text', 'integer', 'real')
# True [2026] ['Int64', 'object'] {'a': 1}
# [['Ann', 25], ['Bo', 31]]
# | name   |   age |   kg |
# |:-------|------:|-----:|
# | Ann    |    25 | 55.5 |
# | Bo     |    31 | 70.2 |
# name  age   kg
# ['read_clipboard', 'read_csv', 'read_excel', 'read_fwf', 'read_hdf', 'read_html', 'read_json', 'read_parquet', 'read_pickle', 'read_sql', 'read_xml']
# ['to_clipboard', 'to_csv', 'to_excel', 'to_feather', 'to_hdf', 'to_html', 'to_json', 'to_latex', 'to_markdown', 'to_parquet', 'to_pickle', 'to_sql', 'to_stata', 'to_xml']
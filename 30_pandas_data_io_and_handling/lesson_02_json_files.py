import io
import json
import tempfile
from pathlib import Path

import pandas as pd

# JSON FILES: pd.read_json(StringIO(text) or path, orient=..., lines=...)  and  df.to_json(path, orient=..., lines=...)
#   orient    "columns" (default)  "records" (a list of rows)  "index"  "split"  "values"  "table" (with a schema)
#   lines=True   JSON LINES: one JSON object per line (the usual format for big datasets, logs and LLM training data)
#   pd.json_normalize(list_of_dicts, record_path=, meta=, sep=)   flattens NESTED JSON into columns
#   dates: date_format="iso", date_unit="ms"      text: force_ascii=False      path ending .gz: compressed

df = pd.DataFrame({"name": ["Ann", "Bo"], "age": [25, 31]})
for orient in ["columns", "records", "index", "split", "values"]:
    print(f"{orient:<8}", df.to_json(orient=orient))
print(list(json.loads(df.to_json(orient="table"))), json.loads(df.to_json(orient="table"))["data"])

# Reading each orientation back
text = df.to_json(orient="records")
print(pd.read_json(io.StringIO(text)).equals(df), pd.read_json(io.StringIO(df.to_json(orient="split")), orient="split").equals(df))
print(pd.read_json(io.StringIO('[{"a": 1, "b": "x"}, {"a": 2}]')))                     # missing keys become NaN
print(pd.read_json(io.StringIO('{"r1": {"a": 1}, "r2": {"a": 2}}'), orient="index"))

# JSON LINES
lines = df.to_json(orient="records", lines=True)
print(lines.splitlines())
print(pd.read_json(io.StringIO(lines), lines=True).equals(df))
many = "\n".join(json.dumps({"id": i, "text": f"item {i}"}) for i in range(7))
for chunk in pd.read_json(io.StringIO(many), lines=True, chunksize=3):
    print(len(chunk), chunk["id"].tolist())

# NESTED JSON
nested = [
    {"id": 1, "name": "Ann", "address": {"city": "Pune", "zip": "411001"}, "orders": [{"item": "pen", "qty": 2}, {"item": "ink", "qty": 1}]},
    {"id": 2, "name": "Bo", "address": {"city": "Goa", "zip": "403001"}, "orders": [{"item": "cap", "qty": 5}]},
]
print(pd.json_normalize(nested, max_level=1).drop(columns="orders"))
print(pd.json_normalize(nested, sep="_", max_level=1).columns.tolist())
orders = pd.json_normalize(nested, record_path="orders", meta=["id", "name", ["address", "city"]])
print(orders)

# The standard json module and the dictionaries of Module 9 work as well
raw = '{"sensor": "A", "readings": [1.5, 2.5, 3.5]}'
print(pd.DataFrame(json.loads(raw)))
print(json.loads(df.to_json(orient="records")), json.dumps(df.to_dict(orient="records")))

# Dates, text and files
events = pd.DataFrame({"t": pd.to_datetime(["2026-11-15 10:00:00"]), "msg": ["café"]})
print(events.to_json(orient="records", date_format="iso"))                      # dates: use "iso" (the old "epoch" default is deprecated)
print(events.to_json(orient="records", date_format="iso", force_ascii=False))     # keep accents readable
print(pd.read_json(io.StringIO(events.to_json(orient="records", date_format="iso")), convert_dates=["t"])["t"].dt.year.tolist())
with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "data.json"
    df.to_json(path, orient="records", indent=2)
    print(path.read_text().splitlines()[:3])
    print(pd.read_json(path).shape)
    zipped = Path(folder) / "data.jsonl.gz"
    df.to_json(zipped, orient="records", lines=True)
    print(pd.read_json(zipped, lines=True).shape, zipped.read_bytes()[:2])

# Types: numbers stored as text are converted, and big integers keep precision as long as they fit
print(pd.read_json(io.StringIO('[{"n": "1", "x": "2.5"}]')).dtypes.astype(str).to_dict())
print(pd.read_json(io.StringIO('[{"n": 1, "s": "a"}]'), dtype={"n": "float64"}).dtypes.astype(str).to_dict())

# EXPECTED OUTPUT
# columns  {"name":{"0":"Ann","1":"Bo"},"age":{"0":25,"1":31}}
# records  [{"name":"Ann","age":25},{"name":"Bo","age":31}]
# index    {"0":{"name":"Ann","age":25},"1":{"name":"Bo","age":31}}
# split    {"columns":["name","age"],"index":[0,1],"data":[["Ann",25],["Bo",31]]}
# values   [["Ann",25],["Bo",31]]
# ['schema', 'data'] [{'index': 0, 'name': 'Ann', 'age': 25}, {'index': 1, 'name': 'Bo', 'age': 31}]
# True True
#    a    b
# 0  1    x
# 1  2  NaN
#     a
# r1  1
# r2  2
# ['{"name":"Ann","age":25}', '{"name":"Bo","age":31}']
# True
# 3 [0, 1, 2]
# 3 [3, 4, 5]
# 1 [6]
#    id name address.city address.zip
# 0   1  Ann         Pune      411001
# 1   2   Bo          Goa      403001
# ['id', 'name', 'orders', 'address_city', 'address_zip']
#   item  qty id name address.city
# 0  pen    2  1  Ann         Pune
# 1  ink    1  1  Ann         Pune
# 2  cap    5  2   Bo          Goa
#   sensor  readings
# 0      A       1.5
# 1      A       2.5
# 2      A       3.5
# [{'name': 'Ann', 'age': 25}, {'name': 'Bo', 'age': 31}] [{"name": "Ann", "age": 25}, {"name": "Bo", "age": 31}]
# [{"t":"2026-11-15T10:00:00.000","msg":"caf\u00e9"}]
# [{"t":"2026-11-15T10:00:00.000","msg":"café"}]
# [2026]
# ['[', '  {', '    "name":"Ann",']
# (2, 2)
# (2, 2) b'\x1f\x8b'
# {'n': 'int64', 'x': 'float64'}
# {'n': 'float64', 's': 'str'}
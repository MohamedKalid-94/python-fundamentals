import io
import tempfile
from pathlib import Path

import pandas as pd

# CSV FILES: pd.read_csv(path_or_buffer, ...)  and  df.to_csv(path_or_buffer, ...)
# The "file" can be a path, a URL, or any stream (io.StringIO(text), io.BytesIO(bytes)), which is used here.
#   READING   sep  header  names  index_col  usecols  dtype  converters  parse_dates  na_values  true_values/false_values
#             skiprows  skipfooter  nrows  comment  decimal  thousands  encoding  chunksize  dtype_backend
#   WRITING   index  columns  header  sep  na_rep  float_format  date_format  mode ("a" appends)  compression  encoding

simple = "a,b\n1,x\n2,y\n3,z\n"
df = pd.read_csv(io.StringIO(simple))
print(df, df.dtypes.astype(str).to_dict())

# Files without a header row, or with another delimiter and decimal comma
print(pd.read_csv(io.StringIO("1,x\n2,y\n"), header=None, names=["n", "label"]))
messy = "# sensor export\nid;name;temp;when;ok\n1;Ann;21,5;2026-11-15 10:00;yes\n2;Bo;;2026-11-15 10:05;no\n3;Cy;23,0;2026-11-15 10:10;yes\n"
data = pd.read_csv(io.StringIO(messy), sep=";", decimal=",", comment="#", parse_dates=["when"], true_values=["yes"], false_values=["no"])
print(data)
print(data.drop(columns="when").dtypes.astype(str).to_dict(), data["when"].dt.hour.tolist(), pd.api.types.is_datetime64_any_dtype(data["when"]))

# Choosing columns, the index, and how many rows
print(pd.read_csv(io.StringIO(simple), usecols=["b"]).columns.tolist(), pd.read_csv(io.StringIO(simple), index_col="a").index.tolist())
print(pd.read_csv(io.StringIO(simple), nrows=2).shape, pd.read_csv(io.StringIO(simple), skiprows=2, header=None).values.tolist())
print(pd.read_csv(io.StringIO(simple + "total,3\n"), skipfooter=1, engine="python").shape)

# Missing values and types
text = "id,code,score\n1,007,10\n2,010,NA\n3,200,-999\n"
print(pd.read_csv(io.StringIO(text))["code"].tolist())                                       # leading zeros are lost: 007 becomes 7
print(pd.read_csv(io.StringIO(text), dtype={"code": str})["code"].tolist())                  # keep them with dtype=str
print(pd.read_csv(io.StringIO(text), na_values=["NA", "-999"])["score"].tolist())
print(pd.read_csv(io.StringIO(text), na_values=["NA", "-999"], dtype_backend="numpy_nullable").dtypes.astype(str).to_dict())
print(pd.read_csv(io.StringIO(text), dtype={"id": "int32"}).dtypes.astype(str).to_dict())
print(pd.read_csv(io.StringIO("name\nann\nbo\n"), converters={"name": str.upper})["name"].tolist())
print(pd.read_csv(io.StringIO('n\n"1,234"\n"5,678"\n'), thousands=",")["n"].tolist())

# Quotes and commas inside a field, and other encodings
quoted = 'name,note\n"Smith, J.","said ""hi"""\nBo,ok\n'
print(pd.read_csv(io.StringIO(quoted)).values.tolist())
print(pd.read_csv(io.BytesIO("name\ncafé\n".encode("latin-1")), encoding="latin-1")["name"].tolist())

# A file too big for memory: read it in chunks
big = "n\n" + "\n".join(str(i) for i in range(10)) + "\n"
total = 0
sizes = []
for chunk in pd.read_csv(io.StringIO(big), chunksize=4):
    sizes.append(len(chunk))
    total += int(chunk["n"].sum())
print(sizes, total)

# WRITING
frame = pd.DataFrame({"name": ["Ann", "Bo, Jr."], "temp": [21.456, None], "ok": [True, False]}, index=["r1", "r2"])
print(frame.to_csv(), end="")
print(frame.to_csv(index=False, float_format="%.1f", na_rep="NA"), end="")
print(frame.to_csv(columns=["name", "ok"], header=False, index=False, sep=";"), end="")
with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "out.csv"
    frame.to_csv(path)
    back = pd.read_csv(path, index_col=0)
    print(back.equals(frame), back.index.tolist(), path.read_text().splitlines()[0])
    frame.to_csv(path, mode="a", header=False)                                              # append more rows
    print(len(path.read_text().splitlines()))
    zipped = Path(folder) / "out.csv.gz"
    frame.to_csv(zipped, compression="gzip")                                                # the extension chooses the compression
    print(pd.read_csv(zipped, index_col=0).shape, zipped.read_bytes()[:2])

# Dates are written as text, and read back as text unless you ask for dates
stamps = pd.DataFrame({"t": pd.to_datetime(["2026-11-15 10:00", "2026-11-15 10:05"]), "v": [1, 2]})
text = stamps.to_csv(index=False, date_format="%d/%m/%Y %H:%M")
print(text.splitlines()[1], pd.read_csv(io.StringIO(text))["t"].dtype, pd.read_csv(io.StringIO(text), parse_dates=["t"], dayfirst=True)["t"].dt.day.tolist())

# EXPECTED OUTPUT
#    a  b
# 0  1  x
# 1  2  y
# 2  3  z {'a': 'int64', 'b': 'str'}
#    n label
# 0  1     x
# 1  2     y
#    id name  temp                when     ok
# 0   1  Ann  21.5 2026-11-15 10:00:00   True
# 1   2   Bo   NaN 2026-11-15 10:05:00  False
# 2   3   Cy  23.0 2026-11-15 10:10:00   True
# {'id': 'int64', 'name': 'str', 'temp': 'float64', 'ok': 'bool'} [10, 10, 10] True
# ['b'] [1, 2, 3]
# (2, 2) [[2, 'y'], [3, 'z']]
# (3, 2)
# [7, 10, 200]
# ['007', '010', '200']
# [10.0, nan, nan]
# {'id': 'Int64', 'code': 'Int64', 'score': 'Int64'}
# {'id': 'int32', 'code': 'int64', 'score': 'float64'}
# ['ANN', 'BO']
# [1234, 5678]
# [['Smith, J.', 'said "hi"'], ['Bo', 'ok']]
# ['café']
# [4, 4, 2] 45
# ,name,temp,ok
# r1,Ann,21.456,True
# r2,"Bo, Jr.",,False
# name,temp,ok
# Ann,21.5,True
# "Bo, Jr.",NA,False
# Ann;True
# Bo, Jr.;False
# True ['r1', 'r2'] ,name,temp,ok
# 5
# (2, 3) b'\x1f\x8b'
# 15/11/2026 10:00,1 str [15, 15]
import numpy as np

# RECORD ARRAYS (np.recarray): a structured array whose fields can ALSO be read as attributes: r.temp
#   np.rec.array(list_of_tuples, dtype=...)       np.rec.fromrecords(list, names="a,b")
#   np.rec.fromarrays([arr1, arr2], names="a,b")  a_structured_array.view(np.recarray)
# Attribute access is convenient, but a record array is slower than a plain structured array, and a field
# named like an array attribute (shape, size, ...) cannot be reached with a dot. Prefer a["name"] in new code.

dtype = np.dtype([("id", "<u2"), ("temp", "<f4"), ("tag", "U6")])
r = np.rec.array([(1, 21.5, "lab"), (2, 22.0, "roof")], dtype=dtype)
print(type(r).__name__, type(r[0]).__name__)
print(r.id, r.temp, r[0].tag, r.tag)
r.temp = [30.0, 31.0]                          # attribute assignment writes into the array
r[1].tag = "attic"
print(r.temp, r.tag, r["temp"])

print(r.dtype.names, r.shape)
print(r[r.temp > 30.5].id)

# Building them
ids = np.array([1, 2, 3])
temps = np.array([20.0, 21.0, 22.0])
by_arrays = np.rec.fromarrays([ids, temps], names="id,temp")
by_records = np.rec.fromrecords([(1, 20.0), (2, 21.0)], names="id,temp")
print(by_arrays.temp.mean(), by_records.id, by_arrays.dtype.names)

# Converting
structured = np.zeros(2, dtype=dtype)
as_records = structured.view(np.recarray)
as_plain = as_records.view(np.ndarray)
print(type(structured).__name__, type(as_records).__name__, type(as_plain).__name__)
print(np.shares_memory(structured, as_records))
print(r.tolist()[0], by_arrays[0])

# A record array as a lookup table
sensors = np.rec.fromrecords([("temp", 0.1, -40.0), ("press", 0.5, 300.0)], names="name,scale,offset")
row = sensors[sensors.name == "press"][0]
print(row.scale, row.offset, 200 * row.scale + row.offset)

# EXPECTED OUTPUT
# recarray record
# [1 2] [21.5 22. ] lab ['lab' 'roof']
# [30. 31.] ['lab' 'attic'] [30. 31.]
# ('id', 'temp', 'tag') (2,)
# [2]
# 21.0 [1 2] ('id', 'temp')
# ndarray recarray ndarray
# True
# (1, 30.0, 'lab') (1, 20.0)
# 0.5 300.0 400.0
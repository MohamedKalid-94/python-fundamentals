import numpy as np
import numpy.lib.recfunctions as rfn

# STRUCTURED ARRAYS: every element is a RECORD with NAMED, TYPED fields (like a C struct).
# Ways to describe the dtype:
#   a list of (name, type) tuples       [("id", "<u2"), ("temp", "<f4"), ("tag", "U6")]
#   a string                            "u2, f4, U6"        (the fields are named f0, f1, f2)
#   a dict with names, formats, offsets, itemsize           (full control of the memory layout)
# Access a whole field with a["name"] (a VIEW), one record with a[i].

reading = np.dtype([("id", "<u2"), ("temp", "<f4"), ("tag", "U6")])
print(reading.names, reading.itemsize)
a = np.zeros(3, dtype=reading)
print(a)
a["id"] = [1, 2, 3]
a["temp"] = [21.5, 22.0, 23.5]
a["tag"] = ["lab", "roof", "cellar"]
a[0] = (10, 20.5, "lab")                       # assign a whole record with a tuple
print(a)
print(a["temp"], a[1], a[1]["tag"], a[a["temp"] > 21.7]["id"])
print(np.dtype("u2, f4, U6").names)

# A packed layout and a C-aligned layout (see the padding bytes a C compiler adds)
packed = np.dtype({"names": ["header", "length", "value"], "formats": ["u1", "<u2", "<f4"],
                   "offsets": [0, 1, 3], "itemsize": 7})
aligned = np.dtype([("header", "u1"), ("length", "<u2"), ("value", "<f4")], align=True)
print(packed.itemsize, aligned.itemsize)
print({name: aligned.fields[name][1] for name in aligned.names})      # the byte offset of every field

# Sub-arrays and nested records
point = np.dtype([("pos", "<f4", (3,)), ("meta", [("ok", "?"), ("crc", "<u2")])])
p = np.zeros(2, dtype=point)
p["pos"][0] = [1, 2, 3]
p["meta"]["crc"] = [0xBEEF, 0x1234]
print(p["pos"].shape, p["pos"][0], hex(int(p["meta"]["crc"][0])), p.dtype["meta"].names)

# Sorting and comparing
b = np.array([(3, 22.0, "c"), (1, 25.0, "a"), (2, 22.0, "b")], dtype=reading)
print(np.sort(b, order="temp")["id"])                                # the fields after "temp" break ties: id 2 before id 3
print(np.sort(b, order=["temp", "id"])[::-1]["id"], b["id"][np.argsort(b, order="id")])
print(np.array_equal(b, b.copy()), (b == b[0]).tolist())

# Several fields at once: a view with the same layout, or a plain 2-D array
numbers = b[["id", "temp"]]
print(numbers.dtype.names, rfn.structured_to_unstructured(numbers))
table = np.array([[1.0, 2.5], [2.0, 3.5]])
print(rfn.unstructured_to_structured(table, np.dtype([("x", "f4"), ("y", "f4")])))

# recfunctions: add, rename, drop and merge fields (each returns a NEW array)
c = rfn.append_fields(b, "ok", [True, False, True], usemask=False)
print(c.dtype.names)
c = rfn.rename_fields(c, {"temp": "celsius"})
c = rfn.drop_fields(c, "tag")
print(c.dtype.names, c["ok"].tolist())
merged = rfn.merge_arrays((np.array([1, 2], dtype=[("a", "i4")]), np.array([0.5, 1.5], dtype=[("b", "f8")])), flatten=True)
print(merged.dtype.names, merged["b"])

# Bytes in, bytes out: a binary packet array (links to Module 25 and Module 16)
frame = np.array([(7, 1.5), (8, 2.5)], dtype=[("id", "<u2"), ("value", "<f4")])
raw = frame.tobytes()
print(len(raw), raw[:6])
print(np.frombuffer(raw, dtype=frame.dtype)["value"])

# EXPECTED OUTPUT
# ('id', 'temp', 'tag') 30
# [(0, 0., '') (0, 0., '') (0, 0., '')]
# [(10, 20.5, 'lab') ( 2, 22. , 'roof') ( 3, 23.5, 'cellar')]
# [20.5 22.  23.5] (2, 22.0, 'roof') roof [2 3]
# ('f0', 'f1', 'f2')
# 7 8
# {'header': 0, 'length': 2, 'value': 4}
# (2, 3) [1. 2. 3.] 0xbeef ('ok', 'crc')
# [2 3 1]
# [1 3 2] [1 2 3]
# True [True, False, False]
# ('id', 'temp') [[ 3. 22.]
#  [ 1. 25.]
#  [ 2. 22.]]
# [(1., 2.5) (2., 3.5)]
# ('id', 'temp', 'tag', 'ok')
# ('id', 'celsius', 'ok') [True, False, True]
# ('a', 'b') [0.5 1.5]
# 12 b'\x07\x00\x00\x00\xc0?'
# [1.5 2.5]
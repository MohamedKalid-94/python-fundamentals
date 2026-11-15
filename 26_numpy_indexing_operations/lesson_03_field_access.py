import numpy as np

# FIELD ACCESS: arrays whose elements have NAMED FIELDS (a "structured" dtype), like a C struct.
# The full story (creating, sorting, record arrays) is in Module 28. Here: reading and writing by name.
#   a["name"]            the whole column of that field (a VIEW)
#   a[["name", "age"]]   several fields
#   a[0]                 one element (a record)

people = np.array(
    [("Ann", 25, 55.5), ("Bo", 31, 70.2), ("Cy", 19, 62.0)],
    dtype=[("name", "U10"), ("age", "i4"), ("weight", "f4")],
)
print(people.dtype)
print(people.shape, people[0])
print(people["name"])
print(people["age"].mean())
print(people[["name", "age"]])                       # several fields
people["age"][1] = 32                                # a field is a view: writing changes the array
people["weight"] += 1
print(people["age"], people["weight"])
print(people[people["age"] > 20]["name"])            # a mask on one field
print(people.dtype.names, people.dtype["age"])
print(people.itemsize, people.nbytes)                # 40 + 4 + 4 = 48 bytes per record

# EXPECTED OUTPUT
# [('name', '<U10'), ('age', '<i4'), ('weight', '<f4')]
# (3,) ('Ann', 25, 55.5)
# ['Ann' 'Bo' 'Cy']
# 25.0
# [('Ann', 25) ('Bo', 31) ('Cy', 19)]
# [25 32 19] [56.5 71.2 63. ]
# ['Ann' 'Bo']
# ('name', 'age', 'weight') int32
# 48 144
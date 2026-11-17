import timeit

import numpy as np

# PERFORMANCE OPTIMIZATION with arrays: the rules, in order of importance
#   1. VECTORIZE: replace Python loops with whole-array operations (ufuncs, masks, broadcasting, np.dot)
#   2. CHOOSE the smallest dtype that is accurate enough (float32 instead of float64 halves memory and traffic)
#   3. AVOID COPIES and temporaries: views, out=, in-place operators, preallocated results
#   4. KEEP the memory layout in mind: C order (rows contiguous) vs Fortran order (columns contiguous)
#   5. MEASURE before you optimise: timeit, cProfile (Module 18). The lines below print True/False, not times,
#      because times differ from computer to computer.

# 1. VECTORIZATION
n = 1_000_000
numbers = np.arange(n, dtype=np.float64)
as_list = numbers.tolist()


def loop_sum_of_squares():
    total = 0.0
    for x in as_list:
        total += x * x
    return total


loop_time = min(timeit.repeat(loop_sum_of_squares, number=1, repeat=3))
vector_time = min(timeit.repeat(lambda: np.dot(numbers, numbers), number=20, repeat=3)) / 20
print(np.isclose(loop_sum_of_squares(), np.dot(numbers, numbers)), loop_time > 10 * vector_time)

# A branch without a loop
temps = np.array([18.0, 25.0, 31.0, 22.0])
print(np.where(temps > 24, "hot", "ok"), np.select([temps < 20, temps < 30], [0, 1], default=2))

# All pairwise distances: broadcasting instead of two nested loops
points = np.arange(40, dtype=float).reshape(20, 2)
loops = np.zeros((20, 20))
for i in range(20):
    for j in range(20):
        loops[i, j] = np.sqrt(((points[i] - points[j]) ** 2).sum())
broadcast = np.sqrt(((points[:, None, :] - points[None, :, :]) ** 2).sum(axis=-1))
print(np.allclose(loops, broadcast))

# 2. DTYPES: memory and precision
x = np.linspace(0, 1, 1_000_000)
print(x.nbytes, x.astype(np.float32).nbytes, x.astype(np.float16).nbytes)
print(abs(x.sum() - x.astype(np.float32).sum()) / x.sum() < 1e-4)

# 3. COPIES AND TEMPORARIES
a = np.arange(5, dtype=float)
b = np.ones(5)
c = np.full(5, 10.0)
plain = a * b + c                                      # creates temporary arrays
reused = np.empty(5)
np.multiply(a, b, out=reused)                          # writes into an existing array
np.add(reused, c, out=reused)
print(np.array_equal(plain, reused))
a += 1                                                 # in place: no new array
print(a)
view = numbers[100:200]
print(view.base is numbers, np.shares_memory(view, numbers), view.nbytes)       # a slice copies nothing
parts = [numbers[i:i + 250_000].sum() for i in range(0, n, 250_000)]            # process in chunks
print(np.isclose(sum(parts), numbers.sum()))

# Preallocate instead of growing an array in a loop
grown = np.array([])
for i in range(5):
    grown = np.append(grown, i * i)                    # a new, bigger array is allocated every time
prefilled = np.empty(5)
for i in range(5):
    prefilled[i] = i * i
print(np.array_equal(grown, prefilled), np.array_equal(prefilled, np.arange(5) ** 2))

# 4. MEMORY LAYOUT
c_order = np.zeros((1000, 1000))
f_order = np.asfortranarray(c_order)
print(c_order.flags["C_CONTIGUOUS"], f_order.flags["F_CONTIGUOUS"], c_order.strides, f_order.strides)
# Reading along the contiguous axis walks through memory in order (fast, cache friendly);
# the other axis jumps by a whole row every step. The results are equal, only the speed differs.
print(np.array_equal(c_order.sum(axis=0), c_order.sum(axis=1)))
transposed = c_order.T                                  # a view: only the strides changed
print(transposed.flags["C_CONTIGUOUS"], transposed.flags["F_CONTIGUOUS"], np.shares_memory(c_order, transposed))
repacked = np.ascontiguousarray(transposed)             # a real copy in the new order
print(repacked.flags["C_CONTIGUOUS"], np.shares_memory(c_order, repacked))
print(np.zeros((3, 4), order="F").strides, np.zeros((3, 4)).strides)

# Structure of arrays vs array of structures: a field of a structured array is NOT contiguous
records = np.zeros(1000, dtype=[("t", "<f8"), ("v", "<f4"), ("flag", "u1")])
print(records.itemsize, records["v"].strides, records["v"].flags["C_CONTIGUOUS"])
separate = np.ascontiguousarray(records["v"])           # copy one field out for heavy calculations
print(separate.strides)

# 5. Which is faster? Measure, do not guess. Example: sorting before searching many times
data = np.random.default_rng(0).integers(0, 1_000_000, 200_000)
queries = np.random.default_rng(1).integers(0, 1_000_000, 2_000)
ordered = np.sort(data)
position = np.searchsorted(ordered, queries)
print(position.shape, bool((position >= 0).all()))

# EXPECTED OUTPUT
# True True
# ['ok' 'hot' 'hot' 'ok'] [0 1 2 1]
# True
# 8000000 4000000 2000000
# True
# True
# [1. 2. 3. 4. 5.]
# True True 800
# True
# True True
# True True (8000, 8) (8, 8000)
# True
# False True True
# True False
# (8, 24) (32, 8)
# 13 (13,) False
# (4,)
# (2000,) True
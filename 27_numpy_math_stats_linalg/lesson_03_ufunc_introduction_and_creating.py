import numpy as np

# UFUNC = "universal function": a compiled function that works element by element, with
#   broadcasting, type conversion, and the options  out=  (where to write)  and  where=  (at which positions).
# np.add, np.sin, np.greater, np.bitwise_and, np.maximum ... are all ufuncs.
# A ufunc also has METHODS:  reduce  accumulate  outer  at  reduceat

print(isinstance(np.add, np.ufunc), isinstance(np.median, np.ufunc), np.add.nin, np.add.nout, np.divmod.nout)
print("dd->d" in np.add.types, "f->f" in np.sin.types)                       # the types it was compiled for

a = np.array([1, 2, 3, 4])
print(np.add.reduce(a), np.multiply.reduce(a), np.maximum.reduce(a))          # a whole axis down to one value
print(np.add.accumulate(a), np.multiply.accumulate(a), np.maximum.accumulate([3, 1, 4, 1, 5]))   # the running values
print(np.multiply.outer([1, 2, 3], [10, 20]))                                 # every pair
print(np.add.reduceat(np.arange(8), [0, 3, 5]))                               # sums of [0:3], [3:5], [5:]
m = np.arange(6).reshape(2, 3)
print(np.add.reduce(m, axis=0), np.add.reduce(m, axis=1), np.add.reduce(m, axis=None))
print(np.add.reduce(m, axis=0, keepdims=True))
x = np.zeros(4, dtype=int)
np.add.at(x, [0, 0, 3], 5)                                                    # unbuffered: repeats count
print(x)

# out= and where=
out = np.empty(3)
np.multiply([1, 2, 3], 2.5, out=out)
print(out)
roots = np.sqrt(np.array([4.0, -1.0, 9.0]), where=np.array([True, False, True]), out=np.zeros(3))
print(roots)                                                                  # where= False: out is left as it was
print(np.add(np.array([1, 2]), 1, dtype=np.float32).dtype)                    # choose the calculation type

# CREATING YOUR OWN "UFUNC"
def clamp_scale(x, k):
    return min(x, 10) * k

vec = np.vectorize(clamp_scale)                    # a Python loop in disguise: convenient, NOT fast
print(vec(np.array([1, 5, 20]), 2))
vec_float = np.vectorize(clamp_scale, otypes=[float])
print(vec_float([1, 5, 20], 0.5))

plus = np.frompyfunc(lambda a, b: a + b, 2, 1)     # a real ufunc object, but it returns OBJECT arrays
print(plus(np.array([1, 2]), np.array([10, 20])), plus.nin, plus.nout, plus(np.array([1, 2]), 1).dtype)
print(plus.reduce([1, 2, 3, 4]), plus.accumulate([1, 2, 3, 4]))

# Better: express the calculation with real ufuncs, which run in compiled code
print(np.minimum(np.array([1, 5, 20]), 10) * 2)
# Faster than a Python function and not limited to one type. A tool like Numba (outside this course)
# can compile a real Python function into a fast ufunc when you cannot avoid writing a loop.

# EXPECTED OUTPUT
# True False 2 1 2
# True True
# 10 24 4
# [ 1  3  6 10] [ 1  2  6 24] [3 3 4 4 5]
# [[10 20]
#  [20 40]
#  [30 60]]
# [ 3  7 18]
# [3 5 7] [ 3 12] 15
# [[3 5 7]]
# [10  0  0  5]
# [2.5 5.  7.5]
# [2. 0. 3.]
# float32
# [ 2 10 20]
# [0.5 2.5 5. ]
# [11 22] 2 1 object
# 10 [1 3 6 10]
# [ 2 10 20]
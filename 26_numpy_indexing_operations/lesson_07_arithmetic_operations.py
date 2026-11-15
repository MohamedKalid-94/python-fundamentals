import numpy as np

# ARITHMETIC OPERATIONS work element by element, with broadcasting.
#   +  np.add          -  np.subtract       *  np.multiply     /  np.divide (always a float result)
#   // np.floor_divide  %  np.mod            ** np.power        -x np.negative
# The functions accept  out=  (write into an existing array)  and  where=  (only at some positions).

a = np.array([10, 20, 30])
b = np.array([1, 2, 3])

# Addition and subtraction
print(a + b, a - b, a + 5, 100 - a)
# Multiplication (element by element: NOT a matrix product, that is @ in Module 27)
print(a * b, a * 2, a ** 2, 2 ** b)
# Division
print(a / b, a // b, a % 7, np.divmod(a, 7))
print((a / b).dtype, (a // b).dtype, (b * 1.5).dtype)
print(np.floor_divide(-7, 2), -7 // 2, np.mod(-7, 3), np.fmod(-7, 3))     # floor vs truncation for negatives

# In-place operators change the array. The result must fit the dtype.
c = np.array([1, 2, 3])
c += 5
c *= 2
print(c)
try:
    c += 0.5                                      # a float result does not fit back into an int array
except TypeError as error:
    print("TypeError:", str(error)[:50])
f = c.astype(float)
f += 0.5
print(f)

# out= and where=
out = np.zeros(3)
np.add(a, b, out=out)
print(out)
r = np.array([4.0, 0.0, 9.0])
print(np.divide(1.0, r, out=np.full(3, -1.0), where=r != 0))      # no division where r is 0

# Division by zero gives inf or nan (and a warning, hidden here with errstate)
with np.errstate(divide="ignore", invalid="ignore"):
    print(np.array([1.0, -1.0, 0.0]) / 0.0)
    print(np.array([1, 2]) // 0)                  # integer division by zero gives 0

# Types: mixing dtypes (Module 25, lesson 03)
small = np.array([100, 120], dtype=np.int8)
print(small + small)                              # int8 wraps around
print(small.astype(np.int16) + small)             # widen first
print(np.array([1, 2], dtype=np.float32) + 1.5, (np.array([1, 2], dtype=np.float32) + 1.5).dtype)

# Operators on whole tables, with broadcasting
table = np.array([[1, 2, 3], [4, 5, 6]])
print(table + np.array([10, 20, 30]))
print(table * np.array([[1], [-1]]))
print(table.sum(), table.sum(axis=0), table.prod(axis=1))

# EXPECTED OUTPUT
# [11 22 33] [ 9 18 27] [15 25 35] [90 80 70]
# [10 40 90] [20 40 60] [100 400 900] [2 4 8]
# [10. 10. 10.] [10 10 10] [3 6 2] (array([1, 2, 4]), array([3, 6, 2]))
# float64 int64 float64
# -4 -4 2 -1
# [12 14 16]
# TypeError: Cannot cast ufunc 'add' output from dtype('float64
# [12.5 14.5 16.5]
# [11. 22. 33.]
# [ 0.25       -1.          0.11111111]
# [ inf -inf  nan]
# [0 0]
# [-56 -16]
# [200 240]
# [2.5 3.5] float32
# [[11 22 33]
#  [14 25 36]]
# [[ 1  2  3]
#  [-4 -5 -6]]
# 21 [5 7 9] [  6 120]
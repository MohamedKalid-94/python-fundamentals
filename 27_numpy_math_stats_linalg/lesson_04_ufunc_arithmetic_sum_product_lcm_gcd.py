import math

import numpy as np

# THE UFUNCS BY GROUP (the topics of your syllabus)
#   arithmetic    add subtract multiply divide power mod absolute negative reciprocal
#   summation     np.sum  add.reduce  cumsum  add.accumulate
#   product       np.prod multiply.reduce cumprod
#   difference    np.diff  np.ediff1d  np.gradient
#   LCM and GCD   np.lcm  np.gcd (with .reduce for a whole array)
#   trigonometric, hyperbolic, logarithmic, rounding: lessons 01 and 02
#   set operations: boolean ufuncs on masks (below); np.unique, np.union1d ... are functions, not ufuncs

a = np.array([4, 6, 8, 12])
print(np.add(a, 1), np.subtract(a, 1), np.multiply(a, 2), np.divide(a, 4))
print(np.power(a, 2), np.mod(a, 5), np.absolute(-a), np.negative(a), np.reciprocal(np.array([2.0, 4.0])))

# SUMMATION
print(np.sum(a), np.add.reduce(a), np.cumsum(a), np.add.accumulate(a))
m = np.arange(1, 7).reshape(2, 3)
print(m.sum(), m.sum(axis=0), m.sum(axis=1), m.sum(axis=1, keepdims=True).shape, np.sum(m, dtype=float))
print(np.sum(np.array([200, 100], dtype=np.uint8)))                           # 300: small ints are summed in a wider type
print(sum([0.1] * 10) == 1.0, math.fsum([0.1] * 10) == 1.0)                   # a plain float sum drifts; math.fsum is exact

# PRODUCT
print(np.prod(a), np.multiply.reduce(a), np.cumprod([1, 2, 3, 4, 5]), np.prod(m, axis=0))
print(np.prod(np.arange(1, 21)), np.prod(np.arange(1, 22)), np.prod(np.arange(1.0, 22.0)))   # int64 overflow at 21!

# DIFFERENCE
s = np.array([1, 4, 9, 16, 25])
print(np.diff(s), np.diff(s, n=2), np.diff(m, axis=1), np.ediff1d(s))
print(np.diff(s, prepend=0), np.gradient(np.array([1.0, 4.0, 9.0, 16.0])))
print(np.diff(np.array([3, 7, 7, 12])) > 0)                                    # which steps went up?

# LCM and GCD
print(np.lcm(12, 18), np.gcd(12, 18), np.gcd([12, 18, 24], 6), np.lcm([2, 3, 4], 6))
print(np.lcm.reduce([4, 6, 10]), np.gcd.reduce([12, 18, 24]))                  # for a whole array
# Use: tasks that run every 4, 6 and 10 ms all start together again after np.lcm.reduce = 60 ms

# SET OPERATIONS with boolean ufuncs: a set as a True/False mask over a universe 1..7
universe = np.arange(1, 8)
in_x = np.isin(universe, [1, 2, 3, 4, 5])
in_y = np.isin(universe, [4, 5, 6])
print(np.logical_and(in_x, in_y), np.logical_or(in_x, in_y), np.logical_xor(in_x, in_y), np.logical_not(in_x))
print(universe[in_x & in_y], universe[in_x | in_y], universe[in_x & ~in_y], universe[in_x ^ in_y])

# maximum and minimum are ufuncs too (element by element, unlike max and min)
print(np.maximum([1, 5, 3], [4, 2, 6]), np.minimum([1, 5, 3], 4), np.fmax([1.0, np.nan], [np.nan, 2.0]))

# EXPECTED OUTPUT
# [ 5  7  9 13] [ 3  5  7 11] [ 8 12 16 24] [1.  1.5 2.  3. ]
# [ 16  36  64 144] [4 1 3 2] [ 4  6  8 12] [ -4  -6  -8 -12] [0.5  0.25]
# 30 30 [ 4 10 18 30] [ 4 10 18 30]
# 21 [5 7 9] [ 6 15] (2, 1) 21.0
# 300
# False True
# 2304 2304 [  1   2   6  24 120] [ 4 10 18]
# 2432902008176640000 -4249290049419214848 5.109094217170944e+19
# [3 5 7 9] [2 2 2] [[1 1]
#  [1 1]] [3 5 7 9]
# [1 3 5 7 9] [3. 4. 6. 7.]
# [ True False  True]
# 36 6 [6 6 6] [ 6  6 12]
# 60 6
# [False False False  True  True False False] [ True  True  True  True  True  True False] [ True  True  True False False  True False] [False False False False False  True  True]
# [4 5] [1 2 3 4 5 6] [1 2 3] [1 2 3 6]
# [4 5 6] [1 4 3] [1. 2.]
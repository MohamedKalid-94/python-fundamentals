import numpy as np

# EXPONENTIAL                                   LOGARITHMIC
#   np.exp(x)    e**x                             np.log     natural log        np.log10   np.log2
#   np.exp2(x)   2**x                             np.log1p(x) = log(1 + x), accurate for tiny x
#   np.expm1(x)  = exp(x) - 1, accurate for tiny x   np.logaddexp(a, b) = log(exp(a) + exp(b))
#   np.power  np.sqrt  np.cbrt  np.square
# ROUNDING
#   np.round(x, decimals)  half goes to the EVEN neighbour       np.floor   toward minus infinity
#                          (it scales, rounds and scales back: results can differ from Python's round)
#   np.ceil   toward plus infinity                               np.trunc / np.fix   toward zero
#   np.rint   to the nearest integer (float result)              np.modf   fractional and integer parts

x = np.array([0.0, 1.0, 2.0])
print(np.round(np.exp(x), 4), np.exp2(x), np.sqrt([4.0, 9.0]), np.cbrt([8.0, -27.0]), np.square([3, 4]))
print(f"{np.expm1(1e-10):.12e}  {np.exp(1e-10) - 1:.12e}")                  # expm1 keeps the digits
print(np.round(np.log([1, np.e, np.e ** 2]), 6), np.log10([1, 10, 1000]), np.log2([1, 8, 1024]))
with np.errstate(divide="ignore", invalid="ignore"):
    print(np.log([0.0, -1.0, 1.0]))                                          # -inf, nan, 0

# Decibels: 20 * log10(amplitude ratio)
print(20 * np.log10([1, 10, 100, 0.1]))

# A numerically stable softmax (used in every classifier and language model)
scores = np.array([1000.0, 1001.0, 1002.0])
with np.errstate(over="ignore", invalid="ignore"):
    print(np.exp(scores) / np.exp(scores).sum())                             # exp(1000) overflows: nan
shifted = np.exp(scores - scores.max())                                      # subtract the maximum first
print(np.round(shifted / shifted.sum(), 4))
print(np.round(np.logaddexp.reduce(scores), 4))                              # log(sum(exp(scores))), stable

# ROUNDING
v = np.array([-2.5, -1.5, -0.5, 0.5, 1.5, 2.5])
print(np.round(v) + 0.0)                                                     # half to even: -2 -2 0 0 2 2
print(np.floor(v).astype(int), np.ceil(v).astype(int), np.trunc(v).astype(int), np.rint(v).astype(int))
print(np.round(2.675, 2), round(2.675, 2))                                    # NumPy 2.68, Python 2.67: they differ!
print(np.round(1234.567, -2), np.round([1.2345, 2.3456], 3))               # negative decimals round to hundreds
print(np.round(5.5), np.round(6.5))
print(np.modf(np.array([1.25, -1.25])))
print(np.round(np.array([0.1, 0.37, 0.62]) / 0.25) * 0.25)                    # round to a multiple of 0.25

# sign, abs, clip
print(np.sign([-3.0, 0.0, 2.0]), np.abs([-3, 4]), np.clip([-5, 5, 15], 0, 10))

# EXPECTED OUTPUT
# [1.     2.7183 7.3891] [1. 2. 4.] [2. 3.] [ 2. -3.] [ 9 16]
# 1.000000000050e-10  1.000000082740e-10
# [0. 1. 2.] [0. 1. 3.] [ 0.  3. 10.]
# [-inf  nan   0.]
# [  0.  20.  40. -20.]
# [nan nan nan]
# [0.09   0.2447 0.6652]
# 1002.4076
# [-2. -2.  0.  0.  2.  2.]
# [-3 -2 -1  0  1  2] [-2 -1  0  1  2  3] [-2 -1  0  0  1  2] [-2 -2  0  0  2  2]
# 2.68 2.67
# 1200.0 [1.234 2.346]
# 6.0 6.0
# (array([ 0.25, -0.25]), array([ 1., -1.]))
# [0.   0.25 0.5 ]
# [-1.  0.  1.] [3 4] [ 0  5 10]
import numpy as np

# ARRAYS FROM NUMERICAL RANGES
#   arange(start, stop, step)      like range(): the STOP is excluded; floats are allowed
#   linspace(start, stop, num)     num points, the STOP is INCLUDED (endpoint=True)
#   logspace(start, stop, num)     powers of 10 from 10**start to 10**stop
#   geomspace(start, stop, num)    values between start and stop with equal RATIOS
#   meshgrid(x, y)                 coordinate grids for 2-D calculations

print(np.arange(5))
print(np.arange(2, 10, 3))
print(np.arange(5, 0, -2))
print(np.arange(0, 1, 0.25))

# arange with a float step can give a surprising LENGTH (rounding). Prefer linspace for floats.
print(np.arange(1, 1.3, 0.1))
print(len(np.arange(1, 1.3, 0.1)))              # 4, not 3: the "excluded" stop slipped in
print(np.linspace(0, 1, 5))
print(np.linspace(0, 1, 5, endpoint=False))
values, step = np.linspace(0, 10, 5, retstep=True)
print(values, step)

print(np.logspace(0, 3, 4))
print(np.geomspace(1, 1000, 4))
print(np.logspace(0, 3, 4, base=2))

# A grid: evaluate a function on every (x, y) pair
x = np.linspace(0, 2, 3)
y = np.linspace(0, 1, 2)
xx, yy = np.meshgrid(x, y)
print(xx)
print(yy)
print(xx + yy)

# Sampling a signal: the time axis of a 5 Hz sine for 1 second at 20 samples per second
t = np.arange(0, 1, 1 / 20)
signal = np.sin(2 * np.pi * 5 * t)
print(t.shape, np.round(signal[:5], 3) + 0.0)         # + 0.0 turns a printed -0. into 0.

# EXPECTED OUTPUT
# [0 1 2 3 4]
# [2 5 8]
# [5 3 1]
# [0.   0.25 0.5  0.75]
# [1.  1.1 1.2 1.3]
# 4
# [0.   0.25 0.5  0.75 1.  ]
# [0.  0.2 0.4 0.6 0.8]
# [ 0.   2.5  5.   7.5 10. ] 2.5
# [   1.   10.  100. 1000.]
# [   1.   10.  100. 1000.]
# [1. 2. 4. 8.]
# [[0. 1. 2.]
#  [0. 1. 2.]]
# [[0. 0. 0.]
#  [1. 1. 1.]]
# [[0. 1. 2.]
#  [1. 2. 3.]]
# (20,) [ 0.  1.  0. -1.  0.]
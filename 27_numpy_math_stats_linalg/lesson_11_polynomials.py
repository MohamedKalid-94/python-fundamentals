import numpy as np
from numpy.polynomial import Polynomial

# POLYNOMIALS: use the class  numpy.polynomial.Polynomial
#   Polynomial([c0, c1, c2])      c0 + c1*x + c2*x**2      coefficients from LOW to HIGH degree
#   p(x)                          evaluate (a number or an array)
#   p.roots()  Polynomial.fromroots(r)  p.deriv()  p.integ()  p.degree()  p.coef
#   + - * // %  and  **           polynomial arithmetic
#   Polynomial.fit(x, y, deg)     a least-squares fit      .convert() gives plain coefficients
# THE OLD INTERFACE (np.poly1d, np.polyfit, np.polyval) lists coefficients from HIGH to LOW: a classic trap.

p = Polynomial([1, 2, 3])                      # 1 + 2x + 3x^2
print(p.coef, p.degree())
print(p(2), p(np.array([0, 1, 2])))            # 1 + 4 + 12 = 17

q = Polynomial([6, -5, 1])                     # x^2 - 5x + 6
print(q.roots(), Polynomial.fromroots([2, 3]).coef)
print(q(2), q(3))                              # zero at the roots

# Arithmetic
r = Polynomial([1, 1])                         # 1 + x
print((p + r).coef, (p - r).coef, (p * r).coef)
quotient, remainder = divmod(q, Polynomial([-2, 1]))     # divide by (x - 2)
print(quotient.coef, remainder.coef)
print((r ** 3).coef)                           # (1 + x)^3

# Calculus
print(p.deriv().coef, p.integ().coef, p.integ().deriv().coef)

# Fitting: exact data from y = 2x + 1
x = np.array([0.0, 1.0, 2.0, 3.0])
y = 2 * x + 1
line = Polynomial.fit(x, y, deg=1).convert()
print(np.round(line.coef, 6))

# A quadratic fit to noisy points; the scaled fit is converted back to plain coefficients
xs = np.arange(0.0, 6.0)
ys = np.array([0.1, 1.2, 3.9, 9.1, 15.8, 25.2])
curve = Polynomial.fit(xs, ys, deg=2).convert()
print(np.round(curve.coef, 3))
print(np.round(curve(np.array([6.0])), 2))

# The evaluation function and the old interface
print(np.polynomial.polynomial.polyval(2, [1, 2, 3]))        # polyval(x, coefficients low to high)
print(np.polyval([3, 2, 1], 2), np.polyfit(x, y, 1).round(6))      # OLD: high to low  [slope, intercept]
print(np.sort(np.roots([1, -5, 6])))                         # OLD: high to low

# Use: a sensor calibration curve. Raw ADC counts against known temperatures.
counts = np.array([100.0, 500.0, 1000.0, 2000.0, 3000.0])
degrees = np.array([-10.0, 10.0, 30.0, 70.0, 110.0])
calibration = Polynomial.fit(counts, degrees, deg=1).convert()
print(np.round(calibration.coef, 5), np.round(calibration(1500.0), 2))

# EXPECTED OUTPUT
# [1. 2. 3.] 2
# 17.0 [ 1.  6. 17.]
# [2. 3.] [ 6. -5.  1.]
# 0.0 0.0
# [2. 3. 3.] [0. 1. 3.] [1. 3. 5. 3.]
# [-3.  1.] [0.]
# [1. 3. 3. 1.]
# [2. 6.] [0. 1. 1. 1.] [1. 2. 3.]
# [1. 2.]
# [ 0.175 -0.148  1.027]
# [36.25]
# 17.0
# 17 [2. 1.]
# [2. 3.]
# [-11.96107   0.04088] 49.36
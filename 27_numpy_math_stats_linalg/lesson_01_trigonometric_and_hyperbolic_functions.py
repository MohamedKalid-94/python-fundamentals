import numpy as np

# MATHEMATICAL FUNCTIONS are "ufuncs": they work element by element on whole arrays (and on single numbers).
# TRIGONOMETRIC: angles are in RADIANS.
#   np.sin  np.cos  np.tan          np.arcsin  np.arccos  np.arctan       np.arctan2(y, x)  (the angle of a point)
#   np.radians / np.deg2rad         np.degrees / np.rad2deg               np.pi
#   np.hypot(x, y) = sqrt(x*x + y*y)                                      np.unwrap (remove 360-degree jumps)
# HYPERBOLIC: np.sinh  np.cosh  np.tanh          np.arcsinh  np.arccosh  np.arctanh

angles = np.array([0, 30, 45, 60, 90])
rad = np.radians(angles)
print(np.round(rad, 4), np.round(np.degrees(rad)))
print(np.round(np.sin(rad), 4), np.round(np.cos(rad), 4))
print(np.round(np.tan(np.radians([0, 45, 60])), 4))
print(np.isclose(np.sin(np.pi), 0), abs(np.sin(np.pi)) < 1e-15, np.sin(np.pi) == 0)    # floats are approximate

# Inverse functions return radians
print(np.round(np.degrees(np.arcsin([0, 0.5, 1])), 1), np.round(np.degrees(np.arccos(0.5)), 1))
print(np.round(np.degrees(np.arctan2([1, 1, -1, -1], [1, -1, -1, 1])), 1))   # the angle of 4 points, one per quadrant
with np.errstate(invalid="ignore"):
    print(np.arcsin(2.0))                                                    # outside [-1, 1]: nan

# hypot: the length of the hypotenuse
print(np.hypot(3, 4), np.hypot([3, 5], [4, 12]))

# unwrap: a phase that jumps from 300 to 40 degrees really continues to 400
phase = np.radians([0, 100, 200, 300, 40])
print(np.round(np.degrees(np.unwrap(phase))))

# HYPERBOLIC FUNCTIONS
x = np.array([-1.0, 0.0, 1.0])
print(np.round(np.sinh(x), 4), np.round(np.cosh(x), 4), np.round(np.tanh(x), 4))
print(np.round(np.arcsinh(x), 4), np.round(np.arccosh([1.0, 2.0]), 4), np.round(np.arctanh([-0.5, 0, 0.5]), 4))
print(np.allclose(np.cosh(x) ** 2 - np.sinh(x) ** 2, 1))                    # cosh^2 - sinh^2 = 1
print(np.round(np.tanh([-10.0, 0.0, 10.0]), 4))                              # squashes any number into (-1, 1)

# Use: a 50 Hz sine wave sampled at 1 kHz for 20 ms
t = np.arange(0, 0.02, 0.001)
wave = np.sin(2 * np.pi * 50 * t)
print(len(t), np.round(wave[:6], 3) + 0.0, np.round(wave.max(), 3))

# EXPECTED OUTPUT
# [0.     0.5236 0.7854 1.0472 1.5708] [ 0. 30. 45. 60. 90.]
# [0.     0.5    0.7071 0.866  1.    ] [1.     0.866  0.7071 0.5    0.    ]
# [0.     1.     1.7321]
# True True False
# [ 0. 30. 90.] 60.0
# [  45.  135. -135.  -45.]
# nan
# 5.0 [ 5. 13.]
# [  0. 100. 200. 300. 400.]
# [-1.1752  0.      1.1752] [1.5431 1.     1.5431] [-0.7616  0.      0.7616]
# [-0.8814  0.      0.8814] [0.    1.317] [-0.5493  0.      0.5493]
# True
# [-1.  0.  1.]
# 20 [0.    0.309 0.588 0.809 0.951 1.   ] 1.0
Write the questions as # comments and your solutions as code. Use assert and np.isclose to check your own answers.

Make a table of sin and cos for 0 to 360 degrees in steps of 30. Check that sin² + cos² = 1 for every row with np.allclose. Use arctan2 to find the heading of the vectors (1, 1), (-1, 1), (-1, -1) and (1, -1). Unwrap the phase [10, 170, 330, 20, 100] degrees.
Build 100 ms of a signal made of a 50 Hz and a 120 Hz sine wave sampled at 1 kHz. Find its peak and its mean. Compare the mean with 0 using np.isclose, not ==.
Convert amplitude ratios to decibels and back. Compute compound growth of 1000 at 5 percent for 10 years with exp. Show with 1e-10 that expm1 and log1p keep digits that exp(x) - 1 and log(1 + x) lose.
Write a stable softmax and a stable log-softmax for a 2-D batch of logits. Check that every row sums to 1. Show that the naive version fails for logits around 1000.
Compare floor, ceil, trunc, round and rint for the values -2.5 to 2.5 in steps of 0.5. Round a list of readings to the nearest 0.05. Show where np.round and Python’s round disagree for 0.5, 1.5 and 2.675.
With ufunc methods only: the running maximum of a list, a multiplication table from multiply.outer, group sums with add.reduceat, and counts of each value with np.add.at.
Write saturate(x, low, high) once with np.vectorize and once with np.clip. Check that the results are equal, then time both with timeit for 100,000 numbers (do not assert on the times) and explain the difference.
From a list of timestamps, compute the time between samples with diff, find gaps longer than twice the median interval, compute a cumulative energy with cumsum, and show where an int64 factorial table overflows compared with a float64 one.
Four tasks run every 4, 6, 10 and 15 ms. Find the common period with lcm.reduce, and the time offsets within it where all start together. Reduce the fractions [6/8, 10/15, 12/18] to lowest terms with gcd.
For a 3x4 table: the sum, mean, median, min and max by row, by column and overall; each row divided by its sum with keepdims; the same with a missing value and the nan functions; and an average of only the cells above a threshold with where=.
For 20 numbers you choose: mean, median, mode, variance and standard deviation with ddof=0 and ddof=1, IQR outliers, a weighted average, a 5-bin histogram, z-scores, and the correlation with a second list.
Simulate 10,000 dice rolls with a seed and compare each frequency with 1/6. Shuffle a deck of 52 cards, deal 5 cards without replacement, and split 100 samples 70/15/15 into train, validation and test sets. Show that two runs with the same seed give the same split.
For normal, poisson, exponential and binomial: draw 100,000 values, compare the mean and the variance with the theory, and write down the formulas. Simulate packet arrivals: show that Poisson counts per second and exponential gaps between packets describe the same process. Add noise to a sine wave and compute the signal-to-noise ratio in dB.
Two 3x3 matrices of integers you choose: check that (A B) C = A (B C), that (A B)ᵀ = Bᵀ Aᵀ, and that A B differs from B A. Build two 2-D rotation matrices, multiply them, and check that the result is a rotation by the sum of the angles. Apply it to five points.
Solve a system of three equations with solve, and compare with inv(A) @ b. Make a singular matrix and catch the LinAlgError. Compute the eigenvalues of a symmetric 3x3 matrix and check A v = λ v for every pair. For a small matrix with an obvious pattern, find the rank-1 and rank-2 approximations with the SVD and compare the error with the singular values.
Fit polynomials of degree 1, 2 and 3 to 8 noisy calibration points. Compare the residuals, find the roots and the derivative of the best one, and show the old-versus-new coefficient order trap with np.polyfit and Polynomial.fit.
Embedded exercise: build a thermistor lookup table. Take 10 (ADC count, temperature) points, fit a degree-3 polynomial, evaluate it for all 4096 possible ADC counts in one expression, and find the largest difference from the original points. Convert the table to hundredths of a degree with np.round(...).astype(np.int16), and prove that no value overflows int16.
Predict first, then run, and explain each result in a comment:
python
import numpy as np

a = np.array([2.5, 3.5, -2.5])
print(np.round(a), np.floor(a), np.trunc(a))
b = np.array([200, 100], dtype=np.uint8)
print(b.sum(), b.sum(dtype=np.uint8), (b + b).tolist())
print(np.add.reduce([[1, 2], [3, 4]], axis=1), np.multiply.outer([1, 2], [3, 4]).tolist())
print(np.linalg.det(np.array([[2.0, 0.0], [0.0, 3.0]])), np.diff([1, 4, 9, 16], n=2))
print((np.arange(3)[:, None] * np.arange(1, 4)).sum())
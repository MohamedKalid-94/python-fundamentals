import numpy as np

rng = np.random.default_rng(5)

# 1. A sensor log with missing values: summary and outliers with the IQR rule
readings = np.array([21.0, 21.4, np.nan, 20.8, 35.0, 21.1, 21.3, np.nan, 20.9, 21.2])
valid = readings[~np.isnan(readings)]
q1, q3 = np.percentile(valid, [25, 75])
spread = q3 - q1
low, high = q1 - 1.5 * spread, q3 + 1.5 * spread
outliers = valid[(valid < low) | (valid > high)]
print(len(valid), round(float(valid.mean()), 2), round(float(np.median(valid)), 2), outliers)

# 2. A moving average: with cumsum (fast, one pass) and with convolve
signal = np.array([1.0, 2.0, 6.0, 4.0, 5.0, 9.0])
window = 3
running = np.cumsum(np.insert(signal, 0, 0.0))
average = (running[window:] - running[:-window]) / window
print(average, np.allclose(average, np.convolve(signal, np.ones(window) / window, mode="valid")))

# 3. Monte Carlo: estimate pi from random points in the unit square
points = rng.random((200_000, 2))
inside = (points ** 2).sum(axis=1) < 1
print(abs(4 * inside.mean() - np.pi) < 0.02)

# 4. Linear regression with least squares, and R squared
x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
y = np.array([2.2, 4.1, 6.2, 7.8, 10.1, 12.2])
X = np.column_stack((x, np.ones_like(x)))
(slope, intercept), *_ = np.linalg.lstsq(X, y, rcond=None)
prediction = X @ np.array([slope, intercept])
r_squared = 1 - ((y - prediction) ** 2).sum() / ((y - y.mean()) ** 2).sum()
print(round(float(slope), 3), round(float(intercept), 3), round(float(r_squared), 4))

# 5. Softmax and cross-entropy loss (the core of a classifier), computed in a stable way
logits = np.array([[2.0, 1.0, 0.1], [0.5, 2.5, 0.3]])
shifted = logits - logits.max(axis=1, keepdims=True)
probabilities = np.exp(shifted) / np.exp(shifted).sum(axis=1, keepdims=True)
print(np.round(probabilities, 3), np.round(probabilities.sum(axis=1), 6))
labels = np.array([0, 1])
loss = -np.log(probabilities[np.arange(2), labels]).mean()
print(round(float(loss), 4))

# 6. Principal components with the SVD: how much of the variation lies along one direction?
data = np.array([[1.0, 2.1], [2.0, 3.9], [3.0, 6.2], [4.0, 7.8], [5.0, 10.1]])
centered = data - data.mean(axis=0)
U, s, Vt = np.linalg.svd(centered, full_matrices=False)
explained = s ** 2 / (s ** 2).sum()
print([f"{share:.2%}" for share in explained])
print(np.round(np.abs(centered @ Vt[0]), 3))             # the position of each point along the main axis

# 7. A circuit: two loops, mesh currents from Kirchhoff's voltage law  R @ I = V
R1, R2, R3, V = 100.0, 200.0, 300.0, 5.0
resistances = np.array([[R1 + R2, -R2], [-R2, R2 + R3]])
voltages = np.array([V, 0.0])
currents = np.linalg.solve(resistances, voltages)
print(np.round(currents * 1000, 3), "mA")

# 8. Rounding to the step of a sensor, and the error this causes
true_values = np.array([20.13, 20.38, 20.62, 20.87])
quantised = np.round(true_values / 0.25) * 0.25
print(quantised, np.round(np.abs(true_values - quantised).max(), 3))

# EXPECTED OUTPUT
# 8 22.84 21.15 [35.]
# [3. 4. 5. 6.] True
# True
# 1.989 0.14 0.9983
# [[0.659 0.242 0.099]
#  [0.109 0.802 0.089]] [1. 1.]
# 0.3185
# ['99.96%', '0.04%']
# [4.401 2.343 0.161 2.039 4.544]
# [22.727  9.091] mA
# [20.25 20.5  20.5  20.75] 0.12
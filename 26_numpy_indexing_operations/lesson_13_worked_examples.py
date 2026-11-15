import numpy as np

# WORKED EXAMPLES that combine the lessons of this module

# 1. Normalise the columns of sensor data with broadcasting (z-score)
readings = np.array([[20.0, 1000.0, 0.5], [22.0, 1010.0, 0.7], [21.0, 990.0, 0.6], [30.0, 1005.0, 0.4]])
mean = readings.mean(axis=0)
std = readings.std(axis=0)
z = (readings - mean) / std
print(np.round(z, 2))
print(np.round(z.mean(axis=0), 6) + 0.0, np.round(z.std(axis=0), 6))

# 2. Outliers: find them with a mask and replace them with the mean of the good values
temps = np.array([20.1, 20.3, 19.9, 35.0, 20.2, 20.0, -5.0, 20.4])
outlier = np.abs(temps - temps.mean()) > 1.5 * temps.std()
print(outlier)
clean = np.where(outlier, temps[~outlier].mean(), temps)
print(np.round(clean, 2))

# 3. Top-3 retrieval for RAG: the three best similarity scores, best first
scores = np.array([0.12, 0.91, 0.45, 0.88, 0.05, 0.67])
documents = np.array(["a", "b", "c", "d", "e", "f"])
k = 3
top = np.argpartition(scores, -k)[-k:]                   # the k best, unordered
top = top[np.argsort(scores[top])[::-1]]                 # ordered, best first
print(top, scores[top], documents[top])

# 4. Nearest neighbour with a distance table (broadcasting)
points = np.array([[0.0, 0.0], [1.0, 1.0], [5.0, 5.0], [1.0, 0.5]])
distance = np.sqrt(((points[:, None, :] - points[None, :, :]) ** 2).sum(axis=-1))
np.fill_diagonal(distance, np.inf)                       # a point is not its own neighbour
print(distance.argmin(axis=1))

# 5. A status register: which readings have an error flag and which are busy
status = np.array([0b0001, 0b0101, 0b1000, 0b1100], dtype=np.uint8)
ERROR, BUSY = 0b0100, 0b1000
print((status & ERROR).astype(bool), (status & BUSY) != 0, status[(status & ERROR) == 0])

# 6. A lookup table with searchsorted: ADC counts to categories
bounds = np.array([100, 500, 900])
labels = np.array(["low", "mid", "high", "max"])
adc = np.array([50, 100, 499, 500, 950])
print(labels[np.searchsorted(bounds, adc, side="right")])

# 7. Removing duplicate rows but keeping the order of first appearance
log = np.array([[1, 10], [2, 20], [1, 10], [3, 30], [2, 20]])
_, first_seen = np.unique(log, axis=0, return_index=True)
print(log[np.sort(first_seen)])

# 8. Counting the readings per category
categories = np.array([0, 2, 1, 2, 2, 0, 1, 2])
print(np.bincount(categories, minlength=4))

# EXPECTED OUTPUT
# [[-0.82 -0.17 -0.45]
#  [-0.32  1.18  1.34]
#  [-0.57 -1.52  0.45]
#  [ 1.7   0.51 -1.34]]
# [0. 0. 0.] [1. 1. 1.]
# [False False False  True False False  True False]
# [20.1  20.3  19.9  20.15 20.2  20.   20.15 20.4 ]
# [1 3 5] [0.91 0.88 0.67] ['b' 'd' 'f']
# [3 3 1 1]
# [False  True False  True] [False False  True  True] [1 8]
# ['low' 'mid' 'mid' 'high' 'max']
# [[ 1 10]
#  [ 2 20]
#  [ 3 30]]
# [2 2 4 0]
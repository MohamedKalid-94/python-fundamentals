import struct

import numpy as np

# WORKED EXAMPLES that combine the lessons of this module

# 1. A sensor frame: 4 channels x 3 samples of 16-bit ADC values, little endian
channels, samples = 4, 3
raw = struct.pack("<12H", 100, 110, 120, 200, 210, 220, 300, 310, 320, 400, 410, 420)
adc = np.frombuffer(raw, dtype="<u2").reshape(channels, samples)
print(adc.shape, adc.dtype)
volts = adc * (3.3 / 4095)                      # scale to volts: a whole-array operation
print(np.round(volts[:, 0], 4))
print(adc.mean(axis=1))                         # the mean of every channel
row, column = np.unravel_index(adc.argmax(), adc.shape)       # flat index -> (row, column)
print(adc.max(), adc.argmax(), int(row), int(column))

# 2. Splitting a long recording into windows of 4 samples
signal = np.arange(10)
windows = np.array_split(signal, [4, 8])
print([w.tolist() for w in windows])
usable = signal[: len(signal) // 4 * 4].reshape(-1, 4)
print(usable)

# 3. Embeddings and cosine similarity (the heart of RAG retrieval)
documents = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 1.0, 1.0]])
query = np.array([1.0, 0.0, 0.5])
normalised = documents / np.linalg.norm(documents, axis=1, keepdims=True)
unit_query = query / np.linalg.norm(query)
scores = normalised @ unit_query
print(np.round(scores, 3))
print("best document:", scores.argmax())

# 4. Stacking the results of several runs into one table
runs = [np.linspace(0, 1, 5) * k for k in (1, 2, 3)]
table = np.vstack(runs)
print(table.shape, table[:, -1])

# EXPECTED OUTPUT
# (4, 3) uint16
# [0.0806 0.1612 0.2418 0.3223]
# [110. 210. 310. 410.]
# 420 11 3 2
# [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]
# [[0 1 2 3]
#  [4 5 6 7]]
# [0.949 0.    0.775]
# best document: 0
# (3, 5) [1. 2. 3.]
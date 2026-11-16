import numpy as np

# RANDOM NUMBERS: use the Generator.
#   rng = np.random.default_rng(seed)      the modern interface (the PCG64 algorithm)
#   rng.random(size)                       floats in [0, 1)
#   rng.integers(low, high, size)          integers, HIGH EXCLUDED (endpoint=True includes it)
#   rng.choice(a, size, replace, p)        pick from a list, optionally with probabilities
#   rng.shuffle(a)                         shuffle IN PLACE         rng.permutation(a)   a shuffled COPY
#   rng.permuted(a, axis)                  shuffle independently along an axis
# The SAME SEED gives the SAME numbers: always pass a seed in tests and experiments (reproducibility).
# The exact numbers of a Generator may change between NumPy versions, so this lesson prints properties, not raw values.

rng = np.random.default_rng(42)
print(type(rng).__name__, type(rng.bit_generator).__name__)
first = np.random.default_rng(7).random(3)
second = np.random.default_rng(7).random(3)
print(np.array_equal(first, second))                       # same seed, same numbers
print(rng.random(3).shape, rng.random((2, 2)).shape)

x = rng.random(1000)
print(x.min() >= 0, x.max() < 1, 0.4 < x.mean() < 0.6)

dice = rng.integers(1, 7, size=600)                        # 1..6: the upper limit is excluded
print(dice.min() >= 1, dice.max() <= 6, set(dice.tolist()) == {1, 2, 3, 4, 5, 6})
print(rng.integers(0, 10, size=2000, endpoint=True).max() == 10)

# choice
print(rng.choice(["a", "b", "c"]) in ["a", "b", "c"])
no_repeat = rng.choice(10, size=4, replace=False)
print(len(no_repeat), len(set(no_repeat.tolist())))        # 4 different numbers
picks = rng.choice(["x", "y"], size=2000, p=[0.9, 0.1])    # probabilities
print((picks == "x").mean() > 0.85)

# shuffle (in place) and permutation (a copy)
data = np.arange(10)
copy = rng.permutation(data)
print(sorted(copy.tolist()) == data.tolist(), data.tolist())
rng.shuffle(data)
print(sorted(data.tolist()) == list(range(10)))

# 2-D: permutation shuffles the ROWS; permuted shuffles each row on its own
m = np.arange(12).reshape(3, 4)
rows = rng.permutation(m)
print(sorted(rows.sum(axis=1).tolist()) == sorted(m.sum(axis=1).tolist()))
inside = rng.permuted(m, axis=1)
print(np.array_equal(np.sort(inside, axis=1), m))

# A reproducible train/test split
samples = np.arange(100)
order = np.random.default_rng(0).permutation(len(samples))
train, test = samples[order[:80]], samples[order[80:]]
print(len(train), len(test), len(np.intersect1d(train, test)))

# Independent streams for parallel work, and saving the state
streams = [np.random.default_rng(s) for s in np.random.SeedSequence(123).spawn(3)]
print(len(streams), np.array_equal(streams[0].random(2), streams[1].random(2)))
state = rng.bit_generator.state
before = rng.random(2)
rng.bit_generator.state = state
print(np.array_equal(before, rng.random(2)))

# The LEGACY interface (old tutorials): its numbers are frozen forever
legacy = np.random.RandomState(0)
print(np.round(legacy.rand(3), 4))

# EXPECTED OUTPUT
# Generator PCG64
# True
# (3,) (2, 2)
# True True True
# True True True
# True
# True
# 4 4
# True
# True [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# True
# True
# True
# 80 20 0
# 3 False
# True
# [0.5488 0.7152 0.6028]
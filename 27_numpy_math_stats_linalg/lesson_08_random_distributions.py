import numpy as np

# DISTRIBUTIONS: every Generator method draws numbers from one:   rng.<name>(parameters, size)
#   name         parameters            mean               typical use
#   uniform      low, high             (low + high) / 2   equal chances: random delays, test data
#   normal       loc (mean), scale (sd) loc                measurement noise, errors
#   binomial     n, p                  n * p              successes in n tries (bit errors in a frame)
#   poisson      lam                   lam                events per interval (packets per second)
#   exponential  scale                 scale              waiting time between events
#   rayleigh     scale                 scale * sqrt(pi/2) magnitude of 2-D noise, signal fading
#   logistic     loc, scale            loc                S-curves, logistic regression
#   pareto       a                     1 / (a - 1)        heavy tails: file sizes (NumPy draws the "Lomax" form)
#   chisquare    df                    df                 variance tests, goodness of fit
#   zipf         a (above 1)           zeta(a-1)/zeta(a)  word frequencies: a few words are very common
#   multinomial  n, pvals              n * p for each class   counts over several classes
# size is a number or a shape tuple. The mean of a big sample is close to the theoretical mean.
# Plots of these distributions (Matplotlib and Seaborn) come in Module 28.
# Raw random values may change between NumPy versions, so this lesson prints checks, not the numbers.

rng = np.random.default_rng(2026)
N = 200_000
zeta3, zeta4 = 1.2020569031595942, np.pi ** 4 / 90
samples = {
    "uniform(2, 6)": (rng.uniform(2, 6, N), 4.0),
    "normal(5, 2)": (rng.normal(5, 2, N), 5.0),
    "binomial(10, 0.3)": (rng.binomial(10, 0.3, N), 3.0),
    "poisson(4)": (rng.poisson(4, N), 4.0),
    "exponential(2)": (rng.exponential(2.0, N), 2.0),
    "rayleigh(2)": (rng.rayleigh(2.0, N), 2.0 * np.sqrt(np.pi / 2)),
    "logistic(1, 0.5)": (rng.logistic(1.0, 0.5, N), 1.0),
    "pareto(3)": (rng.pareto(3.0, N), 0.5),
    "chisquare(4)": (rng.chisquare(4, N), 4.0),
    "zipf(4)": (rng.zipf(4.0, N), zeta3 / zeta4),
}
for name, (sample, expected) in samples.items():
    print(f"{name:<18} type {sample.dtype.kind}   mean close to theory: {abs(sample.mean() - expected) < 0.05}")

# Other properties
print(abs(samples["normal(5, 2)"][0].std() - 2) < 0.05)                          # the spread
uniform = samples["uniform(2, 6)"][0]
print(uniform.min() >= 2, uniform.max() < 6)
print(samples["binomial(10, 0.3)"][0].max() <= 10, samples["poisson(4)"][0].min() >= 0)
print(samples["exponential(2)"][0].min() > 0, samples["zipf(4)"][0].min() >= 1)

# Shapes
print(rng.normal(0, 1, size=(2, 3)).shape, rng.standard_normal(3).shape, rng.uniform(size=5).shape)

# Multinomial: counts over several classes (every row adds up to n)
counts = rng.multinomial(10, [0.2, 0.3, 0.5], size=5)
print(counts.shape, (counts.sum(axis=1) == 10).all())
share = rng.multinomial(1000, [0.2, 0.3, 0.5]) / 1000
print(np.allclose(share, [0.2, 0.3, 0.5], atol=0.08))

# Simulating a noisy sensor: a clean signal plus normal noise
t = np.linspace(0, 1, 100_000)
clean = np.sin(2 * np.pi * 5 * t)
noisy = clean + rng.normal(0, 0.1, size=clean.shape)
print(abs((noisy - clean).std() - 0.1) < 0.01)

# Poisson: how many packets arrive in each of 5 seconds at an average of 3 per second
packets = rng.poisson(3, size=5)
print(packets.shape, packets.dtype.kind, packets.min() >= 0)

# The data of a histogram (the plot comes in Module 28)
histogram, edges = np.histogram(samples["normal(5, 2)"][0], bins=10)
print(histogram.sum() == N, len(edges))

# EXPECTED OUTPUT
# uniform(2, 6)      type f   mean close to theory: True
# normal(5, 2)       type f   mean close to theory: True
# binomial(10, 0.3)  type i   mean close to theory: True
# poisson(4)         type i   mean close to theory: True
# exponential(2)     type f   mean close to theory: True
# rayleigh(2)        type f   mean close to theory: True
# logistic(1, 0.5)   type f   mean close to theory: True
# pareto(3)          type f   mean close to theory: True
# chisquare(4)       type f   mean close to theory: True
# zipf(4)            type i   mean close to theory: True
# True
# True True
# True True
# True True
# (2, 3) (3,) (5,)
# (5, 3) True
# True
# True
# (5,) i True
# True 11
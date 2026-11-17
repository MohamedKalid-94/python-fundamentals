from pathlib import Path

import matplotlib

matplotlib.use("Agg")                      # draw into files: no window opens (works on servers and in CI)
import matplotlib.pyplot as plt
import numpy as np

# MATPLOTLIB draws the arrays. The pattern:
#   fig, ax = plt.subplots(figsize=(6, 3))      a figure with one set of axes (rows, columns for several)
#   ax.plot / ax.scatter / ax.bar / ax.hist / ax.imshow      draw
#   ax.set(xlabel=..., ylabel=..., title=...)  ax.legend()  ax.grid(True)
#   fig.savefig("name.png", dpi=100)           write the picture;   plt.close(fig)   free the memory
# On your own computer replace the savefig line by plt.show() to see the window (remove matplotlib.use("Agg")).
# This lesson saves its pictures in the folder  plots/  next to this file (ignored by Git). Open them to look.
# It prints facts about the figures, not the pixels.

OUT = Path(__file__).parent / "plots"
OUT.mkdir(exist_ok=True)

# 1. A line plot with two curves
t = np.linspace(0, 1, 500, endpoint=False)
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(t, np.sin(2 * np.pi * 3 * t), label="3 Hz")
ax.plot(t, 0.5 * np.sin(2 * np.pi * 7 * t), "--", label="7 Hz")
ax.set(xlabel="time (s)", ylabel="amplitude", title="Two sine waves")
ax.legend()
ax.grid(True)
fig.savefig(OUT / "sines.png", dpi=100)
print(fig.get_size_inches().tolist(), len(ax.lines), ax.get_title(), ax.get_xlabel(), ax.get_legend() is not None)
plt.close(fig)

# 2. A scatter plot and a bar chart side by side
rng = np.random.default_rng(3)
x = rng.uniform(0, 10, 100)
y = 2 * x + rng.normal(0, 1.5, 100)
fig, (left, right) = plt.subplots(1, 2, figsize=(8, 3))
left.scatter(x, y, s=10)
slope, intercept = np.polyfit(x, y, 1)
left.plot([0, 10], [intercept, intercept + 10 * slope], color="red")
right.bar(["a", "b", "c"], [3, 5, 2])
fig.tight_layout()
fig.savefig(OUT / "scatter_bar.png", dpi=100)
print(len(left.collections), len(right.patches), abs(slope - 2) < 0.3)
plt.close(fig)

# 3. A HISTOGRAM: the same counts as np.histogram, drawn as bars
data = rng.normal(50, 10, 5000)
fig, ax = plt.subplots(figsize=(6, 3))
counts, edges, bars = ax.hist(data, bins=20, color="steelblue", edgecolor="white")
ax.set(xlabel="value", ylabel="count", title="Histogram of 5000 values")
fig.savefig(OUT / "histogram.png", dpi=100)
numpy_counts, numpy_edges = np.histogram(data, bins=20)
print(np.array_equal(counts, numpy_counts), np.allclose(edges, numpy_edges), len(bars), int(counts.sum()))
plt.close(fig)

# A density histogram: the AREA of all the bars is 1
fig, ax = plt.subplots()
density, edges, _ = ax.hist(data, bins=20, density=True)
print(round(float((density * np.diff(edges)).sum()), 6))
plt.close(fig)

# 4. A picture of a 2-D array (a heat map) and a spectrum
grid = np.add.outer(np.arange(20), np.arange(30)) % 7
fs, n = 1000, 1000
tt = np.arange(n) / fs
sig = np.sin(2 * np.pi * 50 * tt) + 0.5 * np.sin(2 * np.pi * 120 * tt)
freqs = np.fft.rfftfreq(n, 1 / fs)
amp = 2 * np.abs(np.fft.rfft(sig)) / n
fig, (top, bottom) = plt.subplots(2, 1, figsize=(6, 5))
image = top.imshow(grid, cmap="viridis", aspect="auto")
fig.colorbar(image, ax=top)
bottom.plot(freqs, amp)
bottom.set(xlim=(0, 200), xlabel="frequency (Hz)", ylabel="amplitude", title="Spectrum")
fig.tight_layout()
fig.savefig(OUT / "heatmap_spectrum.png", dpi=100)
print(grid.shape, tuple(float(v) for v in bottom.get_xlim()), float(freqs[np.argmax(amp)]))
plt.close(fig)

# 5. Many axes at once: a 2 x 2 grid of the first four distributions
fig, axes = plt.subplots(2, 2, figsize=(7, 5))
samples = {"normal": rng.normal(0, 1, 2000), "uniform": rng.uniform(0, 1, 2000),
           "exponential": rng.exponential(1.0, 2000), "poisson": rng.poisson(4, 2000)}
for ax, (name, values) in zip(axes.ravel(), samples.items()):
    ax.hist(values, bins=25)
    ax.set_title(name)
fig.tight_layout()
fig.savefig(OUT / "distributions.png", dpi=100)
print(axes.shape, [ax.get_title() for ax in axes.ravel()])
plt.close(fig)

# 6. The files exist
for name in ["sines", "scatter_bar", "histogram", "heatmap_spectrum", "distributions"]:
    print(f"{name}.png", (OUT / f"{name}.png").stat().st_size > 2000)

# EXPECTED OUTPUT
# [6.0, 3.0] 2 Two sine waves time (s) True
# 1 3 True
# True True 20 5000
# 1.0
# (20, 30) (0.0, 200.0) 50.0
# (2, 2) ['normal', 'uniform', 'exponential', 'poisson']
# sines.png True
# scatter_bar.png True
# histogram.png True
# heatmap_spectrum.png True
# distributions.png True
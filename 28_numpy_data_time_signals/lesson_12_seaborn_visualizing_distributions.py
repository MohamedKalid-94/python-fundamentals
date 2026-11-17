import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# SEABORN draws statistical plots on top of Matplotlib, with good-looking defaults.
#   sns.set_theme(style="whitegrid")
#   sns.histplot(data, bins=, kde=True)       histogram, optionally with a smooth density curve
#   sns.kdeplot(data, fill=True)              the smooth density alone
#   sns.ecdfplot(data)                        the cumulative distribution: the share of values below x
#   sns.boxplot / sns.violinplot(data=...)    compare groups: median, quartiles, outliers
#   sns.displot(data, col=...)                several panels at once (it returns a FacetGrid)
#   sns.rugplot(data)                         a tick for every value
# Seaborn needs pandas (Modules 29 to 31). Install:  pip install seaborn matplotlib
# Pictures go to the folder plots/ (ignored by Git). The lines below print facts about the figures.

OUT = Path(__file__).parent / "plots"
OUT.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid")

rng = np.random.default_rng(11)
normal = rng.normal(5, 2, 1000)

# 1. A histogram with a density curve
fig, ax = plt.subplots(figsize=(6, 3))
sns.histplot(normal, bins=20, kde=True, ax=ax)
ax.set(title="Normal(5, 2)")
fig.savefig(OUT / "sns_hist.png", dpi=100)
print(len(ax.patches), len(ax.lines), ax.get_title())
plt.close(fig)

# 2. Several distributions on top of each other (the lesson 08 list)
fig, ax = plt.subplots(figsize=(7, 3))
sns.kdeplot(rng.normal(0, 1, 2000), label="normal", ax=ax)
sns.kdeplot(rng.exponential(1.0, 2000), label="exponential", ax=ax)
sns.kdeplot(rng.rayleigh(1.0, 2000), label="rayleigh", ax=ax)
ax.legend()
fig.savefig(OUT / "sns_kde.png", dpi=100)
print(len(ax.lines), [text.get_text() for text in ax.get_legend().get_texts()])
plt.close(fig)

# 3. The cumulative distribution and a rug of the values
fig, ax = plt.subplots(figsize=(6, 3))
sns.ecdfplot(normal, ax=ax)
sns.rugplot(normal[:50], ax=ax)
ax.set(ylabel="share of values below x")
fig.savefig(OUT / "sns_ecdf.png", dpi=100)
line = ax.lines[0]
print(float(line.get_ydata().max()), float(line.get_ydata()[len(line.get_ydata()) // 2]) > 0.4)
plt.close(fig)

# 4. Comparing groups with a box plot and a violin plot (a dictionary of arrays)
groups = {"sensor A": rng.normal(20, 1, 300), "sensor B": rng.normal(22, 2, 300), "sensor C": rng.normal(21, 0.5, 300)}
fig, (left, right) = plt.subplots(1, 2, figsize=(9, 3))
with warnings.catch_warnings():
    # seaborn 0.13.2 still passes an option that Matplotlib 3.11 has deprecated: the warning is harmless
    warnings.simplefilter("ignore", matplotlib.MatplotlibDeprecationWarning)
    sns.boxplot(data=groups, ax=left)
    sns.violinplot(data=groups, ax=right)
fig.tight_layout()
fig.savefig(OUT / "sns_groups.png", dpi=100)
print([label.get_text() for label in left.get_xticklabels()])
plt.close(fig)

# 5. displot: panels side by side
samples = {"poisson": rng.poisson(4, 1500), "binomial": rng.binomial(10, 0.3, 1500)}
fig, axes = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
for ax, (name, values) in zip(axes, samples.items()):
    sns.histplot(values, discrete=True, ax=ax)
    ax.set_title(name)
fig.savefig(OUT / "sns_discrete.png", dpi=100)
print([ax.get_title() for ax in axes])
plt.close(fig)

grid = sns.displot(normal, kde=True, height=3, aspect=1.5)
grid.savefig(OUT / "sns_displot.png", dpi=100)
print(type(grid).__name__, type(grid.figure).__name__)
plt.close(grid.figure)

for path in sorted(OUT.glob("sns_*.png")):
    print(path.name, path.stat().st_size > 2000)

# EXPECTED OUTPUT
# 20 1 Normal(5, 2)
# 3 ['normal', 'exponential', 'rayleigh']
# 1.0 True
# ['sensor A', 'sensor B', 'sensor C']
# ['poisson', 'binomial']
# FacetGrid Figure
# sns_discrete.png True
# sns_displot.png True
# sns_ecdf.png True
# sns_groups.png True
# sns_hist.png True
# sns_kde.png True
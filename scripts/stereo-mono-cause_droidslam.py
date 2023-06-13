import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Your matrix

cause = [
    [27,	4,	9,	9,	11,	2,	8],
    [2,	2,	0,	0,	2,	1,	0]
]
cause = np.array(cause)

total_runs = [
    [43,	28],
    [12,	9],
    [12,	8],
    [15,	0],
    [21,	19],
    [3,	3],
    [12,	12]
]

total_runs = np.array(total_runs).T
A = cause * 100 / total_runs
A[(A == np.inf) | (np.isnan(A))] = -1

# Create annotations: "-" where A == np.inf or np.isnan(A), otherwise the value from A
annotations = np.where(A < 0, "X", np.round(A, 1))

# Convert the numpy array to a DataFrame for easier visualization
df = pd.DataFrame(A, index=["Monocular", "Stereo"], 
                  columns=["Jerky motion", "Reflections", "Bright light / Lens flare", "Dynamic elements", "Repetitive patterns", "Similar scenes", "Self-shadows"])

# Convert the annotations to a DataFrame for seaborn
annot_df = pd.DataFrame(annotations, index=df.index, columns=df.columns)

FIGSIZE = (8, 3)
FONTSIZE = 8
ANNOTSIZE = 9.5

plt.figure(figsize=FIGSIZE)

# Create the heatmap with grayscale
# ax = sns.heatmap(df, annot=True, cmap='binary', linewidths=0, cbar=True, vmin=0, vmax=100, annot_kws={"size": ANNOTSIZE})
ax = sns.heatmap(df, annot=annot_df, fmt="", cmap='binary', linewidths=0, cbar=True, vmin=0, vmax=100, annot_kws={"size": ANNOTSIZE})

# Clear current x-labels
ax.set_xticklabels(['']*df.shape[1])

# Set y-labels
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, horizontalalignment='right', fontsize=FONTSIZE)

# Move the x-axis to the top and center the ticks
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')
ax.set_xticks([x - 0.5 for x in range(1, len(df.columns) + 1)], minor=False)

# Manually set x-labels
for i, column in enumerate(df.columns):
    ax.text(i+0.4, -0.3, column, rotation=45, fontsize=FONTSIZE, ha='left')

plt.tight_layout()
plt.show()

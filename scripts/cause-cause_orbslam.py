import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Your matrix
cause_cause = [
    [106,	10,	12,	22,	35,	0,	2],
    [10,	24,	0,	0,	19,	8,	0],
    [12,	0,	12,	2,	0,	0,	0],
    [22,	0,	2,	35,	0,	0,	0],
    [35,	19,	0,	0,	55,	10,	0],
    [0,	8,	0,	0,	10,	13,	0],
    [2,	0,	0,	0,	0,	0,	7]
]
cause_cause = np.array(cause_cause)
A = cause_cause * 100 / 139

# Create annotations: "-" where A == np.inf or np.isnan(A), otherwise the value from A
annotations = np.where(A < 0, "X", np.round(A, 1))

# Convert the numpy array to a DataFrame for easier visualization
df = pd.DataFrame(A, index=["Jerky motion", "Reflections", "Bright light / Lens flare", "Dynamic elements", "Repetitive patterns", "Similar scenes", "Self-shadows"], 
                  columns=["Jerky motion", "Reflections", "Bright light / Lens flare", "Dynamic elements", "Repetitive patterns", "Similar scenes", "Self-shadows"])

# Convert the annotations to a DataFrame for seaborn
annot_df = pd.DataFrame(annotations, index=df.index, columns=df.columns)

FIGSIZE = (8, 3)
FONTSIZE = 8
ANNOTSIZE = 9.5

# FIGSIZE = (16, 6)
# FONTSIZE = 12
# ANNOTSIZE = 10

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
    ax.text(i+0.4, -0.5, column, rotation=45, fontsize=FONTSIZE, ha='left')

plt.tight_layout()
plt.show()

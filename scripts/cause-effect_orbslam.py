import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Your matrix
cause_effect = [
    [0,	5,	0,	0,	5,	5,	0],
    [102,	10,	12,	31,	38,	0,	2],
    [4,	5,	0,	4,	8,	5,	5],
    [0,	4,	0,	0,	4,	3,	0]
]
cause_effect = np.array(cause_effect)

total_runs_causes = [
    246,
    41,
    58,
    48,
    99,
    13,
    38
]
total_runs_causes = np.array(total_runs_causes).reshape(1, -1)
A = cause_effect * 100 / total_runs_causes
A[(A == np.inf) | (np.isnan(A))] = -1

# Create annotations: "-" where A == np.inf or np.isnan(A), otherwise the value from A
annotations = np.where(A < 0, "X", np.round(A, 1))

# Convert the numpy array to a DataFrame for easier visualization
df = pd.DataFrame(A, index=["False positive loop closure", "Lost localization", "Inconsistent translation scale", "Incorrect topology"], 
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
    ax.text(i+0.4, -0.5, column, rotation=45, fontsize=FONTSIZE, ha='left')

plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt

orbslam = [
    38.23529412,
    45.20547945,
    64.70588235
]
A = np.array(orbslam)

droidslam = [
    31.25,
    38.70967742,
    37.83783784
]
B = np.array(droidslam)

x_labels = ["1", "2", "3 or more"]

x = np.arange(len(x_labels))  # the label locations
width = 0.3  # the width of the bars

fig, ax = plt.subplots()

# Improved colors with alpha transparency
rects1 = ax.bar(x - width/2, A, width, label='ORBSLAM', color='steelblue', alpha=0.7)
rects2 = ax.bar(x + width/2, B, width, label='DROIDSLAM', color='darkorange', alpha=0.7)

# Add some text for labels and custom x-axis tick labels, etc.
ax.set_xlabel('Number of challenging factors present')
ax.set_ylabel('Failure percentage')
ax.set_xticks(x)
ax.set_xticklabels(x_labels)
ax.legend()

ax.set_ylim([0, 100])  # y axis should go from 0.0 to 1.0

# Improved aesthetics: grid and spines
ax.grid(True, color='grey', linestyle='--', linewidth=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig.tight_layout()
plt.show()

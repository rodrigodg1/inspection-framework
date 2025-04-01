import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_style('darkgrid')

# 1,963,200 bytes for a 4 robot 20 minute simulation
# 24,540 bytes for 1 robot per minute

time_intervals = np.linspace(0, 600, 100) # 100 points between 0 and 600 minutes

size_per_minute = 24540 # in bytes
size_intervals_bytes = size_per_minute * time_intervals # Total size in bytes for 1 robot

# Convert the size to megabytes (1 MB = 1,048,576 bytes)
size_intervals_mb = size_intervals_bytes / 1048576 # Size in megabytes

plt.rcParams.update({'font.size': 14})

# Plotting the graph
plt.plot(time_intervals / 60, size_intervals_mb, label="Memory Size", linestyle='-', marker='o')

# Adding labels and title
plt.xlabel('Time (hours)')
plt.ylabel('Memory Size (MB)')

# Show grid and plot
plt.grid(True)
plt.legend()
plt.savefig('size-series.png', dpi=300)
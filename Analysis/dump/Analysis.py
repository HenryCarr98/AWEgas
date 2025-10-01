import sys
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd

"""
Section 1: Strong scaling
"""

# Plot of system for 100k cells


# Read CSV file into DataFrame
file="../plotdata/100kcells.csv"
df = pd.read_csv(file, header=None, names=["x", "Density"])

# Plot directly from DataFrame
df.plot(x="x", y="Density", legend=False)

plt.xlabel("x")
plt.ylabel("Density")
plt.savefig("img/plot100kcells.png", dpi=375)


# Thread count vs execution tims 

# Relative Speedup and efficiency 

# Fit of Amdahl's law (not using least-squares)


"""
Section 2: Weak scaling
"""

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("../var_thread/varthreads_100000_cells.csv")

# Assuming the CSV has columns named 'Threads' and 'ExecutionTime' (adjust accordingly)
xs = df['threads']
ys = df['execution_time_sec']

# Plotting
# plt.figure(figsize=(6,4))
# plt.plot(xs, ys, marker="+", linestyle="-", color="k")
# Plotting with custom marker color (e.g., 'red') and linestyle
plt.figure(figsize=(6,4))
plt.plot(xs, ys, marker="+", linestyle="-", color="red",markeredgecolor="k")  # Red color for markers

# Set axis limits (for example, x-axis between 0 and 20, y-axis between 0 and 100)
plt.xlim(0, 34)  # Change as needed
plt.ylim(40, 180)  # Change as needed

plt.xlabel("Threads")
plt.ylabel("Execution Time (s)")
plt.title("Execution Time vs Threads for fixed (100,000) cells")
plt.grid(True)

# Save plot
plt.savefig("../img/plot_threads.pdf")
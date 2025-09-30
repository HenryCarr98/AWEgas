#%%


import sys
import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("varthreads_100000_cells.csv")

# Assuming the CSV has columns named 'Threads' and 'ExecutionTime' (adjust accordingly)
xs = df['threads']
ys = df['execution_time_sec']

# Plotting
# plt.figure(figsize=(6,4))
# plt.plot(xs, ys, marker="+", linestyle="-", color="k")
# Plotting with custom marker color (e.g., 'red') and linestyle
plt.figure(figsize=(6,4))
plt.plot(xs, ys, marker="x", linestyle="-", color="red")  # Red color for markers

# Set axis limits (for example, x-axis between 0 and 20, y-axis between 0 and 100)
plt.xlim(0, 34)  # Change as needed
plt.ylim(40, 180)  # Change as needed

plt.xlabel("Threads")
plt.ylabel("Execution Time (s)")
plt.title("Execution Time vs Threads for fixed (100,000) cells")
plt.grid(True)

# Save plot
plt.savefig("../img/plot_threads.pdf")




# %%
# Estimate the sequential fraction 'f' manually.
# We assume the execution time approaches the sequential time as the number of threads increases.
# Find the maximum execution time (assumed to be close to the sequential time)
execution_time = df['execution_time_sec']
threads = df['threads']
time_seq = execution_time.max()


# Extract times
T1 = df[df['threads'] == 1]['execution_time_sec'].values[0]     # T(1)
TN = df[df['threads'] == 32]['execution_time_sec'].values[0]    # T(32)
N = 32 #max number of threads

# Estimate f using the rearranged Amdahl's Law formula
f = (N * (1 - (TN / T1))) / (N - 1)



# f = 0.7034 # You can change this based on your observation.

# Amdahl's Law calculation
def amdahls_law(N, f):
    return time_seq * ((1 - f) + (f / N))

# Calculate the theoretical execution time from Amdahl's law
theoretical_time = amdahls_law(threads, f)

# Plot the original data
plt.figure(figsize=(6,4))
plt.plot(threads, execution_time, marker="o", linestyle="-", color="blue", label="Measured Time")

# Plot the Amdahl's Law curve
plt.plot(threads, theoretical_time, linestyle="--", color="red", label="Amdahl's Law")

# Labeling axes and title
plt.xlabel("Threads")
plt.ylabel("Execution Time (s)")
plt.title("Execution Time vs Threads with Amdahl's Law")
plt.grid(True)

# Add a legend
plt.legend()


# Save plot
plt.savefig("../img/plot_threads_fitted.pdf")


#%%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("varthreads_100000_cells.csv")

# Extract data
N = df["threads"].values           # Number of threads
T = df["execution_time_sec"].values
T1 = T[0]                          # Execution time at 1 thread

# Linearize Amdahl's Law
x = 1 / N                          # 1/N
y = T / T1                         # T(N)/T(1)

# Linear regression: y = a + b*x
A = np.vstack([np.ones_like(x), x]).T
coeffs = np.linalg.lstsq(A, y, rcond=None)[0]  # [a, b]

a, b = coeffs
f = b / (a + b)

print(f"Estimated sequential fraction f: {f:.4f}")

# Now use Amdahl's Law to compute theoretical T(N)
def amdahl_time(T1, f, N):
    return T1 * ((1 - f) + f / N)

amdahl_times = amdahl_time(T1, f, N)

# Plotting
plt.figure(figsize=(6,4))
plt.plot(N, T, marker="o", label="Measured", color="blue")
plt.plot(N, amdahl_times, marker="x", linestyle="--", label="Amdahl's Law (f={:.2f})".format(f), color="red")

plt.xlabel("Threads")
plt.ylabel("Execution Time (s)")
plt.title("Execution Time vs Threads with Amdahl's Law Fit")
plt.grid(True)
plt.legend()
# %%

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
# Base directory = directory where this script lives
BASE_DIR = Path(__file__).resolve().parent.parent

# Paths relative to script
"""
Plots a single realisation of the code 
"""
#%%
data_file = BASE_DIR / "realisations" / "100kcells.csv"
out_file = BASE_DIR / "img" / "plot100kcells.png"

# Read CSV file into DataFrame
df = pd.read_csv(data_file, header=None, names=["x", "Density"])
# Access as Series
x = df["x"]
y = df["Density"]


# Plot
plt.plot(x, y, linestyle="-", color="red")  # Red color for markers

plt.xlabel("x")
plt.ylabel("Density")
plt.title("Sod shock-tube for 100,000 cells")
plt.grid()
plt.show()
# plt.savefig(out_file, dpi=375)

#%%
"""
Plots threads vs execution time 
"""

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("../var_thread/varthreads_100000_cells.csv")

data_file = BASE_DIR / "var_thread" / "varthreads_100000_cells.csv"
out_file = BASE_DIR / "img" / "plot100kcellsvarthreads.png"



# Assuming the CSV has columns named 'Threads' and 'ExecutionTime' (adjust accordingly)
xs = df['threads']
ys = df['execution_time_sec']

plt.plot(xs, ys, marker="+", linestyle="-", color="red",markeredgecolor="k")  # Red color for markers

# Set axis limits 
plt.xlim(0, 34)  # Change as needed
plt.ylim(40, 180)  # Change as needed

plt.xlabel("Threads")
plt.ylabel("Execution Time (s)")
plt.title("Execution Time vs Threads for 100,000 cells")
plt.grid(True)

# Save plot
# plt.savefig(out_file, dpi=375)

#%%
"""
Plots threads vs execution time 
"""
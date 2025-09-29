import subprocess
import csv
import os
import time
import matplotlib.pyplot as plt

# Configuration
executable = "./gas"    # path to your compiled program
num_cells = 100000      # cells
max_threads = 28
csv_file = "var_thread/varthreads.csv"

threads_list = []
times_list = []

with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["threads", "execution_time_sec"])

    for threads in range(1, max_threads + 1):
        print(f"Running with {threads} threads...")

        # Set OpenMP thread count
        env = os.environ.copy()
        env["OMP_NUM_THREADS"] = str(threads)

        # Use perf_counter for high-resolution timing
        start = time.perf_counter()
        subprocess.run([executable, str(num_cells)], env=env)
        end = time.perf_counter()

        elapsed = end - start

        writer.writerow([threads, elapsed])
        threads_list.append(threads)
        times_list.append(elapsed)

        print(f"{threads} threads -> {elapsed:.6f} sec")

print(f"CSV saved to {csv_file}")

# # --- Plotting ---
# plt.figure(figsize=(8,5))
# plt.plot(threads_list, times_list, marker='o', linestyle='-')
# plt.xlabel("Number of threads")
# plt.ylabel("Execution time (seconds)")
# plt.title(f"Performance scaling for {num_cells} cells")
# plt.xticks(range(1, max_threads + 1))
# plt.grid(True)
# plt.tight_layout()
# plt.savefig("performance_plot.png")
# plt.show()

import subprocess
import csv
import os
import time

# Configuration
executable = "./gas"    # path to your compiled program
num_cells = 125000      # cells
max_threads = 32

# Dynamic CSV filename based on number of cells
csv_file = f"var_thread/varthreads_{num_cells}_cells.csv"

threads_list = []
times_list = []

with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["threads", "execution_time_sec"])
    f.flush()

    for threads in range(1, max_threads + 1):
        print(f"Running with {threads} threads...")

        # Set OpenMP thread count
        env = os.environ.copy()
        env["OMP_NUM_THREADS"] = str(threads)

        # # High-resolution timer
        # start = time.perf_counter()
        # subprocess.run([executable, str(num_cells)], env=env)
        # end = time.perf_counter()
        # elapsed = end - start

        start = time.perf_counter()
        with open(os.devnull, 'w') as fnull:
            subprocess.run([executable, str(num_cells)], env=env, stdout=fnull, stderr=fnull)
        end = time.perf_counter()

        elapsed = end - start
        print(elapsed)

        writer.writerow([threads, elapsed])
        f.flush()  # ensure immediate write

        threads_list.append(threads)
        times_list.append(elapsed)

        print(f"{threads} threads -> {elapsed:.6f} sec")

print(f"CSV saved to {csv_file}")
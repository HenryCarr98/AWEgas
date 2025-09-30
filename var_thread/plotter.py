import sys
import matplotlib.pyplot as plt
import csv

xs = []
ys = []

with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        threads = int(row[0])
        time_sec = float(row[1])
        xs.append(threads)
        ys.append(time_sec)

plt.figure(figsize=(6,4))
plt.plot(xs, ys, marker="o", linestyle="-", color="b")

plt.xlabel("Threads")
plt.ylabel("Execution Time (s)")
plt.title("Execution Time vs Threads for fixed cells")
plt.grid(True)

# Save plot
plt.savefig("../img/plot_threads.pdf")

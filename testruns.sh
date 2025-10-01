
#!/bin/bash
EXEC=./gas
CELLS=50000   # fixed cell count
OUTFILE=var_thread/benchmark_threads_$CELLS.csv

# Write header
echo "threads,time_seconds" > "$OUTFILE"

# Vary thread count from 1 to 12
for THREADS in $(seq 1 1 14); do
    echo "Running CELLS=$CELLS with THREADS=$THREADS"
    export OMP_NUM_THREADS=$THREADS

    start=$(date +%s.%N)
    $EXEC $CELLS > /dev/null
    end=$(date +%s.%N)

    elapsed=$(echo "$end - $start" | bc -l)

    echo "$THREADS,$elapsed" >> "$OUTFILE"
done

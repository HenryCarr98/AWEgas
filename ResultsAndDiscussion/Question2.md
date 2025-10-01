- [Testing and optimising the performance of the numerical scheme](#testing-and-optimising-the-performance-of-the-numerical-scheme)
  - [Scaling analysis](#scaling-analysis)
- [Determining efficiency of the code](#determining-efficiency-of-the-code)

# Testing and optimising the performance of the numerical scheme

Now that we are satisfied the code has been suitably parallelised, the task now is to examine its performance as 

- [ ] Cell count remains fixed and thread count is varied (strong scaling)
- [ ] Cell count is varied and thread count is fixed (at the maximum determined by the strong scaling) also known as "weak scaling"

From this, we can then make estimates of the efficiency, speedup and much more. 

## Scaling analysis

One (if not the most) critical aspect of our work involved the determination of the point at which the performance of the code either plateaus or begins to decrease with respect to the number of processor threads allocated to the task. To do this, the code was compiled with the `-fopenmp` flag it was decided to test it with the following parameters 

1. Fixed cell count of `100,000`
2. Varied thread count from `1` to `32`

There are many ways to measure the time of execution however for the sake of simplicity, we elected to delegate this task to a Python script (please cf. with `benchmark_threads.py` and `benchmark_cells.py`) which made use of the `subprocess` library to handle the execution. This script adopted the following workflow 

1. Define the path to the executable and output files
2. Initialise the parameters 
3. Set OpenMP environment variable:
   ```python
   env = os.environ.copy()
   env["OMP_NUM_THREADS"] = str(threads)
   ```
4. Run the executable using subprocess.run while suppressing stdout/stderr:
   ```python
   with open(os.devnull, 'w') as fnull:
      subprocess.run([executable, str(num_cells)], env=env, stdout=fnull, stderr=fnull)
   ```
5. Measure wallclock execution time
6. Write to csv.

# Determining efficiency of the code

The easiest and most logical method available to us is to simply run the code for an array of different thread counts whilst keeping the number of cells fixed (`100,000` to be precise). From this, one can readily plot execution time as a function of the number of threads as below:

<p align="center">
<img src="img/plot100kcellsvarthreads.png" alt="drawing" style="width:640px;centered"/>
<center>Fig. 1: thread count vs execution time. </center>


We can readily see that performance (excluding some fluctuations in the order of 5-8s) steadily (exponentially) decreases until reaching an almost plateau-like stablility at 15 threads (where the execution time dips below 60 seconds). We can therefore make the straightforward observation that past 15 threads, one does **not** see an increase in performance- this is therefore our **scaling limit**. 

One leading cause of this is due to the fact that some of the code can only be executed in serial (we shall estimate this fraction later)- therefore adding more threads will not offer any benefit. One also has to account for the fact that, in terms of computing, this is a relatively small problem and the delays caused by communication overheads between e.g., nodes or the Lustre file system quickly diminish any gains offered by increasing the thread count. 

<p align="center">
<img src="../img/plot100kcellsefficiency.png" alt="drawing" style="width:640px;centered"/>
<center>Fig. 1: thread count vs execution time. </center>


<!-- # Performance Analysis Plan for Sod Shock Tube Solver

>[!important]
> Keep within the bounds of the objective
> > *Explore performance with varying thread counts and varying problem sizes (within the bounds of compute available to you, if that is only e.g. two or four CPU cores that is not a problem).*


## Objective

To quantify the impact of OpenMP parallelisation on the solver’s performance, verify correctness of parallel implementation, and assess numerical stability with respect to timestep control.



## Step 1: Serial vs Parallel Execution (50k cells)

**Purpose:** Verify correctness of parallelisation and quantify speed-up.

**Procedure:**

1. Set up two runs with `nel = 50,000` cells:

   * **Serial run:** Compile without `-fopenmp` or set `OMP_NUM_THREADS=1`.
   * **Parallel run:** Compile with OpenMP (`-fopenmp`) and set `OMP_NUM_THREADS=8`.
2. Record wall-clock runtime using `omp_get_wtime()` or Python wrapper.
3. Output cell density profiles from both runs.
4. **Compare solutions:** Plot density vs position (`x`) to ensure parallelisation did not alter results.

**Expected outcome:**

* Parallel run should be faster (ideally ~4–6× speed-up on 8 threads).
* Density profiles must be numerically identical within floating-point tolerance.



## Step 2: Scaling and Stability Study

**Purpose:** Measure performance scaling with thread count and observe timestep behaviour.

**Procedure:**

1. Select a fixed problem size (e.g., 50k cells).
2. Run simulations with different thread counts: `1, 2, 4, 8, 16`.
3. Record:

   * Wall-clock execution time
   * Minimum CFL timestep (`min_cfl`) per run
   * Thread count used
4. **Analysis:**

   * Plot execution time vs thread count (strong scaling)
   * Observe how timestep adapts with different parallel configurations
   * complexity? 

**Expected outcome:**

* Near-linear scaling for the most parallelisable loops.
* Serial sections (corrector step) will limit speed-up at higher threads.
* CFL-adapted timestep will remain stable across parallel runs.



## Step 3: Performance vs Numerical Stability

**Purpose:** Demonstrate that parallelisation does not compromise solver stability.

**Procedure:**

1. Monitor timestep (`dt`) evolution during the simulation.
2. Ensure that the CFL condition is respected throughout.
3. Cross-check with serial run: timestep values should be comparable.

**Expected outcome:**

* Parallelisation accelerates computation without affecting timestep selection or numerical correctness.
* No CFL violations or instabilities should occur.



## Step 4: Deliverables

1. CSV file logging:

   * Thread count
   * Execution time (is `time.perf_counter()` correct?)
   * Explain workflow
2. Plots:

   * Density profile comparison (Serial vs Parallel)
   * Execution time vs thread count (scaling curve)
   * Optional: timestep evolution vs simulation time
   * Amdahl’s Law over the top I think? $Speedup = t_1/t_{cpumax}$
     * Linear regression? 


15 threads 

cell count:

100
500
750
1000
2000
5000
10000
25000
50000
75000
100000
125000

try to test weak scaling
 -->

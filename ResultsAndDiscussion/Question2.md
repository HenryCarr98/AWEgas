- [Performance Analysis Plan for Sod Shock Tube Solver](#performance-analysis-plan-for-sod-shock-tube-solver)
  - [Objective](#objective)
  - [Step 1: Serial vs Parallel Execution (50k cells)](#step-1-serial-vs-parallel-execution-50k-cells)
  - [Step 2: Scaling and Stability Study](#step-2-scaling-and-stability-study)
  - [Step 3: Performance vs Numerical Stability](#step-3-performance-vs-numerical-stability)
  - [Step 4: Deliverables](#step-4-deliverables)


# Performance Analysis Plan for Sod Shock Tube Solver

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
   * Minimum CFL timestep
2. Plots:

   * Density profile comparison (Serial vs Parallel)
   * Execution time vs thread count (scaling curve)
   * Optional: timestep evolution vs simulation time
   * Amdahl’s Law over the top I think? $Speedup = t_1/t_{cpumax}$



- [Refining a 1-D solver](#refining-a-1-d-solver)
  - [Overview of the Code](#overview-of-the-code)
  - [What's "wrong" with it and why do we want to change it?](#whats-wrong-with-it-and-why-do-we-want-to-change-it)
- [Implementing my changes](#implementing-my-changes)
  - [Parallelisation](#parallelisation)
    - [Why were some loops were left serial?](#why-were-some-loops-were-left-serial)
    - [Why did we use `#pragma omp parallel for reduction(min:min_cfl)`?](#why-did-we-use-pragma-omp-parallel-for-reductionminmin_cfl)
- [Summary](#summary)



# Refining a 1-D solver

Disclaimer: this document gives a brief overview of the changes made to the algorithm. For my results and discussion, please look at the file named `Question2.md`.

## Overview of the Code

> This program is a 1D finite-element solver for the compressible Euler equations. It models shock propagation using Sod’s shock tube initial conditions. The solver sets up a 1D mesh, computes nodal and cell-centered quantities (positions, velocities, densities, pressures, and energies), and advances the solution in time using an explicit predictor–corrector scheme. OpenMP is used to parallelise loops over cells and nodes, and the program outputs density data to a file for post-processing.


## What's "wrong" with it and why do we want to change it? 

3 main areas: 

1. Lack of Parallelisation. All loops over nodes and cells were executed sequentially.  
   1. Problem: For large meshes (e.g., 100k cells), this led to unnecessarily long runtimes on modern multi-core CPUs. Why it mattered: Computational loops like initialisation, time-stepping, and CFL calculations are embarrassingly parallel. Not exploiting this wastes available hardware resources.

1. Unsafe or Inefficient Output. Density output was printed directly to stdout. 
   1. Problem: For large meshes, this clutters the console and slows execution due to I/O bottlenecks. Why it mattered: Simulation output should be reproducible, structured, and separated from the console to allow automated post-processing and plotting.

1. Rigid Threading and Performance Testing. The code had no way to vary the number of threads. 
   1. Problem: Users could not easily benchmark or optimise performance on different hardware. Why it mattered: Without benchmarking, you cannot understand scaling behavior, identify bottlenecks, or choose the optimal thread count.

# Implementing my changes

## Parallelisation

I systematically analysed all loops over cells and nodes to identify those that were independent and safe to parallelise. 

For loops where each iteration wrote to distinct array elements, we applied `#pragma omp` parallel for to execute iterations concurrently. 

For loops computing global aggregates, like the `minimum CFL condition`, we used `#pragma omp parallel for reduction(min:...)` to safely combine thread-local results without race conditions. 

> Definition: 
> CFL = Courant–Friedrichs–Lewy condition.

Loops with sequential dependencies, such as the corrector step updating nodal velocities, were intentionally left serial to maintain correctness. This approach maximised concurrency while avoiding synchronisation overhead and false sharing, resulting in significant runtime improvements on multi-core CPUs.


### Why were some loops were left serial?

Example: Corrector step updating nodal velocities:

```c++
for (int ind = 0; ind < nnd; ind++) {
    // update velocity based on neighboring elements
    ndu[ind] += dt * a;
}
```

- Reason: Each iteration depends on values from neighboring nodes `(ndu[ind-1] or ndu[ind+1])`.

- If we parallelised this naively, threads could read stale values or overwrite each other, producing incorrect physics.

- Decision: Leave these loops serial to ensure numerical correctness. In other words, some calculations are inherently sequential due to data dependencies.

- [x] The factor `0.5` keeps the timestep well below the stability limit.

### Why did we use `#pragma omp parallel for reduction(min:min_cfl)`?

The loop iterates over all elements `iel` to compute a local CFL timestep for each cell:

```c++
double cfl = elv[iel] / sqrt(c2 + 2*elq[iel]);
```

To maintain numerical stability, we need the minimum CFL across all cells.

**Definition:**  
Numerical stability refers to the property of a time-stepping scheme where errors do not grow uncontrollably as the simulation progresses (recall my presentation about the spectral method where if the high energy oscillations aren't treated, they quickly grow and destroy the solution). 

For explicit methods solving hyperbolic PDEs (e.g., the KdV equation...), such as the Euler equations, the timestep `dt` must be small enough relative to the speed at which information propagates across the mesh.

**CFL Condition:**  

In this code, each cell has a *length* (`elv[iel]`) and a *local wave speed* (`sqrt(c2 + 2*elq[iel])`). The Courant–Friedrichs–Lewy (CFL) condition ensures that in one timestep, information from any cell does not travel further than the cell itself:


$$dt \le \frac{\text{cell length}}{\text{local wave speed}}$$


If `dt` is too large, waves can “jump over” cells, producing oscillations, non-physical results, or simulation blow-up.

**Implementation in Code:**

```cpp
double min_cfl = std::numeric_limits<double>::max();
#pragma omp parallel for reduction(min:min_cfl)
for (int iel = 0; iel < nel; iel++) {
    double cfl = elv[iel] / sqrt(c2 + 2*elq[iel]);
    min_cfl = std::min(min_cfl, cfl);
}
dt = 0.5 * min_cfl; // safety factor to ensure stability
```

So to revisit the original statement (why we needed to use `#pragma omp parallel for reduction(min:min_cfl)`) the answer is quite simple.

The Problem: 

- We have a list of numbers — one CFL timestep for each cell.  
- We want **the smallest number** out of the list:

```cpp
for (int i = 0; i < nel; i++) {
    min_cfl = std::min(min_cfl, cfl[i]);
}
```

Doing this one after the other is not only slow for lots of cells, it could lead to a *race condition* in which all threads try to write to `min_cfl` at once and give an invalid answer (if, e.g, using OpenMP).

I changed this by adding 

```c++
#pragma omp parallel for reduction(min:min_cfl)
```
So that:
- [x] Each thread calculates a local minimum.
- [x] OpenMP safely combines these into the global minimum at the end
- [x] Each thread gets its own copy of `min_cfl`. Each thread finds the smallest number in its own chunk of the list.

# Summary 


The code has been modernised to be thread-safe, memory-safe, and performant, while ensuring numerical stability and reproducible outputs. Key technical improvements include:

Careful OpenMP parallelisation with loop classification: independent loops, reductions for global aggregates, and serial loops for sequential dependencies.

CFL-based timestep control for explicit time-stepping stability.

Redirected output to a structured folder for post-processing.

I also added some quality of life changes. Please take a look at the revised folder structure. Each run of numerics is appended to the "data" folder. 
# Simulation and percolation

## The surface

- A square substrate of side `GRID_SIZE_MICRONS` (default 100 µm).
- Coverage is measured on an N×N mesh (`MESH_POINTS`). A mesh point is covered if it lies inside any circle. Coverage fraction = covered points ÷ total points. Parts of circles that extend past the edge are not counted.

## Nucleation (`utils/math.py`)

`random_points(num_circles, surface_dim, random_seed)`:

- Seeds Python's `random` and NumPy's global RNG (`utils/seeding.set_seed`).
- Draws integer coordinates `x, y ∈ [0, surface_dim)` one point at a time.
- Accepts a point only if its distance to **every** existing point is strictly between **5 µm and 140 µm** (`two_points_distance`). On a 100 µm grid the upper bound never applies, since the diagonal is about 141 µm, so in practice this is a minimum-spacing rule.
- Retries until it has `NUM_CIRCLES` valid points. If the grid cannot fit that many points at 5 µm spacing, it never finishes.

`build_initial_circles()` turns each point into a `matplotlib.patches.Circle` of radius `INITIAL_RADIUS_MICRONS`.

## Growth step

All flakes have the same radius at a given time. For each time step `t` with fitted coverage `S(t)` (%):

1. **Analytical estimate:** split the target area evenly across the `n` circles, ignoring overlaps:

   $$
   A_{circle} = \frac{S(t)}{n}\times 100,\qquad r = \sqrt{A_{circle}/\pi}
   $$

   The factor `100` converts percent to µm² on a 100 × 100 µm grid (`S/100 · 10 000 µm²`).
2. **Measure** the actual coverage on the mesh. Overlapping and out-of-bounds parts make it lower than the target.
3. **Correction loop:** while `S(t) − measured > 1` percentage point, add the missing area to the per-circle area, recompute the radius, regrow and measure again. The loop only grows circles and never shrinks them.
4. The corrected circles carry over to the next time step. Only their centres matter, because the radius is recomputed from scratch each step.

Recorded per step: target coverage, coverage before correction (`initial_simulated_coverage_pct`) and after (`final_simulated_coverage_pct`).

## Connectivity graph (`utils/visualization.generate_graph`)

- **Nodes:** circles.
- **Edges:** two circles touch if the distance between their centres ≤ `r₁ + r₂ + 0.01` µm (`two_circles_touching`, tolerance 0.01 µm).
- **Boundary sets:** a circle touches an edge if the distance from its centre to that edge (a `shapely` `LineString`) ≤ its radius (`circle_touches_line`). Four sets are built: `top`, `bottom`, `left` and `right`.

Graph construction compares every pair of circles, which is O(n²). For 48 circles that is cheap compared with the mesh work.

> Edge naming: `top` is the line y = 0 and `bottom` is y = `GRID_SIZE`, which matches image row order. Both directions are checked, so the naming does not change the result.

## Percolation test (`utils/search_algorithm.breadth_first_search`)

- **Top → bottom:** for each circle touching the top edge, run a breadth-first search over the graph. If any search reaches a circle that touches the bottom edge, the step percolates top-to-bottom.
- **Left → right:** the same, between the left and right edges.
- A step **percolates** if either direction is connected (`percolates = top_to_bottom or left_to_right` in the CSV).

The BFS returns the visit order and a found flag. The pipelines only use the flag.

## Surface vs. Monte Carlo

| | `surface` | `n_simulations` |
|---|---|---|
| Seeds | `RANDOM_SEED` (one run) | Random seed per run (not reproducible) |
| Time steps | All | Stops at the first percolating step |
| Output | One row per time step | One row per simulation |
| Figures | Optional, per time step | None |
| Parallel | No | Yes (`multiprocessing.Pool`) |

# Known limitations

Behaviour of the current code that can surprise users, gathered from reading it. These are documented and not yet changed.

## Grid size is effectively fixed at 100 µm

The growth step converts coverage to per-circle area with `S / n * 100` (all `run_surface_*` and `run_simulations_*` scripts). That conversion is only correct when the grid area is 10 000 µm², i.e. `GRID_SIZE_MICRONS=100`. With a larger grid the correction loop makes up the difference over more iterations. With a smaller grid the first estimate overshoots, and the loop never shrinks circles, so the measured coverage comes out above the target.

## `SHOW_PLOTS` saves figures and does not show them

No code calls `plt.show()`. `SHOW_PLOTS=True` means "create and save figures". In the `surface` task that means one PNG and one PDF per time step, which is slow.

## Monte Carlo runs are not reproducible

`n_simulations` draws seeds from an unseeded `numpy.random.default_rng()`, so `RANDOM_SEED` has no effect there. Every seed is recorded in the `seed_used` column, so you can reproduce any single run by setting `RANDOM_SEED` to that value and running `surface`.

## `results` assumes every run percolated

The `results` task fits a Gaussian to `percolation_final_coverage_pct` and `percolation_time_min` without dropping rows where `percolated` is `False`, whose values are empty (NaN). A single non-percolating run makes the fitted mean and std NaN. With the default parameters coverage approaches 100 %, so every run percolates in practice. Filter the CSV first if you change the parameters.

## Logistic derivative in the surface plot

`run_surface_logistic.py` calls `logistic_derivative(t_fit, S_fit, k, t0)`, which passes the fitted curve `S_fit` where the scalar saturation `L` is expected. The plotted "Derivative" is therefore $S(t)\cdot k\,e^{-k(t-t_0)}/(1+e^{-k(t-t_0)})^2$ rather than $dS/dt$. Only the figure is affected, not the simulation.

## Unused configuration

`DATA_DIR`, `RAW_DIR`, `PROCESSED_DIR` and `RADIUS_MICRONS` are read but never used. They still have to be set (the numeric ones are parsed when the config is built).

## Nucleation can loop forever

`random_points()` retries until it has placed every point at ≥ 5 µm spacing. If `NUM_CIRCLES` is too large for `GRID_SIZE_MICRONS`, it never returns.

## Zero standard deviations

With `USE_STD=True`, a data row with `standard_deviation = 0` (such as the `0, 0, 0` point in `original_experimental_data.txt`) causes a division by zero in the weighted fit. `experimental_raw.csv` leaves that row out for this reason.

## Duplicated pipeline code

`simulate_growth` / `simulate_growth_until_percolation` are copied across four scripts. Keep them in sync when changing the algorithm.

## Run from the project root

Paths in `.env` and the package imports (`config`, `utils`, …) assume the current working directory is the project root.

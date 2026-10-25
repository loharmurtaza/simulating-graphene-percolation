# CLI and pipelines

## Command line

```bash
python -m main --model {logistic,exponential} --task {surface,n_simulations,results}
```

Both arguments are required. `main.cli()`:

1. Sets up logging (console and `logs/run_<timestamp>.log`).
2. Builds the config dataclasses the task needs.
3. Calls the matching `run_pipeline_<model>` function from `scripts/`.

| `--task` | Config objects | Logistic pipeline | Exponential pipeline |
|----------|----------------|-------------------|----------------------|
| `surface` | `SurfaceCoverageConfig` | `scripts/run_surface_logistic.py` | `scripts/run_surface_exponential.py` |
| `n_simulations` | `SurfaceCoverageConfig`, `SimulationsConfig` | `scripts/run_simulations_logistic.py` | `scripts/run_simulations_exponential.py` |
| `results` | `FinalResultsConfig` | `scripts/run_results_logistic.py` | `scripts/run_results_exponential.py` |

Each script also has a `__main__` block, so for example `python -m scripts.run_surface_logistic` runs it directly. Note that this path does **not** call `setup_logging()`, so you get no log output.

---

## `surface`: single run

Purpose: follow one random arrangement of flakes through the whole growth process and record when it percolates.

1. **Load data:** `load_experimental_raw_data()` returns time, coverage and std arrays.
2. **Fit the model:** see [growth-models.md](growth-models.md).
   - Logistic: fit `L, k, t0`. Time grid `t_fit = 0, 0.1, …, 27.0` min (271 steps).
   - Exponential: fit `α, C₁`. Time grid `t_fit = linspace(-C₁/α, 30, 500)` (500 steps).
3. **Plot the fit** (if `SHOW_PLOTS`): data with error bars, fitted curve and derivative. The exponential plot also marks the inflection point (maximum of the derivative).
4. **Mean flake area estimate:** a linear fit of mean area against coverage from two measured samples (`6.8 µm²` at `3.2 %`, `106.58 µm²` at `51.2 %`), extrapolated to every experimental point. This is informational only and goes to the log.
5. **Nucleation:** `random_points()` places `NUM_CIRCLES` centres using `RANDOM_SEED`, then `build_initial_circles()` creates circles of radius `INITIAL_RADIUS_MICRONS`.
6. **Growth:** `simulate_growth()` runs through every time step, grows the circles to the fitted coverage and checks percolation. See [simulation-and-percolation.md](simulation-and-percolation.md). It runs all time steps and does not stop at percolation.
7. **Save:** one CSV row per time step, plus one before/after-correction coverage figure per time step if `SHOW_PLOTS`.

> With `SHOW_PLOTS=True`, the surface task writes a PNG and a PDF at 300 dpi for **every** time step (271 for logistic, 500 for exponential). That is the slowest part of the task. Set `SHOW_PLOTS=False` if you only need the CSV.

---

## `n_simulations`: Monte Carlo

Purpose: estimate the distribution of the percolation threshold (coverage and time) over many random flake arrangements.

1. Fit the model once. All simulations share it.
   - Logistic time grid: `0 … 27.0` step `0.1`.
   - Exponential time grid: `-C₁/α … 27.0` step `0.1`.
2. Draw `SIMULATIONS_TO_RUN` seeds from `numpy.random.default_rng()`, which has no fixed seed, so **runs are not reproducible**.
3. Spread the work over `min(MAX_WORKERS, cpu_count())` processes with `multiprocessing.Pool.imap_unordered`, showing a `tqdm` progress bar.
4. Each worker (`_run_single_simulation`):
   - places new nucleation sites with its own seed,
   - calls `simulate_growth_until_percolation()`, which is the same growth step as `surface` but **returns at the first time step where either direction percolates**,
   - returns a `SimulationResult` as a dict.
5. Write all results to `csvs/growth_results_simulations_<model>.csv`. Rows are in completion order, not ID order.

No figures are produced.

---

## `results`: statistics

Purpose: summarise the Monte Carlo output.

1. Read `<PERCOLATIONS_CSV_DIR>/growth_results_simulations_<model>.csv` with `index_col=0` (`simulation_id` becomes the index).
2. Fit a normal distribution (`scipy.stats.norm.fit`) to:
   - `percolation_final_coverage_pct`: area fraction at percolation,
   - `percolation_time_min`: time of percolation.
3. Plot two histograms with the scaled Gaussian overlaid and the mean marked, labelled **a** (area fraction) and **b** (time).
4. Save the figure as PNG and PDF.

The axis limits are hard-coded to the ranges in the paper: area fraction 40–90 %, time 4.9–7.0 min (logistic) or 4.4–7.8 min (exponential). Change them in `plot_gaussian_curves()` if your parameters move the threshold.

The logistic and exponential versions differ only in plot styling (bin count, y-axis labels, output subfolder).
